

class Scene:
    def __init__(self, length, width, background_image, linked_rooms = None, music=None):
        """
        Create a Scene object. Add entities to the list Scene.entities

        :param length: (integer) Length of the room in tiles
        :param width: (integer) Width of the room in tiles
        :param background_image: (Image?) Image data for the background
        :param linked_rooms: (Dictionary, {'up':None, 'down':None, 'left':None, 'right':None}) Other Scene entities that the room links to from each side
        :param music: (Sound) Sound data to play once the scene becomes active, defaults to None
        """
        self.background_image = background_image
        self.music = music
        # Dictionaries are mutable, so they shouldn't be used as default parameters
        if linked_rooms is None or type(linked_rooms) != dict:
            # None means no linked scenes
            self.linked_rooms = {'up':None, 'down':None, 'left':None, 'right':None}
        else:
            self.linked_rooms = linked_rooms

        self.entities = []
        self.length = length
        self.width = width

    def update_all(self):
        """
        Calls the update function of every entity within the scene
        """
        for entity in self.entities:
            entity.update()


