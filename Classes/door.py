# doors.py
# Esteban, Richard, Utkarsh, Sam
# June 15, 2022
from Classes.collisionentity import CollisionEntity


class Door(CollisionEntity):
    def __init__(self, coord, sprite, index=0, args=()):
        """
        Door class, will allow the player to move to the closest linked room, according to where the Door is placed inside of the scene
        Requires to be interacted with in order to change scene
        :param coord: (tuple of ints) Where to place the door on the grid
        :param sprite: (pygame.Surface) Sprite of the door
        :param index: (int) How many of these are already in the scene (not to be used by frontend)
        :param args: Not used for Doors
        """
        CollisionEntity.__init__(self, coord, sprite, index, args)
        self.interactable = True

    def interact(self):
        """
        Using the width and height of the scene, calculate which side of the scene the door is closest to
        :return: String, "MOVE " + 'up' or 'down' or 'left' or 'right'
        """
        width = self.scene.width
        length = self.scene.length
        # Calculate distances from the edges of the scene
        distance_from_left = abs(self.coord[0] - 0)
        distance_from_right = abs(self.coord[0] - length + 1)
        distance_from_up = abs(self.coord[1] - 0)
        distance_from_down = abs(self.coord[1] - width + 1)
        # Put them in a list
        distances = [distance_from_left, distance_from_right, distance_from_up, distance_from_down]
        # List of potential commands, in the same order as the distances list
        direction = ['left', 'right', 'up', 'down']
        # Return the command that corresponds to the side with the least distance to our door
        return "MOVE " + direction[distances.index(min(distances))]