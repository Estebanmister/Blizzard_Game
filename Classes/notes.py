from Classes.entity import Entity

class Notes(Entity):
    def __init__(self, coord, sprite, player_stats, index=0, args=()):
        Entity.__init__(self, coord, sprite, index, args)

    def show_test(self):
        pass