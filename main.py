# import all prerequisite libraries
import pygame
from data_loader import *
from Classes.player_stats import *
from math import sin, cos, radians
import math
from Classes.visuals import *
from Classes.sounds import *

# define some variables for use later such as, what FPS game will run at
# basic colour tuples, set desired width and height game will run at
FPS = 120
black = (0, 0, 0)
white = (255, 255, 255)
width, height = 700, 700
gamePaused = False
temp_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)
text_counter = 0

# calculate the sprite scale using screen -- calculation is done in Main()
scY = 0
scX = 0
scale = 0
# imports from other files, scene, player object
currentDungeon = load_dungeon('World/Overworld')
currentScene = currentDungeon.head
dungeonDirectory = 'World/Overworld'
player_obj = currentScene.get_entity('Player0')
player_stats = PlayerStats()
player_obj.stats = player_stats
# set our screen size
pygame.init()
screen = pygame.display.set_mode((width, height))
# load assets
pygame.display.set_icon(pygame.image.load("Assets/Sprites/playerdown.png"))
pygame.font.init()

font = pygame.font.SysFont('arial', 40)
Visual = Visuals(width, height, player_stats.get_stats())
tutorialMenu = pygame.image.load("Assets/Sprites/BLIZZARD_TUTORIAL.png")
tutorialPassed = False
Sound = Sounds()
Sound.play_music("menu.wav")

last_interaction_counter = 0


##########################################################################
# Getting into the actual code now, after the prerequisite set ups.

def drawText(textToFill, x, y):
    """
    method to write text on the screen,
    param textToFill: (string) What do we want to type
    param x,y: (integers) What location on Pygame X,Y grid do we want this text
    """
    global text_counter

    if Visual.draw_label is not None:
        Visual.draw_label.kill()

    Visual.draw_label = pygame_gui.elements.UITextBox(html_text=textToFill, relative_rect=pygame.Rect((x, y), (
        Visual.label_data["width"], Visual.label_data["height"])), manager=Visual.ui_manager,
                                                      container=Visual.game_container)
    Visual.draw_label.show()


class UI:
    """
    This class will handle all methods relating to the UI the player will see.
    On screen elements, showing and hiding them, will all be trigged from the methods here.
    The idea is, the UI is seen as a card almost, which can be brought in or out of view as needed.
    """

    def __init__(self):
        pass

    def toggleMenu(self):
        """
        toggles if the menu is visible or not
        """
        global gamePaused
        if gamePaused:
            gamePaused = False
        else:
            gamePaused = True
            self.clearText()
            self.showMenu()

    def showMenu(self):
        """
        if menu is visible, draw the menu on the display
        """
        if gamePaused:
            self.clearText()
            screen.fill(black)
            drawText("MENU", font, white, width / 2, 0)

    @staticmethod
    def quickText(textToFill, delay=300):
        """
        quickText is the same exact method as drawText, it even invokes drawText
        It was simply created as a convenience method when we want to print something
        in exact same spot using preset font, colour, etc. settings.
        param delay: (integer) What is the delay to be used in conjuction with the text
        """
        global text_counter
        text_counter = delay
        drawText(textToFill, 0, (height / 4) * 3)


# With the UI() class complete, we can spawn its object, gameUI.
gameUI = UI()


class PlayerStatsController:
    """
    This class is responsible for acting like a manager to our player's stats.
    If we want to change our player's stats or access them, we can do so
    with the methods here
    """

    def __init__(self):
        pass

    @staticmethod
    def reduceStats():
        """
        We simply call this method to reduce player's stats when player makes a move
        to simulate the feeling of a survival game.
        """
        player_stats.reduce_hunger(0.0002, 0.002)
        player_stats.reduce_thirst(0.0003, 0.004)

        if 'demo' in currentScene.ID:
            # however, if the player is moving along a pleasant scene, player regains sanity.
            # the logic is, staying in a creepy/dark scene for too long will make the player lose their sanity.
            player_stats.add_sanity(0.01)
        else:
            player_stats.reduce_sanity(0.005, 0.01)


