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

    def get_entity(self, ID):
        """
        Search an entity by their ID and return it
        :param ID: (String) ID to search for
        :return: (Entity) or False on fail
        """
        for entity in self.__entities:
            if entity.ID == ID:
                return entity
        return False

    def append_entity(self, entity):
        """
        Append an entity object, ID DOES NOT MATTER, IT IS REASSIGNED!
        :param entity: (Entity) Entity object to append
        """
        # Create a filter that iterates through self.__entities,
        # applies the condition of the type being equal to our entity
        # convert that filter into a list and find the length of that list
        # to see how many of the same entity we already have
        entity.change_ID(len(list(filter(lambda x: type(x) == type(entity), self.__entities))))
        if entity.coord[0] > self.length or entity.coord[0] < 0 or entity.coord[1] > self.width or entity.coord[1] < 0:
            raise Exception("Illegal coordinates, map too small or coordinates below 0")
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
