from Classes.entity import Entity
from random import randint


class WaterBottle(Entity):
    # class initializer
    def __init__(self, coord, sprite, player_stats, index=0, args=()):
        """
        WaterBottle entity, inherits Entity.

        :param player_stats: The playerStats object
        :param index: (Integer) How many of these same entities were already created
        :param coord: (List of Integers) X and Y coordinates in tiles
        :param sprite: (Surface) Pygame image to display this entity
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """
        Entity.__init__(self, coord, sprite, index, args)
        self.__player_stats = player_stats
        self.interactable = True

    def drink(self):
        """
        Adds a random hydration to the player (between 3-6)
        """
        self.__player_stats.add_thirst(randint(3, 6))
        self.scene.remove_entity(self.ID)


class CannedFood(Entity):
    # class initializer
    def __init__(self, coord, sprite, player_stats, index=0, args=()):
        """
        CannedFood entity, inherits Entity.

        :param player_stats: The playerStats object
        :param index: (Integer) How many of these same entities were already created
        :param coord: (List of Integers) X and Y coordinates in tiles
        :param sprite: (Surface) Pygame image to display this entity
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """

        Entity.__init__(self, coord, sprite, index, args)
        self.__player_stats = player_stats
        self.interactable = True

    def eat(self):
        """
        Adds a random saturation to the player (between 3-6)
        """
        self.__player_stats.add_hunger(randint(3, 6))
        self.scene.remove_entity(self.ID)