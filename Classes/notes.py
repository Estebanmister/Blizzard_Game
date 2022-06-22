from Classes.entity import Entity

class Notes(Entity):
    # A class level variable to keep track

    def __init__(self, coord, sprite, index=0, args=()):
        Entity.__init__(self, coord, sprite, index, args)
        self.interactable = True
        self.current_line = args[0]


    def interact(self):
        """
        :return: (String) A instruction for the frontend containing the text to display.
        """
        return f"DISPLAY {self.current_line}"


