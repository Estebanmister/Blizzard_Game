# notes.py
# Esteban, Richard, Utkarsh, Sam
# June 19, 2022
from Classes.entity import Entity

class Notes(Entity):

    def __init__(self, coord, sprite, index=0, args=()):
        # The notes class displays notes to the front end
        Entity.__init__(self, coord, sprite, index, args)
        self.interactable = True
        self.current_line = args[0]


    def interact(self):
        """
        :return: (String) A instruction for the frontend containing the text to display.
        """
        return f"DISPLAY {self.current_line}"


