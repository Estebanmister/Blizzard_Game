from Classes.entity import Entity


class Wall(Entity):

    # Wall inherits Entity and contain a tuple of coordinates that is just... illegal
    def __init__(self, coord: tuple, sprite, index=0, args=()):
        """
        Creates a wall entity

        :param coord: (tuple) X and Y coordinates in tiles, in form of (x,y)
        :param sprite: (Surface) Pygame image to display for a wall entity
        :param index: (Integer) How many wall entities were already created
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """
        Entity.__init__(self, coord, sprite, index, args=args)
        self.__coord = coord

    def get_coord(self):
        """
        :return: Coordinate of the wall entity
        """
        return self.__coord
