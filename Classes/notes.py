from Classes.entity import Entity


class Notes(Entity):
    # A class level variable to keep track
    current_line = 0

    @classmethod
    def update(cls):
        """
        Update the current_line counter by 1
        """
        cls.current_line += 1

    def __init__(self, coord, sprite, index=0, args=()):
        Entity.__init__(self, coord, sprite, index, args)
        self.interactable = True

    def show_text(self):
        """
        :return: (String) A instruction for the frontend containing the text to display.
        """

        notes_file = open("../Entities/Notes.txt", "r")

        # Get the current line
        current_message_list = notes_file.readlines()
        current_message=current_message_list[self.current_line]

        # Update the counter
        self.update()

        # Remove itself once the message is sent
        self.scene.remove_entity(self.ID)

        return f"DISPLAY {current_message}"


