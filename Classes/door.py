from Classes.collisionentity import CollisionEntity


class Door(CollisionEntity):
    def __init__(self, coord, sprite, index=0, args=()):
        CollisionEntity.__init__(self, coord, sprite, index, args)
        self.interactable = True

    def interact(self):
        """
        Using the width and height of the scene, calculate which side of the scene the door is closest to
        :return: String, "MOVE " + 'up' or 'down' or 'left' or 'right'
        """
        width = self.scene.width
        length = self.scene.length
        distance_from_left = abs(self.coord[0] - 0)
        distance_from_right = abs(self.coord[0] - width)
        distance_from_up = abs(self.coord[1] - 0)
        distance_from_down = abs(self.coord[1] - length)
        distances = [distance_from_left, distance_from_right, distance_from_up, distance_from_down]
        direction = ['left', 'right', 'up', 'down']

        return "MOVE " + direction[distances.index(min(distances))]