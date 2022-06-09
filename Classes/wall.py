from Classes.entity import Entity


class Wall(Entity):
    # Wall inherits Entity and contain a tuple of coordinates that is just... illegal
    #
    def __init__(self, coord, sprite, index):
        Entity.__init__(self, coord, sprite, index)
