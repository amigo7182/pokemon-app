# Pokémon Blue Auto Battler

This project use Q-learning algorithm to learn how to play Pokémon Blue first gym. The result it come up with after training can be used as a 
guide for new player on how to approach the battle. Pokémon game can have steep learning curve and intricate mechanics that can easily overwhelm 
new players, leading to early frustration and players abandoning the game altogether. By building this application, we hope that it will help 
new players who are overwhelmed with the game’s mechanics to grasp how to play the game faster.


## Environment Setup
* This project requires Python version 3.14 or higher
* The environment was built using the standard Python library with the addition of `numpy` (version 2.4.6 or higher) as the sole external dependency
* Using `pyproject.toml` and `uv.lock` file, the `uv` package manager can be used for rapid setup
* **To set up the environment using `uv`**: Run `uv sync` in the repository root to automatically install dependencies and lock the environment.
* **To set up the environment using `pip`**: Run `pip install numpy>=2.4.6` in your terminal.

## Execution Instructions
The main script has two different modes of operation: training and simulation.
* **Training Mode:** Execute `python main.py train` in your terminal. This will initialize the environment and the Q-learning agent, run the training episodes,
and print the average reward per 500 episodes trained. Once completed, it will save the learned Q-table to `Q_table.pickle`.
* **Simulation Mode:** Execute `python main.py` in your terminal. The agent will automatically load the saved `Q_table.pickle` file, run the game, and print
out the turn-by-turn log of the battle.

## Code Organization
* **`main.py`:** The entry point of the application. It contains the primary `train()` loop to train Q-learning agent and the `simulation()` function
that runs the battle sequence and outputs the battle log.
* **`environment.py`:** Simulates the core game mechanics, managing player actions, turn progression, and damage calculations. It defines the `PokemonEnv`
class, the state space, and the action space.
* **`agent.py`:** Acts as the model, navigating the environment and determining move selection. It contains the `QLearningAgent` class which update the
Q-table using Bellman equation.

## Acknowledgments
During project implementation, Gemini has been utilized to help us figure out how Pokémon Blue game engine works. It has also been used to help us identify 
bugs in our program, help draft the overview of agent-environment contract, which allows different teams interface to line up, and help draft some components 
of this ReadMe.
