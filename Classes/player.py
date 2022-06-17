from Classes.entity import Entity
from math import sqrt
from pygame.image import load

class Player(Entity):
    def __init__(self, coord, sprite, index=0, args=()):
        """
        Player Class,
        :param coord: Tuple, coordinates
        :param sprite: Sprite to display by default
        :param args: (List of pygame.surfaces) IMPORTANT! The arguments for this class represent the 4 sprites displayed with each motion
        """
        Entity.__init__(self, coord, sprite, index, args)
        self.direction_sprites = []
        for arg in args:
            self.direction_sprites.append(load(arg))

    def move(self, direction):
        """
        Moves the player, checks for illegal coordinates, and updates self.sprite according to the movement made
        :param direction: (String) The direction 'up', 'down', 'left', 'right'
        :return:
        """
        previous = self.coord
        if direction == "up":
            self.coord = (self.coord[0], self.coord[1] + 1)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[1]
        elif direction == "down":
            self.coord = (self.coord[0], self.coord[1] - 1)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[0]
        elif direction == "left":
            self.coord = (self.coord[0] - 1, self.coord[1])
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "right":
            self.coord = (self.coord[0] + 1, self.coord[1])
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]
        if not self.scene.check_coordinate(self.coord):
            self.coord = previous

    def interact_with(self):
        """
        Call everytime the player clicks the interact button, they will interact with the closest entity
        todo: make it so it interacts with the entity IN FRONT of the player instead
        """
        RANGE = 4
        closest_entity = None
        for entity in self.scene.get_all_entities():
            if entity == self:
                continue
            distance = sqrt((entity.coord[0] - self.coord[0])**2 + (entity.coord[1] - self.coord[1])**2)
            if distance < RANGE:
                if closest_entity:
                    if distance < sqrt((closest_entity.coord[0] - self.coord[0])**2 + (closest_entity.coord[1] - self.coord[1])**2):
                        if entity.interactable:
                            closest_entity = entity
                else:
                    if entity.interactable:
                        closest_entity = entity
        if closest_entity:
            return closest_entity.interact()
        else:
            return None