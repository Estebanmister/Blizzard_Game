from Classes.entity import Entity
from math import sqrt
from pygame.image import load
from Classes.player_stats import *
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
        self.stats = None
        for arg in args:
            self.direction_sprites.append(load(arg))

    def interact(self):
        print("Ouch!!")

    def move(self, direction):
        """
        Moves the player, checks for illegal coordinates, and updates self.sprite according to the movement made
        :param direction: (String) The direction 'up', 'down', 'left', 'right'
        :return:
        """
        previous = self.coord
        # Each direction is interpreted by natural language
        if direction == "up":
            # Move the player
            self.coord = (self.coord[0], self.coord[1] + 0.0333)
            if any(self.direction_sprites):
                # If direction sprites are specificed, then select the correct one to display
                self.sprite = self.direction_sprites[1]
        elif direction == "down":
            self.coord = (self.coord[0], self.coord[1] - 0.0333)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[0]
        elif direction == "left":
            self.coord = (self.coord[0] - 0.0333, self.coord[1])
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "right":
            self.coord = (self.coord[0] + 0.0333, self.coord[1])
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]
        elif direction == "up-left":
            self.coord = (self.coord[0] - 0.01665, self.coord[1]-0.01665)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "up-right":
            self.coord = (self.coord[0] + 0.01665, self.coord[1] - 0.01665)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]
        elif direction == "down-left":
            self.coord = (self.coord[0] - 0.01665, self.coord[1] + 0.01665)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "down-right":
            self.coord = (self.coord[0] + 0.01665, self.coord[1] + 0.01665)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]
        if not self.scene.check_coordinate(self.coord):
            self.coord = previous

    def interact_with(self):
        """
        Call everytime the player clicks the interact button, they will interact with the closest entity
        todo: make it so it interacts with the entity IN FRONT of the player instead
        """
        RANGE = 1
        closest_entity = None
        # For every entity
        for entity in self.scene.get_all_entities():
            # If this is ourselves, skip
            if entity == self:
                continue
            # If this entity is not interactive, don't bother doing any calculations
            if entity.interactable:
                # Calculate the distance to the entity using the pythagorean theorem
                distance = sqrt((entity.coord[0] - self.coord[0])**2 + (entity.coord[1] - self.coord[1])**2)
                # If the entity is within range
                if distance < RANGE:
                    # But if we already have another entity in range
                    if closest_entity:
                        # Check if this new entity is closer than the old entity
                        if distance < sqrt((closest_entity.coord[0] - self.coord[0])**2 + (closest_entity.coord[1] - self.coord[1])**2):
                            # If it is so, then we have a new closest entity
                            closest_entity = entity
                    else:
                        closest_entity = entity
        if closest_entity:
            # If we ended up with a closest entity, then interact with it
            # and return any commands it might have for the frontend
            return closest_entity.interact()
        else:
            # Otherwise return None
            return None