# Create object of parent class
managePlayer = PlayerStatsController()


def player_input(keys_input):
    """
    This function is in charge of all things related to Pygame Key inputs
    Param keys_pressed: (module) What keys are currently being pressed (checked each frame)
    We take action accordingly if any keys are being pressed that may be actionable.
    """
    global currentScene
    global player_obj
    global scX, scY
    global scale
    global gamePaused
    global temp_surface
    global last_interaction_counter
    global dungeonDirectory
    global tutorialPassed

    if keys_input[pygame.K_w] or keys_input[pygame.K_a] or keys_input[pygame.K_s] or keys_input[pygame.K_d]:
        # if the game is not paused and the user presses W,A,S,D or any of the 4 in combination, call player movement.
        if not gamePaused:
            if keys_input[pygame.K_w] and keys_input[pygame.K_a]:
                player_obj.move("up-left")
                managePlayer.reduceStats()
            elif keys_input[pygame.K_w] and keys_input[pygame.K_d]:
                player_obj.move("up-right")
                managePlayer.reduceStats()
            elif keys_input[pygame.K_s] and keys_input[pygame.K_a]:
                player_obj.move("down-left")
                managePlayer.reduceStats()
            elif keys_input[pygame.K_s] and keys_input[pygame.K_d]:
                player_obj.move("down-right")
                managePlayer.reduceStats()
            elif keys_input[pygame.K_w]:
                player_obj.move('down')
                managePlayer.reduceStats()
            elif keys_input[pygame.K_a]:
                player_obj.move('left')
                managePlayer.reduceStats()
            elif keys_input[pygame.K_s]:
                player_obj.move('up')
                managePlayer.reduceStats()
            elif keys_input[pygame.K_d]:
                player_obj.move('right')
                managePlayer.reduceStats()
    else:
        player_obj.move("none")
    if keys_input[pygame.K_f]:
        print("F is pressed")
        tutorialPassed = True
    if keys_input[pygame.K_ESCAPE]:
        # If the escape key is pressed, toggle opening the Menu and Pausing the game
        # with use of the gameUI object.
        if not gamePaused:
            gamePaused = True
            pygame.time.delay(650)
        else:
            gamePaused = False
            pygame.time.delay(650)

    if keys_input[pygame.K_e] and last_interaction_counter == 0:
        '''This is the most complex interaction,
        When 'E' is pressed, capture the return command from the nearest
        interactable entity, examples: MOVE up, SAY xyz, MOVE down...
        If the nearest interactable entity is a door, it may command: MOVE left or MOVE up
        if the nearest entity is a note, it may command: SAY the faded note reads 'You are doomed!'
        in any case, capture what the command of the nearest entity is, (could be None if nothing nearby too)
        and respond with the appropriate method.
        '''
        last_interaction_counter = 20
        command_to_do = player_obj.interact_with()
        print(command_to_do)
        if command_to_do is None:
            # as said above, if nothing nearby to interact with, let user know with a textbox thanks to gameUI method.
            gameUI.quickText("There's nothing to interact with here", delay=100)
        if command_to_do is not None:
            # if there is a command to do, respond appropriately
            if command_to_do.split(' ')[0] == 'DISPLAY':
                # if certain text is to be shown: DISPLAY 'xyz abc', then format the text to display appropriately
                # such as stripping out the DISPLAY in DISPLAY 'xyz abc', so player only sees 'xyz abc'
                gameUI.quickText(' '.join(command_to_do.split(' ')[1:]))
            if command_to_do.split(' ')[0] == 'EXIT':
                newdungeon = command_to_do.split(' ')[1]
                dungeonDirectory = newdungeon
                print("MOVING TO " + newdungeon)
                currentDungeon = load_dungeon(newdungeon)
                currentScene = currentDungeon.head
                if currentScene.music is not None and currentScene.music != '':
                    Sound.play_music(currentScene.music)
                player_obj = currentScene.get_entity('Player0')
                player_obj.stats = player_stats

                '''sCX and scY are a pair, meant to represent the length of a tile.
                if we are in a 5x5 room, tiles can be bigger than in a 20x20 room
                where we'd obviously need to make them smaller to fit the same display size.
                These are important to our rendering process.
                '''
                scX = width / currentScene.width
                scY = height / currentScene.length
                scale = min(scX, scY)

                # tempsurf is for optimization, it was observed putting too many sprites on the screen
                # was a big loss for performance. This way, we put all sprites onto tempsurf, and simply
                # draw tempsurf on the screen at the end. 
                temp_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)
                for entity in currentScene.get_all_entities():
                    # the tempsurf optimization is specifically for walls, we put the walls inside it
                    # and draw tempsurf at the end, aka all walls are drawn in one swift stroke.
                    if "CollisionEntity" in entity.ID:
                        # if entity is a wall, don't draw it directly, put it onto tempsurf
                        coordinate_draw = entity.coord
                        sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                        if currentScene.width > currentScene.length:
                            temp_surface.blit(sprite, (
                                ((coordinate_draw[0] * scale + (width - (scX * currentScene.length)) / 2),
                                 coordinate_draw[1] * scale)))
                        if currentScene.length > currentScene.width:
                            temp_surface.blit(sprite, (
                                (coordinate_draw[0] * scale,
                                 (coordinate_draw[1] * scale + (height - (scY * currentScene.width)) / 2))))
                        if currentScene.length == currentScene.width:
                            temp_surface.blit(sprite,
                                              (coordinate_draw[0] * scale, coordinate_draw[1] * scale))
            if command_to_do.split(' ')[0] == 'MOVE':
                # if the interaction command is MOVE xyz, we move the player to a different room
                # this demonstrates complex coding because this deals with linked lists.
                print(command_to_do.split(' ')[1])
                middle_scene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                if middle_scene is not None:
                    currentScene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                    if currentScene.music is not None and currentScene.music != '':
                        # if the scene has a music track associated with it, play it
                        Sound.play_music(currentScene.music)
                    player_obj = currentScene.get_entity('Player0')
                    player_obj.stats = player_stats
                    print(currentScene.ID)

                    # When we are in a new scene, we need to recalculate what the tile sizes should be
                    # in the new scene
                    scX = width / currentScene.width
                    scY = height / currentScene.length
                    scale = min(scX, scY)
                    temp_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)

                    # Cache all the walls inside a surface
                    for entity in currentScene.get_all_entities():
                        if "CollisionEntity" in entity.ID:
                            coordinate_draw = entity.coord
                            sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                            if currentScene.width > currentScene.length:
                                temp_surface.blit(sprite, (
                                    ((coordinate_draw[0] * scale + (width - (scX * currentScene.length)) / 2),
                                     coordinate_draw[1] * scale)))
                            if currentScene.length > currentScene.width:
                                temp_surface.blit(sprite, (
                                    (coordinate_draw[0] * scale,
                                     (coordinate_draw[1] * scale + (height - (scY * currentScene.width)) / 2))))
                            if currentScene.length == currentScene.width:
                                temp_surface.blit(sprite,
                                                  (coordinate_draw[0] * scale, coordinate_draw[1] * scale))

        pygame.time.delay(100)
    elif keys_input[pygame.K_e]:
        last_interaction_counter -= 1


