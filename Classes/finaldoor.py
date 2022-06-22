# finaldoor.py
# Esteban, Richard, Utkarsh, Sam
# June 21, 2022
from Classes.collisionentity import CollisionEntity


class FinalDoor(CollisionEntity):
    def __init__(self, coord, sprite, index=0, args=()):
        """
        This entity will allow the player to exit the dungeon and load another one,
         defined by the address string on args[0]
        Requires to be interacted with in order to change dungeon
        :param coord: (tuple of ints) Where to place the door on the grid
        :param sprite: (pygame.Surface) Sprite of the door
        :param index: (int) How many of these are already in the scene (not to be used by frontend)
        :param args: (List of Strings) String[0]: The location of the dungeon this door leads to
        """
        CollisionEntity.__init__(self, coord, sprite, index, args)
        self.interactable = True
        self.where = args[0]

    def interact(self):
        return "EXIT " + self.where