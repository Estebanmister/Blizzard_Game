# collisionentity.py
# Esteban, Richard, Utkarsh, Sam
# June 13, 2022
from Classes.entity import Entity


class CollisionEntity(Entity):

    # CollisionEntity inherits Entity and contain a tuple of coordinates that is just... illegal
    def __init__(self, coord, sprite, index=0, args=()):
        """
        Creates a collision entity, that will add an illegal coordinate to the scene, to restrict movement

        :param coord: (tuple) X and Y coordinates in tiles, in form of (x,y)
        :param sprite: (Surface) Pygame image to display for a CollisionEntity entity
        :param index: (Integer) How many CollisionEntity entities were already created
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """
        Entity.__init__(self, coord, sprite, index, args=args)
        self.__coord = coord

    def get_coord(self):
        """
        :return: Coordinate of the CollisionEntity entity
        """
        return self.__coord
