# Agent-Environment Interface Contract

This document specifies the API between the Q-learning agent and the Pokémon battle environment. The environment must conform to this interface so that the agent (already implemented in `agent.py` and validated on FrozenLake-v1) can be plugged in without modification.

The interface follows [Gymnasium](https://gymnasium.farama.org/) conventions.

## Overview

The agent interacts with the environment through a standard loop:

```python
state, info = env.reset()
done = False
while not done:
    action = agent.choose_action(state)
    next_state, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    agent.update(state, action, reward, next_state, done)
    state = next_state
```

The environment must implement `reset()` and `step()` matching the signatures below.

## State Representation

**Proposed format:** a tuple of integers, hashable and usable as a dictionary key.

```python
state = (
    player_pokemon_id,    # int, 0 to N_PLAYER_POKEMON - 1
    player_hp_bucket,     # int, 0 to 3 (quartiles: 0-25%, 26-50%, 51-75%, 76-100%)
    opponent_pokemon_id,  # int, 0 to N_OPPONENT_POKEMON - 1
    opponent_hp_bucket,   # int, 0 to 3
    turn,                 # int, capped at MAX_TURNS (e.g., 20)
)
```

**Rationale:**
- HP is bucketed (not raw integers) to keep the state space tractable for a tabular Q-table. Without bucketing, HP alone could push the state space into the millions.
- Status conditions (poison, paralysis, sleep, burn, freeze) are **not** included in v1 to keep the state space small. Can be added later if needed.
- Turn number is included to let the agent reason about pacing (e.g., "I should switch now before it's too late").

**Open question:** Should status conditions be part of v1? Recommend deferring until baseline is working.

## Action Space

**Type:** `gymnasium.spaces.Discrete(N)`

**Proposed encoding** (assuming 4 moves per Pokémon and up to 2 switch options):

| Action ID | Meaning             |
|-----------|---------------------|
| 0         | Use move slot 0     |
| 1         | Use move slot 1     |
| 2         | Use move slot 2     |
| 3         | Use move slot 3     |
| 4         | Switch to Pokémon 1 |
| 5         | Switch to Pokémon 2 |

Total: `N = num_moves + num_switch_targets`.

**Invalid action handling:** If the agent picks an action that isn't legal in the current state (e.g., switching to a fainted Pokémon, using a move slot the active Pokémon doesn't have), the environment should either:
- (a) Ignore the action and apply a small negative reward, or
- (b) Treat it as a no-op and let the opponent take its turn.

**Open question:** Action masking via `info["action_mask"]` would be cleaner but adds complexity. Recommend deferring to v2.

## Reward Structure

**Proposed v1 (sparse):**

| Event              | Reward |
|--------------------|--------|
| Win the battle     | +1.0   |
| Lose the battle    | -1.0   |
| Every other step   |  0.0   |

**Rationale:** Sparse rewards are simpler and avoid biasing the agent toward intermediate behaviors that may not lead to winning. The Q-learning algorithm will propagate the terminal reward back through the trajectory via the Bellman update.

**Optional shaping (defer to v2 if v1 doesn't converge):**

| Event                              | Reward |
|------------------------------------|--------|
| Faint an opponent Pokémon          | +0.3   |
| Lose a Pokémon                     | -0.3   |
| Deal damage (per % HP removed)     | +0.001 |

Shaping rewards can accelerate learning but risk the agent finding loopholes (e.g., dragging out the battle for damage points). Only add if needed.

## API Signatures

### `reset() -> (state, info)`

Resets the environment to the start of a new battle.

- Restores all Pokémon to full HP.
- Clears any status conditions.
- Resets the turn counter to 0.
- Sets the active Pokémon to the first slot on each side.

**Returns:**
- `state`: tuple matching the state representation above.
- `info`: dict, may be empty. Can include debugging info (e.g., `{"player_team": [...], "opponent_team": [...]}`).

### `step(action) -> (next_state, reward, terminated, truncated, info)`

Executes one turn of battle. A "turn" includes both the player's action and the opponent's action, with order determined by Speed stat.

**Arguments:**
- `action`: int, must be in `[0, N)` where N is the size of the action space.

**Returns:**
- `next_state`: tuple matching the state representation, reflecting the post-turn battle state.
- `reward`: float, as specified in the reward structure section.
- `terminated`: bool, `True` if the battle ended (one side has no remaining Pokémon).
- `truncated`: bool, `True` if the turn limit (`MAX_TURNS`) was hit without a winner. Treated as a loss for reward purposes.
- `info`: dict, optional debugging info (e.g., damage dealt, status applied).

### `observation_space` and `action_space`

The environment should expose these as Gymnasium spaces for introspection:

```python
env.observation_space  # gymnasium.spaces.MultiDiscrete or Tuple
env.action_space       # gymnasium.spaces.Discrete(N)
```

This lets the agent be initialized without hardcoding sizes:

```python
agent = QLearningAgent(
    n_states=...,  # derived from observation_space
    n_actions=env.action_space.n,
)
```

## Constants to Agree On

These should be defined once (e.g., in `env/constants.py`) and imported by both sides:

```python
N_PLAYER_POKEMON = ?      # how many Pokémon the player brings (proposal: 3-4)
N_OPPONENT_POKEMON = 2    # Geodude + Onix (Brock's team in Pokémon Blue)
MAX_TURNS = 20            # cap on battle length
HP_BUCKETS = 4            # quartiles
```

## Open Questions / TODOs

- [ ] Final list of which player Pokémon are available (subset of the 29 from the proposal).
- [ ] Confirm whether status conditions are in v1 state.
- [ ] Confirm reward shaping decision (sparse vs. shaped).
- [ ] Confirm invalid-action handling strategy.
- [ ] Decide on `observation_space` type (`MultiDiscrete` vs. `Tuple`).

## Notes for the Agent Side

When switching from FrozenLake (integer states) to Pokémon (tuple states), the Q-table representation in `QLearningAgent` will need to change from `np.zeros((n_states, n_actions))` to a `defaultdict(lambda: np.zeros(n_actions))`. This is a small, isolated change and does not affect the rest of the agent code.