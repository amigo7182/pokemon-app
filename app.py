import random
import math

#represent a pokemon and it associated stats
class Pokemon:
    def __init__(self, name, level, types, stats, moves):
        self.name = name
        self.level = level
        self.types = types

        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.special = stats["special"]
        self.speed = stats["speed"]
        self.moves = moves

#represent a move that pokemon can make
class Move:
    def __init__(self, name, type, power):
        self.name = name
        self.type = type
        self.power = power

#different move available to pokemon
MOVES = {
    "Tackle": Move("Tackle", 35, "NORMAL"),
    "Quick Attack": Move("Quick Attack", 40, "NORMAL"),
    "Scratch": Move("Scratch", 40, "NORMAL"),
    "Vine Whip": Move("Vine Whip", 35, "GRASS"), 
    "Horn Attack": Move("Horn Attack", 65, "NORMAL"),       
    "Bide": Move("Bide", 0, "NORMAL")
}

#the chart to look up to see how effective a pokemon type is against other pokemon type, if not listed
#the effectiveness is 1.0
TYPE_EFFECTIVENESS_CHART = {
    ("NORMAL", "ROCK"): 0.5,
    ("FLYING", "ROCK"): 0.5,
    ("GRASS", "ROCK"): 2.0,
    ("GRASS", "GROUND"): 2.0
}

#the base speed of different pokemon
BASE_SPEEDS = {
    "Bulbasaur": 45,
    "Nidoran♂": 50,
    "Nidoran♀": 41,
    "Rattata": 72,
    "Geodude": 20,
    "Onix": 70
}

