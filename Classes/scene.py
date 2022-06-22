# scene.py
# Esteban, Richard, Utkarsh, Sam
# June 7, 2022
from Classes.collisionentity import CollisionEntity


class Scene:
    def __init__(self, ID, length, width, background_image, linked_rooms=None, music=None):
        """
        Create a Scene object. Add entities to the list with append_entity and remove_entity

        :param length: (integer) Length of the room in tiles
        :param width: (integer) Width of the room in tiles
        :param background_image: (pygame.Surface) Image data for the background
        :param linked_rooms: (Dictionary, {'up':None, 'down':None, 'left':None, 'right':None}) Other Scene entities that the room links to from each side
        :param music: (Sound) Sound data to play once the scene becomes active, defaults to None
        """
        self.ID = ID
        self.background_image = background_image
        self.music = music
        # Dictionaries are mutable, so they shouldn't be used as default parameters
        if linked_rooms is None or type(linked_rooms) != dict:
            # None means no linked scenes
            self.linked_rooms = {'up': None, 'down': None, 'left': None, 'right': None}
        else:
            self.linked_rooms = linked_rooms

        self.__entities = []
        self.length = length
        self.width = width

        # Store the illegal coordinates for the scene
        self.__illegal_coordinates = []

    def get_all_entities(self):
        """
        Get all entities present in the scene
        :return: list of Entity objects
        """
        return self.__entities

    def get_entity(self, ID):
        """
        Search an entity by their ID and return it
        :param ID: (String) ID to search for
        :return: (Entity) or False on fail
        """
        for entity in self.__entities:
            if entity.ID.lower() == ID.lower():
                return entity
        return False

    def append_entity(self, entity):
        """
        Append an entity object, ID DOES NOT MATTER, IT IS REASSIGNED!
        :param entity: (Entity) Entity object to append
        """
        if entity.coord[0] > self.length or entity.coord[0] < 0 or entity.coord[1] > self.width or entity.coord[1] < 0:
            raise Exception("Illegal coordinates, map too small or coordinates below 0")

        # If entity is CollisionEntity, append that coordinate to illegal coordinates
        # Use isinstance() to check if entity is an instance of the class CollisionEntity
        if isinstance(entity, CollisionEntity):
            self.__illegal_coordinates.append(entity.get_coord())
        # Create a filter that iterates through self.__entities,
        # applies the condition of the type being equal to our entity
        # convert that filter into a list and find the length of that list
        # to see how many of the same entity we already have
        entity.change_ID(len(list(filter(lambda x: type(x) == type(entity), self.__entities))))
        entity.assign(self)
        self.__entities.append(entity)

    def remove_entity(self, ID):
        """
        Search and remove an entity by their ID
        :param ID: (string) ID to remove
        :return: (Bool) False on fail, True on success
        """
        for entity in self.__entities:
            if entity.ID == ID:
                self.__entities.remove(entity)
                return True
        return False

    def update_all(self):
        """
        Calls the update function of every entity within the scene
        """
        for entity in self.__entities:
            entity.update()

    def check_coordinate(self, coord: tuple):
        """
        Checks if a coordinate is illegal for access
        :param coord: A tuple, (x,y)
        :return: True if the coordinate is passable, False if not
        """

        # Check if coord is in list of illegal coordinates
        if list(coord) in self.__illegal_coordinates:
            return False
        if coord[0] >= self.length:
            return False
        if coord[1] >= self.width:
            return False
        if coord[0] < 0:
            return False
        if coord[1] < 0:
            return False
        for i in self.__illegal_coordinates:
            if abs(coord[0]-i[0])<0.84 and abs(coord[1]-i[1])<0.84:
                return False

        return True
