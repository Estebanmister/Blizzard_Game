from Classes.consumables import WaterBottle, CannedFood
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
        self.x_vel = 0
        self.y_vel = 0
        for arg in args:
            self.direction_sprites.append(load(arg))

    def interact(self):
        print("Ouch!!")

    @staticmethod
    def deceleration(value):
        """
        :param value: A float value
        :return: value-0.008
        """
        if value-0.003>0:
            return value-0.001
        if value+0.003<0:
            return value+0.001
        return 0

    def move(self, direction):
        """
        Moves the player, checks for illegal coordinates, and updates self.sprite according to the movement made
        :param direction: (String) The direction 'up', 'down', 'left', 'right', "up-left", "up-right", "down-left",
        "down-right"
        """
        # Code logic:
        # The player will start with a velocity of 0 and acceleration of 0.001, if combined velocity of x and y
        # movement is less than 0.03.
        # If more than that, then the acceleration will decrease to 0.0003.
        # Pressing no key down will set both x and y movement to 0.
        # Moving in the opposite direction will first stop the player movement instantly, then move in that direction.
        # Player's velocity will be reset in that axis only if it changes direction in one axis.
        # For example. If the player changes from down-right to down-left, the x-velocity will be reset,
        # y-velocity remains unchanged.
        previous = self.coord

        # Default acceleration
        acceleration = 0.0003

        # Start up acceleration
        if abs(self.x_vel)+abs(self.y_vel)<0.03:
            acceleration=0.0013

        # Stop the player movement if no key down
        if direction == "none":
            self.x_vel=self.deceleration(self.x_vel)
            self.y_vel =self.deceleration(self.y_vel)
        # Each direction is interpreted by natural language
        if direction == "up":

            # If player is already moving in the opposite direction, stop that.
            if self.y_vel<0:
                self.y_vel=0

            # Stop player's movement on the other axis.
            self.x_vel=0
            # Increase the acceleration in the right direction
            self.y_vel += acceleration
            if any(self.direction_sprites):
                # If direction sprites are specified, then select the correct one to display
                self.sprite = self.direction_sprites[1]
        elif direction == "down":
            if self.y_vel>0:
                self.y_vel=0
            self.x_vel = 0
            self.y_vel -= acceleration
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[0]
        elif direction == "left":
            if self.x_vel>0:
                self.x_vel=0
            self.y_vel=0
            self.x_vel -= acceleration
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "right":
            if self.x_vel<0:
                self.x_vel=0
            self.y_vel=0
            self.x_vel += acceleration
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]
        elif direction == "up-left":
            if self.x_vel>0:
                self.x_vel=0
            if self.y_vel>0:
                self.y_vel=0
            self.x_vel -= (acceleration / 2)
            self.y_vel -= (acceleration / 2)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "up-right":
            if self.x_vel<0:
                self.x_vel=0
            if self.y_vel>0:
                self.y_vel=0
            self.x_vel += (acceleration / 2)
            self.y_vel -= (acceleration / 2)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]
        elif direction == "down-left":
            if self.x_vel>0:
                self.x_vel=0
            if self.y_vel<0:
                self.y_vel=0
            self.x_vel -= (acceleration / 2)
            self.y_vel += (acceleration / 2)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[2]
        elif direction == "down-right":
            if self.x_vel<0:
                self.x_vel=0
            if self.y_vel<0:
                self.y_vel=0
            self.x_vel += (acceleration / 2)
            self.y_vel += (acceleration / 2)
            if any(self.direction_sprites):
                self.sprite = self.direction_sprites[3]

        # Set a maximum speed
        if self.x_vel > 0.22:
            self.x_vel = 0.22
        if self.y_vel > 0.22:
            self.y_vel = 0.22
        if self.x_vel < -0.22:
            self.x_vel=-0.22
        if self.y_vel <-0.22:
            self.y_vel=-0.22

        # Move the player
        self.coord = (self.coord[0] + self.x_vel, self.coord[1] + self.y_vel)

        # If moves into illegal coordinate, do not move
        if not self.scene.check_coordinate(self.coord):
            self.coord = previous

    def interact_with(self):
        """
        Call everytime the player clicks the interact button, they will interact with the closest entity
        todo: make it so it interacts with the entity IN FRONT of the player instead
        """
        RANGE = 2
        closest_entity = None
        # For every entity
        for entity in self.scene.get_all_entities():
            # If this is ourselves, skip
            if entity == self:
                continue
            # If this entity is not interactive, don't bother doing any calculations
            if entity.interactable:
                # Calculate the distance to the entity using the pythagorean theorem
                distance = sqrt((entity.coord[0] - self.coord[0]) ** 2 + (entity.coord[1] - self.coord[1]) ** 2)
                # If the entity is within range
                if distance < RANGE:
                    # But if we already have another entity in range
                    if closest_entity:
                        # Check if this new entity is closer than the old entity
                        if distance < sqrt((closest_entity.coord[0] - self.coord[0]) ** 2 + (
                                closest_entity.coord[1] - self.coord[1]) ** 2):
                            # If it is so, then we have a new closest entity
                            closest_entity = entity
                    else:
                        closest_entity = entity
        if closest_entity:
            # If we ended up with a closest entity, then interact with it
            # and return any commands it might have for the frontend
            if isinstance(closest_entity,WaterBottle):
                self.stats.add_hunger(closest_entity.drink())
            elif isinstance(closest_entity,CannedFood):
                self.stats.add_hunger(closest_entity.eat())
            return closest_entity.interact()
        else:
            # Otherwise return None
            return None
