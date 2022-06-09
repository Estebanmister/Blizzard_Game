from Classes.entity import Entity


class Wall(Entity):

    # Wall inherits Entity and contain a tuple of coordinates that is just... illegal
    def __init__(self, coord, sprite, index=0, args=()):
        Entity.__init__(self, coord, sprite, index, args=args)
        self.__coord = coord

    def get_coord(self):
        return self.__coord