def Main():
    """
    With all that set up, we are ready for the main() loop. This houses the while loop
    which will run through the game's calculations, priority of rendering and events each frame.
    This really is where it all comes together.
    """
    # import some prerequisite values as global variables
    run = True
    global keys_pressed
    global currentDungeon
    global currentScene
    global player_obj
    global scY, scX
    global scale
    global gamePaused
    global clock
    global text_counter
    global temp_surface
    global tutorialMenu
    global tutorialPassed

    clock = pygame.time.Clock()
    scX = width / currentScene.width
    scY = height / currentScene.length
    scale = scX

    # the command which sets the title of our window to Blizzard, our game name.
    pygame.display.set_caption("Blizzard")

    # Cache all the walls inside a surface
    for entity in currentScene.get_all_entities():
        if "CollisionEntity" in entity.ID:
            coordinate_draw = entity.coord
            sprite = pygame.transform.scale(entity.sprite, (scale, scale))
            if currentScene.width > currentScene.length:
                temp_surface.blit(sprite, (
                    ((coordinate_draw[0] * scale + (width - (scX * currentScene.length)) / 2),
                     coordinate_draw[1] * scale)))
            if currentScene.length > currentScene.width:
                temp_surface.blit(sprite, (
                    (coordinate_draw[0] * scale,
                     (coordinate_draw[1] * scale + (height - (scY * currentScene.width)) / 2))))
            if currentScene.length == currentScene.width:
                temp_surface.blit(sprite,
                                  (coordinate_draw[0] * scale, coordinate_draw[1] * scale))

    while run:
        '''
        Here we are, the while loop which goes through everything possible each frame.
        Checking for input keys each frame, only running the game at the set FPS (120 in our case)
        '''
        if Visual.screen == "title":
            if not tutorialPassed:
                keys_pressed = pygame.key.get_pressed()
                player_input(keys_pressed)
            # only run the game 120 frames a second to prevent physics from going haywire or game running too fast
            clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                    if event.ui_element == Visual.quit_button:
                        pygame.quit()
                        quit()

                    elif event.ui_element == Visual.continue_button:
                        Visual.screen = "game"
                        Visual.title_container.hide()
                        Visual.player_stats_textbox.show()
                        if currentScene.music is not None and currentScene.music != '':
                            Sound.play_music(currentScene.music)
                        pass

                    elif event.ui_element == Visual.newgame_button:
                        Visual.screen = "game"
                        Visual.title_container.hide()
                        Visual.player_stats_textbox.show()
                        if currentScene.music is not None and currentScene.music != '':
                            Sound.play_music(currentScene.music)
                        pass

                Visual.ui_manager.process_events(event)

            draw_display(currentScene, temp_surface)
            pygame.display.update()
        elif Visual.screen == "game":
            if not player_obj.stats.check_alive():
                # If the player has died, here we run the logic to Respawn them.
                print("MOVING TO " + dungeonDirectory)

                # dungeonDirectory will be used to invoke the linked list and set the scene to where
                # the respawn point is.
                currentDungeon = load_dungeon(dungeonDirectory)
                currentScene = currentDungeon.head

                # -----whenever a scene changes we must call some code again to make sure everything lines up.
                if currentScene.music is not None and currentScene.music != '':
                    Sound.play_music(currentScene.music)
                player_obj = currentScene.get_entity('Player0')
                player_obj.stats = player_stats
                scX = width / currentScene.width
                scY = height / currentScene.length
                scale = min(scX, scY)
                temp_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)
                for entity in currentScene.get_all_entities():
                    if "CollisionEntity" in entity.ID:
                        coordinate_draw = entity.coord
                        sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                        if currentScene.width > currentScene.length:
                            temp_surface.blit(sprite, (
                                ((coordinate_draw[0] * scale + (width - (scX * currentScene.length)) / 2),
                                 coordinate_draw[1] * scale)))
                        if currentScene.length > currentScene.width:
                            temp_surface.blit(sprite, (
                                (coordinate_draw[0] * scale,
                                 (coordinate_draw[1] * scale + (height - (scY * currentScene.width)) / 2))))
                        if currentScene.length == currentScene.width:
                            temp_surface.blit(sprite,
                                              (coordinate_draw[0] * scale, coordinate_draw[1] * scale))
                # -----scene change code ends above
            clock.tick(FPS)
            # keys_pressed is a pygame module, this invokes the complex pygame's get_pressed to get a list of all keys pressed in a certain frame.
            keys_pressed = pygame.key.get_pressed()  # put this here since player_input wont work if the var isn't defined.
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # if pygame gets a QUIT event (player clicking quit), close the game by setting run to false hence breaking the loop.
                    run = False

            # call the player_input function each frame, with the parameter keys_pressed
            player_input(keys_pressed)

            # now we set the priority of our elements in the UI
            if gamePaused:
                # if game is paused, display the menu on this frame.
                gameUI.showMenu()
            else:
                # if game is not paused, draw the scene, and update all entities as usual
                draw_display(currentScene, temp_surface)
                currentScene.update_all()
            if text_counter == 0 and Visual.draw_label:
                Visual.draw_label.hide()
            else:
                text_counter -= 1

            # call pygame display update, else we don't actually see any changes in the screen
            pygame.display.update()


