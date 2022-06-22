class Entity:
    def __init__(self, coord, sprite, index=0, args=()):
        """
        Base entity class that all game objects inherit from
        :param index: (Integer) How many of these same entities were already created
        :param coord: (List of Integers) X and Y coordinates in tiles
        :param sprite: (Surface) Pygame image to display this entity
        :param args: (List of any) Not used in base entity, but may have different functionalities on different subclasses
        """
        assert len(coord) == 2
        self.coord = coord
        # From the class type, take the class name, separate subclasses and take the last one to generate the ID
        self.ID = str(self.__class__).split("'")[1].split('.')[-1] + str(index)
        self.sprite = sprite
        # Parent scene
        self.scene = None
        # Base entity is not interactive
        self.interactable = False

    def change_ID(self, index):
        """
        Regenerate the ID according to the amount of entities already present in the scene
        :param index: How many of this type of entity are present
        :return:
        """
        self.ID = str(self.__class__).split("'")[1].split('.')[-1] + str(index)

    def assign(self, scene):
        """
        Assign a scene object as the parent to this entity, this is done during loading
        """
        self.scene = scene

    def update(self):
        """
        Placeholder on base Entity, used in other subclass entities to perform automatic actions
        """
        pass

    def interact(self):
        """
        Called when a player entity interacts with the object, only called if self.interactable is set to True
        :return:
        """
        #print("Interacted with " + self.ID)