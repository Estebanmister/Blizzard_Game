from Classes.entity import Entity
from Classes.player_stats import PlayerStats
from random import randint


class WaterBottle(Entity):
    def __init__(self, coord, sprite, player_stats, index=0, args=()):
        Entity.__init__(self, coord, sprite, index, args)
        self.__player_stats = player_stats

    def drink(self):
        self.__player_stats.add_thirst(randint(3, 6))


class CannedFood(Entity):
    def __init__(self, coord, sprite, player_stats, index=0, args=()):
        Entity.__init__(self, coord, sprite, index, args)
        self.__player_stats = player_stats

    def eat(self):
        self.__player_stats.add_hunger(randint(3, 6))


test = PlayerStats()
food = CannedFood()
