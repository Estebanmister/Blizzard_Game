# enemy.py
# Esteban, Richard, Utkarsh, Sam
# June 19, 2022
from Classes.collisionentity import CollisionEntity
from math import sin, cos, radians


class Enemy(CollisionEntity):
    def __init__(self, coord, sprite, index=0, args=()):
        """
        Creates an enemy entity, it will kill the player once it enters its line of sight

        :param coord: (tuple) X and Y coordinates in tiles, in form of (x,y)
        :param sprite: (Surface) Pygame image to display for a wall entity
        :param index: (Integer) How many wall entities were already created
        :param args: (List of any) Argument for enemies: Range of sight, starting angle of sight,
                                    range of sight (up and down), speed of turning (can be negative or float)
        """
        CollisionEntity.__init__(self, coord, sprite, index, args=args)
        self.range_of_sight = int(args[0])
        self.angle_of_sight = int(args[1])
        self.start_angle = int(args[1])
        self.sight = int(args[2])
        self.speed_of_turn = float(args[3])
        self.hit = False
        self.stopped_at = self.range_of_sight

    def update(self):
        """
        Check the line of sight, the line of sight is defined in self.range_of_sight,
         self.angle_of_sight, self.start_angle and self.speed_of_turn
        :return:
        """
        all_entities = self.scene.get_all_entities()
        # Comonents of the direction vector
        compx = sin(radians(self.angle_of_sight))
        compy = cos(radians(self.angle_of_sight))
        self.hit = False
        stop = False
        for s in range(self.range_of_sight):
            # Parametric equations of the line of sight
            x = s * compx + self.coord[0]
            y = s * compy + self.coord[1]
            if stop:
                # This is true when we hit a wall
                break
            # Last coordinate we stopped at, used on the frontend to draw a line
            self.stopped_at = s
            for entity in all_entities:
                # If any of the entities are closer than 0.5 to our line of sight, then
                if abs(entity.coord[0] - x) < 0.5 and abs(entity.coord[1] - y) < 0.5:
                    # We check if its a wall
                    if "CollisionEntity" in entity.ID:
                        # In which case the line stops here
                        stop = True
                        break
                    elif "Player" in entity.ID:
                        # If its a player, then we kill
                        self.hit = True
                        entity.stats.set_alive(False)
                        print("PLAYER HIT!")
            # At the end we rotate the angle of sight, Static enemies have a speed of 0
            self.angle_of_sight += self.speed_of_turn
            # check if the angle is outside of our boundary,
            # which goes self.sight angles up or down from self.start_angle
            if self.angle_of_sight > self.start_angle + self.sight or self.angle_of_sight < self.start_angle - self.sight:
                # If we are outside of boundaries, then start turning back
                self.speed_of_turn = -self.speed_of_turn

"""
        for i in range(self.range_of_sight):
            for entity in all_entities:
                localcoords = (self.coord[0] - entity.coord[0], self.coord[1] - entity.coord[1])
                if localcoords[0] - i*sin(radians(self.angle_of_sight)) > 0.5 and localcoords[1] - i*cos(radians(self.angle_of_sight)) > 0.5:
                    if 'Player' in entity.ID:
                        print("Interacted with " + entity.ID)
                        print("At " + str(entity.coord))
                        entity.interact()
                        self.hit = True

        for entity in all_entities:
            localcoords = (self.coord[0] - entity.coord[0], self.coord[1] - entity.coord[1])
            if abs((localcoords[0] * m) - localcoords[1]) < 0.5:
                if self.angle_of_sight > 180 and self.angle_of_sight < 270:
                    if 'Player' in entity.ID:
                        print("Interacted with " + entity.ID)
                        print("At " + str(entity.coord))
                        entity.interact()
                        self.hit = True
                else:
                    if localcoords[0] < 0:
                        if 'Player' in entity.ID:
                            print("Interacted with " + entity.ID)
                            print("At " + str(entity.coord))
                            entity.interact()
                            self.hit = True
        """