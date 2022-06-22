from Classes.entity import Entity
import pygame
notes_index = 0
DEBUG = True
if DEBUG:
    pygame.font.init()
class Notes(Entity):
    # A class level variable to keep track
    current_line = 0

    def __init__(self, coord, sprite, index=0, args=()):
        global notes_index
        if DEBUG:
            notes_file = open("Entities/Notes.txt", "r")
            sprite.blit(pygame.font.SysFont('Arial', 175).render(str(len(notes_file.readlines()) - 1 - notes_index), True, (255, 0, 0)), (25,25))
            notes_file.close()
        Entity.__init__(self, coord, sprite, index, args)
        self.interactable = True
        self.current_line = notes_index
        notes_index += 1


    def interact(self):
        """
        :return: (String) A instruction for the frontend containing the text to display.
        """
        notes_file = open("Entities/Notes.txt", "r")

        # Get the current line
        current_message_list = notes_file.readlines()
        current_message=current_message_list[len(current_message_list) - 1 - self.current_line]

        # Update the counter
        self.update()

        # Remove itself once the message is sent
        self.scene.remove_entity(self.ID)

        return f"DISPLAY {current_message}"


