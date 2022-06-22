# consumables.py
# Esteban, Richard, Utkarsh, Sam
# June 14, 2022
from Classes.entity import Entity
from random import randint


class WaterBottle(Entity):
    # class initializer
    def __init__(self, coord, sprite, index=0, args=()):
        """
        WaterBottle entity, inherits Entity.

        :param index: (Integer) How many of these same entities were already created
        :param coord: (List of Integers) X and Y coordinates in tiles
        :param sprite: (Surface) Pygame image to display this entity
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """
        Entity.__init__(self, coord, sprite, index, args)
        self.interactable = True

    def drink(self):
        """
        Returns a random hydration to the player (between 3-6)
        """
        self.scene.remove_entity(self.ID)
        return randint(3, 6)

    def interact(self):
        return "EATEN"


class CannedFood(Entity):
    # class initializer
    def __init__(self, coord, sprite, index=0, args=()):
        """
        CannedFood entity, inherits Entity.

        :param index: (Integer) How many of these same entities were already created
        :param coord: (List of Integers) X and Y coordinates in tiles
        :param sprite: (Surface) Pygame image to display this entity
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """

        Entity.__init__(self, coord, sprite, index, args)
        self.interactable = True

    def eat(self):
        """
        Returns a random saturation to the player (between 3-6)
        """
        self.scene.remove_entity(self.ID)
        return randint(3, 6)
    def interact(self):
        return "EATEN"