#The environment in which the AI will intereact with
class PokemonEnv:
    def __init__(self):
        self.reset()

    #Reset the game state to it initial state
    def reset(self):
        self.player_team = [
            Pokemon("Bulbasaur", 13, ["GRASS", "POISON"], {"hp": 41, "attack": 20, "defense": 20, "special": 25, "speed": 19}, ["Tackle", "Vine Whip"]),
            Pokemon("Nidoran♂", 13, ["POISON"], {"hp": 39, "attack": 25, "defense": 18, "special": 19, "speed": 22}, ["Tackle", "Horn Attack"]),
            Pokemon("Nidoran♀", 13, ["POISON"], {"hp": 40, "attack": 22, "defense": 20, "special": 18, "speed": 19}, ["Tackle", "Scratch"]),
            Pokemon("Rattata", 13, ["NORMAL"],  {"hp": 32, "attack": 20, "defense": 15, "special": 12, "speed": 25}, ["Tackle", "Quick Attack"])
        ]

        self.opponent_team = [
            Pokemon("Geodude", 12, ["ROCK", "GROUND"], {"hp": 40, "attack": 25, "defense": 30, "special": 15, "speed": 10}, ["Tackle", "Bide"]),
            Pokemon("Onix", 14, ["ROCK", "GROUND"], {"hp": 45, "attack": 20, "defense": 50, "special": 15, "speed": 25}, ["Tackle", "Bide"])
        ]

        self.player_active_pokemon = self.player_team[0]
        self.opponent_active_pokemon = self.opponent_team[0]

        return self.get_state()

    #Get the current state of the game
    def get_state(self):
        player_team_health = (0,) * 4
        opponent_team_health = (0,) * 2

        for index, pokemon in enumerate(self.opponent_team):
            player_team_health[index] = self.calculate_health_bracket(pokemon.hp, pokemon.max_hp)

        for index, pokemon in enumerate(self.opponent_team):
            opponent_team_health[index] = self.calculate_health_bracket(pokemon.hp, pokemon.max_hp)

        return (self.player_active_pokemon.name, player_team_health, self.opponent_active_pokemon.name, opponent_team_health)

    #Calculate the health bracket the pokemon is in
    def calculate_health_bracket(self, hp, max_hp):
        health_ratio = hp / max_hp
        if hp <= 0:
            return 0
        elif health_ratio > 0.5:
            return 3
        elif health_ratio > 0.25:
            return 2
        else:
            return 1

    #Get a list of possible action at the current state of the game
    def get_possible_actions(self):
        possible_actions_list = []

        for move in self.player_active_pokemon.moves:
            possible_actions_list.append("FIGHT_" + move)

        for pokemon in self.player_team:
            if pokemon.name != self.player_active_pokemon.name and pokemon.hp != 0:
                possible_actions_list.append("SWITCH_" + pokemon.name)
        
        possible_actions_list.append("RUN")

        return possible_actions_list

    #Use when a player take a specific action in the game
    def step(self, action):
        reward = -1
        done = False
        log = []

        player_action_type = action.split("_")[0]
        player_move = action.split("_")[1]
        opponent_move = random.choice(["Tackle","Bide"])

        player_go_first = True

        if player_action_type == "SWITCH" or player_action_type == "RUN":
            player_go_first = True
        else:

            if player_move == "Quick attack":
                player_go_first = True
            else:
                if self.player_active_pokemon.speed > self.opponent_active_pokemon.speed:
                    player_go_first = True
                elif self.player_active_pokemon.speed < self.opponent_active_pokemon.speed:
                    player_go_first = False
                else:
                    player_go_first = random.choice([True, False])

        def execute_player_turn(current_reward, is_done):
            opponent_turn_skipped = False
            if player_action_type == "RUN":
                log.append("No! There's no running from a trainer battle!")
                current_reward = current_reward - 10
            elif player_action_type == "SWITCH":
                log.append(self.player_active_pokemon.name + " OK! Come back!")
                for pokemon in self.player_team:
                    if pokemon.name == player_move:
                        self.player_active_pokemon = pokemon
                        log.append("Go! " + pokemon.name + "!")
            else:
                log.append(self.player_active_pokemon.name + " used " + player_move + "!")
                move = MOVES[player_move]
                damage = self.calculate_damage(self.player_active_pokemon, self.opponent_active_pokemon, move)
                self.opponent_active_pokemon.hp = self.opponent_active_pokemon.hp - damage
                log.append(self.player_active_pokemon.name + " dealt " + str(damage) + " damage to " + self.opponent_active_pokemon.name 
                           + "! " + self.opponent_active_pokemon.name + " have " + str(max(0, self.opponent_active_pokemon.hp)) + " hp remaining")
                
                if self.opponent_active_pokemon.hp <= 0:
                    self.opponent_active_pokemon.hp = 0
                    log.append(self.opponent_active_pokemon.name + " fainted!")
                    if self.opponent_active_pokemon.name == "Geodude":
                        current_reward = current_reward + 100
                        self.opponent_active_pokemon = self.opponent_team[1]
                        log.append("Leader Brock sent out Onix!")
                        opponent_turn_skipped = True
                    else:
                        current_reward = current_reward + 1000
                        is_done = True
                        log.append("Player defeated Leader Brock!")
            return current_reward, is_done, opponent_turn_skipped
        
        def execute_opponent_turn(current_reward, is_done):
            player_turn_skipped = False

            log.append(self.opponent_active_pokemon.name + " used " + opponent_move + "!")
            move = MOVES[opponent_move]
            damage = self.calculate_damage(self.opponent_active_pokemon, self.player_active_pokemon, move)
            self.player_active_pokemon.hp = self.player_active_pokemon.hp - damage

            if move.power > 0:
                log.append(self.opponent_active_pokemon.name + " dealt " + str(damage) + " damage to " + self.player_active_pokemon.name 
                            + "! " + self.player_active_pokemon.name + " have " + str(max(0, self.player_active_pokemon.hp)) + " hp remaining")
                
            if self.player_active_pokemon.hp <= 0:
                self.player_active_pokemon.hp = 0
                log.append(self.player_active_pokemon.name + " fainted!")
                current_reward = current_reward - 50
                player_turn_skipped = True

                alive_pokemon = []
                for pokemon in self.player_team:
                    if pokemon.hp > 0:
                        alive_pokemon.append(pokemon)

                if not alive_pokemon:
                    log.append("Player is out of usable pokemon! Player blacked out!")
                    is_done = True
                    current_reward = current_reward - 500
                else:
                    self.player_active_pokemon = random.choice(alive_pokemon)
                    log.append("Go! " + self.player_active_pokemon + "!")
                    
            return current_reward, is_done, player_turn_skipped
        
        if player_go_first:
            reward, done, skipped_turn = execute_player_turn(reward, done)

            if not done and not skipped_turn:
                reward, done, skipped_turn = execute_opponent_turn(reward, done)
        else:
            reward, done, skipped_turn = execute_opponent_turn(reward, done)

            if not done and not skipped_turn:
                reward, done, skipped_turn = execute_player_turn

        return self.get_state(), reward, done, log   

    #calculating the damage that attacker pokemon will deal to defender pokemon using a specific move
    #Google Gemini has been used to help us research and partially guide us when we are trying to implement Pokémon Blue damage calculation.
    def calculate_damage(self, attacker, defender, move):
        #some move have a base power of 0 which result in the pokemon not dealing any damage
        if move.power == 0: return 0

        #calculate the multiplier due to the type match up
        type_effectiveness = 1.0
        for def_type in defender.types:
            type_effectiveness = type_effectiveness * TYPE_EFFECTIVENESS_CHART.get((move.type, def_type), 1.0)

        if type_effectiveness == 0.0: return 0

        #calculate the effect of crit
        base_speed = BASE_SPEEDS[attacker.name]
        is_crit = random.random() < (base_speed / 512.0)
        if is_crit:
            level = attacker.level * 2
        else:
            level = attacker.level

        #add in the effect of the move type
        if move.type in ["FIRE", "WATER", "GRASS", "ELECTRIC", "ICE", "PSYCHIC", "DRAGON"]:
            attack = attacker.special
            defense = defender.special
        else:
            attack = attacker.attack
            defense = defender.defense

        #add in the same type attack bonus
        if move.type in attacker.types:
            stab = 1.5
        else:
            stab = 1.0

        #add in random variance
        random_multiplier = random.randint(217, 255) / 255.0

        return math.floor((math.floor((math.floor(level * 2 / 5 + 2) * move.power * attack / defense) / 50) + 2) * stab * type_effectiveness * random_multiplier)

