import random
import math

#represent a pokemon and it associated stats
class Pokemon:
    def __init__(self, name, level, types, stats, moves):
        self.name = name
        self.level = level
        self.types = types

        self.hp = stats["hp"]
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
    "NidoranM": 50,
    "NidoranF": 41,
    "Rattata": 72,
    "Geodude": 20,
    "Onix": 70
}

#The environment in which the AI will intereact with
class PokemonEnv:
    def __init__(self):
        self.set_initial_state()

    #reset the game state to it initial state
    def set_initial_state(self):
        self.player_team = [
            Pokemon("Bulbasaur", 13, ["GRASS", "POISON"], {"hp": 41, "attack": 20, "defense": 20, "special": 25, "speed": 19}, ["Tackle", "Vine Whip"]),
            Pokemon("NidoranM", 13, ["POISON"], {"hp": 39, "attack": 25, "defense": 18, "special": 19, "speed": 22}, ["Tackle", "Horn Attack"]),
            Pokemon("NidoranF", 13, ["POISON"], {"hp": 40, "attack": 22, "defense": 20, "special": 18, "speed": 19}, ["Tackle", "Scratch"]),
            Pokemon("Rattata", 13, ["NORMAL"],  {"hp": 32, "attack": 20, "defense": 15, "special": 12, "speed": 25}, ["Tackle", "Quick Attack"])
        ]

        self.opponent_team = [
            Pokemon("Geodude", 12, ["ROCK", "GROUND"], {"hp": 40, "attack": 25, "defense": 30, "special": 15, "speed": 10}, ["Tackle", "Bide"]),
            Pokemon("Onix", 14, ["ROCK", "GROUND"], {"hp": 45, "attack": 20, "defense": 50, "special": 15, "speed": 25}, ["Tackle", "Bide"])
        ]

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