# end of the main() function above, once main() is done running, that means the program has ended.


def rotate_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def draw_display(scene, tempsurf):
    '''
    This is the function which will deterine what is being drawed to the display that particular frame
    param Tempsurf: (surface) This is a complex data type, this is a pygame surface which will 
    be holding all our collision entities so they can be displayed as one, which leads to less performance loss
    '''
    global player_obj
    global tutorialMenu
    global tutorialPassed
    tempsurf = tempsurf

    # fill screen with black to remove all leftovers from past frames rendered
    screen.fill(black)

    Visual.ui_manager.update(clock.tick(FPS) / 1000)  # updates information on the ui elements
    if not tutorialPassed:
        screen.blit(tutorialMenu, (0, 0))
    else:
        if Visual.screen == "game":
            Visual.update_stat_display(player_stats.get_stats())

            # Y-axis is width, X axis is length
            # first moves +right -left, second moves +down -up.
            if scene.width > scene.length:
                # Vertical rooms
                screen.blit(pygame.transform.scale(scene.background_image, (scene.length * scX, scene.width * scX)),
                            ((width - (scX * scene.length)) / 2, 0))
            if scene.length > scene.width:
                # Horizontal rooms
                screen.blit(pygame.transform.scale(scene.background_image, (scene.length * scY, scene.width * scY)),
                            (0, (height - (scY * scene.width)) / 2))
            if scene.length == scene.width:
                screen.blit(pygame.transform.scale(scene.background_image, (scene.length * scX, scene.width * scY)),
                            (0, 0))
            # last ones below are (0,0) as a fallback
            # screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),(0, 0)) 
            for entity in scene.get_all_entities():
                angle = 0
                coordinate_draw = entity.coord
                if 'enemy' in entity.ID.lower():
                    angle = entity.angle_of_sight
                    compx = sin(radians(entity.angle_of_sight))
                    compy = cos(radians(entity.angle_of_sight))
                    for s in range(entity.stopped_at + 1):
                        x = (s * compx + entity.coord[0]) * (scale + (width - (scX * scene.length)) / 2)
                        y = (s * compy + entity.coord[1]) * (scale + (height - (scY * scene.width)) / 2)
                        if entity.hit:
                            pygame.draw.circle(screen, (255, 0, 0), (x, y), 3)
                        elif s:
                            pygame.draw.circle(screen, white, (x, y), 3)
                if 'CollisionEntity' not in entity.ID:
                    sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                    if scene.width > scene.length:
                        screen.blit(rotate_center(sprite, angle), (
                            ((coordinate_draw[0] * scale + (width - (scX * scene.length)) / 2),
                             coordinate_draw[1] * scale)))
                    if scene.length > scene.width:
                        screen.blit(rotate_center(sprite, angle), (
                            (coordinate_draw[0] * scale,
                             (coordinate_draw[1] * scale + (height - (scY * scene.width)) / 2))))
                    if scene.length == scene.width:
                        screen.blit(rotate_center(sprite, angle),
                                    (coordinate_draw[0] * scale, coordinate_draw[1] * scale))

            screen.blit(tempsurf, (0, 0))
        Visual.ui_manager.draw_ui(screen)  # displays the ui elements


# As everything is attached to Main() in some way or another, the nice thing is, we only need to run Main() and the program is good to go

Main()
