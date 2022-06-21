import pygame
from data_loader import *
from Classes.player_stats import *
from math import sin, cos, radians
import math
from Classes.visuals import *
from Classes.sounds import *

#define some variables, what FPS game will run at
#basic colour tuples to make writing colours easier
#set desired width and height game will run at later
showtext = False
FPS = 120
black = (0,0,0)
white = (255, 255, 255)
width, height = 700, 700
gamePaused = False
textOnScreen = ''
tempsurf = pygame.Surface((width,height), flags=pygame.SRCALPHA)



#calculate the sprite scale using screen -- calculation is done in Main()
scY = 0
scX = 0
scale = 0
#imports from other files, scene, player object
currentDungeon = load_dungeon('World/Overworld')
currentScene = currentDungeon.head

player_obj = currentScene.get_entity('Player0')
player_stats = PlayerStats()
player_obj.stats = player_stats
#set our screen size
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_icon(pygame.image.load("Assets/Sprites/playerdown.png"))
##########################################################################
pygame.font.init()

font = pygame.font.SysFont('arial',40)
Visual = Visuals(width, height, player_stats.get_stats())
Sound = Sounds()
Sound.play_music("menu.wav")

last_interaction_counter = 0

class UI():
    def __init__(self):
        pass
    def toggleMenu(self):
        global gamePaused
        if gamePaused == True:
            gamePaused = False
        else:
            gamePaused = True
            self.clearText()
            self.showMenu()
            
    def showMenu(self):
        if gamePaused == True:
            self.clearText()
            screen.fill(black)
            self.drawText("MENU",font,white,width/2,0)
    #DrawText and QuickText are in conjunction, quick is just draw with less parameters to pass
    def drawText(self,textToFill, x,y):
        global showtext
        
        if textOnScreen == "":
            showtext = not showtext

        if Visual.drawlabel != None:
            Visual.drawlabel.kill()

        Visual.drawlabel = pygame_gui.elements.UITextBox(html_text=textToFill, relative_rect=pygame.Rect((x, y), (Visual.label_data["width"], Visual.label_data["height"])), manager=Visual.ui_manager, container=Visual.game_container)

        if showtext:
            Visual.drawlabel.show()
        else:
            Visual.drawlabel.hide()
    

    def quickText(self,textToFill):
        global textOnScreen
        self.drawText(textToFill,0,(height/4)* 3)
        textToFill = textOnScreen
    def clearText(self):
        global textOnScreen
        textOnScreen = ''
    def displayUI(self):
        self.drawText(textToFill,0,(height/4)*3)

gameUI = UI()

class playerStatsController():
    def __init__(self):
        pass
    def reduceStats(self):
        player_stats.reduce_hunger(0.0002,0.002)
        player_stats.reduce_thirst(0.0003,0.004)
        if 'demo' in currentScene.ID:
            player_stats.reduce_sanity(0.005,0.01)
        else:
            player_stats.add_sanity(0.01)

managePlayer = playerStatsController()

#Stagger player movement, to prevent spam and ultra fast movement
def player_input(keys_pressed):
    global currentScene
    global player_obj
    global scX, scY
    global scale
    global gamePaused
    global textOnScreen
    global tempsurf
    global last_interaction_counter

    if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_d]:
        if not gamePaused:
            if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_a]:
                player_obj.move("up-left")
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d]:
                player_obj.move("up-right")
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_s] and keys_pressed[pygame.K_a]:
                player_obj.move("down-left")
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_s] and keys_pressed[pygame.K_d]:
                player_obj.move("down-right")
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_w]:
                player_obj.move('down')
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_a]:
                player_obj.move('left')
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_s]:
                player_obj.move('up')
                managePlayer.reduceStats()
            elif keys_pressed[pygame.K_d]:
                player_obj.move('right')
                managePlayer.reduceStats()
    else:
        player_obj.move("none")
    #Open the Menu and Pause the game
    if keys_pressed[pygame.K_ESCAPE]:
        if gamePaused == False:
            gamePaused = True
            pygame.time.delay(650)
        else:
            gamePaused = False
            pygame.time.delay(650)
        
    #Make feature to capture the MOVE up, SAY xyz, MOVE down...
    if keys_pressed[pygame.K_e] and last_interaction_counter == 0:
        last_interaction_counter = 20
        command_to_do = player_obj.interact_with()
        if command_to_do == None:
            if textOnScreen == '':
                gameUI.quickText("There's nothing to interact with here")
            else:
                gameUI.clearText()
        if command_to_do is not None:
            if command_to_do.split(' ')[0] == 'DISPLAY':
                clearText()
                textOnScreen = ' '.join(command_to_do.split(' ')[1:])
            if command_to_do.split(' ')[0] == 'EXIT':
                newdungeon = command_to_do.split(' ')[1]
                print("MOVING TO " + newdungeon)
                currentDungeon = load_dungeon(newdungeon)
                currentScene = currentDungeon.head
                if currentScene.music != None and currentScene.music != '':
                    Sound.play_music(currentScene.music)
                player_obj = currentScene.get_entity('Player0')
                player_obj.stats = player_stats
                tempsurf = pygame.Surface((width, height), flags=pygame.SRCALPHA)
                for entity in currentScene.get_all_entities():
                    if "CollisionEntity" in entity.ID:
                        coordinateDraw = entity.coord
                        sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                        if currentScene.width > currentScene.length:
                            tempsurf.blit(sprite, (
                                ((coordinateDraw[0] * scale + (width - (scX * currentScene.length)) / 2),
                                 coordinateDraw[1] * scale)))
                        if currentScene.length > currentScene.width:
                            tempsurf.blit(sprite, (
                                (coordinateDraw[0] * scale,
                                 (coordinateDraw[1] * scale + (height - (scY * currentScene.width)) / 2))))
                        if currentScene.length == currentScene.width:
                            tempsurf.blit(sprite,
                                          (((coordinateDraw[0] * scale, coordinateDraw[1] * scale))))
            if command_to_do.split(' ')[0] == 'MOVE':
                print(command_to_do.split(' ')[1])
                middle_scene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                if middle_scene != None:
                    currentScene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                    if currentScene.music != None and currentScene.music != '':
                        Sound.play_music(currentScene.music)
                    player_obj = currentScene.get_entity('Player0')
                    player_obj.stats = player_stats
                    print(currentScene.ID)
                    scX = width/currentScene.width
                    scY = height/currentScene.length
                    scale = min(scX,scY)
                    tempsurf = pygame.Surface((width, height), flags=pygame.SRCALPHA)
                    # Cache all of the walls inside of a surface
                    for entity in currentScene.get_all_entities():
                        if "CollisionEntity" in entity.ID:
                            coordinateDraw = entity.coord
                            sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                            if currentScene.width > currentScene.length:
                                tempsurf.blit(sprite, (
                                    ((coordinateDraw[0] * scale + (width - (scX * currentScene.length)) / 2),
                                     coordinateDraw[1] * scale)))
                            if currentScene.length > currentScene.width:
                                tempsurf.blit(sprite, (
                                    (coordinateDraw[0] * scale,
                                     (coordinateDraw[1] * scale + (height - (scY * currentScene.width)) / 2))))
                            if currentScene.length == currentScene.width:
                                tempsurf.blit(sprite,
                                              (((coordinateDraw[0] * scale, coordinateDraw[1] * scale))))

        pygame.time.delay(100)
    elif keys_pressed[pygame.K_e]:
        last_interaction_counter -= 1
def Main():
    run = True
    
    global keys_pressed
    global currentDungeon
    global currentScene
    global player_obj
    global scY, scX
    global scale
    global gamePaused
    global textOnScreen
    global start_time
    global clock

    clock = pygame.time.Clock()
    scX = width/currentScene.width
    scY = height/currentScene.length
    scale = scX

    pygame.display.set_caption("Blizzard")

    # Cache all of the walls inside of a surface
    for entity in currentScene.get_all_entities():
        if "CollisionEntity" in entity.ID:
            coordinateDraw = entity.coord
            sprite = pygame.transform.scale(entity.sprite, (scale, scale))
            if currentScene.width > currentScene.length:
                tempsurf.blit(sprite, (
                    ((coordinateDraw[0] * scale + (width - (scX * currentScene.length)) / 2),
                     coordinateDraw[1] * scale)))
            if currentScene.length > currentScene.width:
                tempsurf.blit(sprite, (
                    (coordinateDraw[0] * scale,
                     (coordinateDraw[1] * scale + (height - (scY * currentScene.width)) / 2))))
            if currentScene.length == currentScene.width:
                tempsurf.blit(sprite,
                              (((coordinateDraw[0] * scale, coordinateDraw[1] * scale))))
    while run:
        if Visual.screen == "title":
            clock.tick(FPS)/1000 
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
                        if currentScene.music != None and currentScene.music != '':
                            Sound.play_music(currentScene.music)
                        pass

                    elif event.ui_element == Visual.newgame_button:
                        Visual.screen = "game"
                        Visual.title_container.hide()
                        Visual.player_stats_textbox.show()
                        if currentScene.music != None and currentScene.music != '':
                            Sound.play_music(currentScene.music)
                        pass

                Visual.ui_manager.process_events(event)
            
            draw_display(currentScene)
            pygame.display.update()


        elif Visual.screen == "game":
            clock.tick(FPS)
            keys_pressed = pygame.key.get_pressed()  #put this here since player_input wont work if the var isn't defined.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            player_input(keys_pressed)
            
            if gamePaused == True:
                gameUI.toggleMenu()
                gameUI.clearText()
            else:
                draw_display(currentScene)
                currentScene.update_all()
            if textOnScreen == '':
                pass
            else:
                gameUI.quickText(textOnScreen)
            pygame.display.update()


def rotate_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def draw_display(scene):
    global tempsurf

    screen.fill(black)
    Visual.ui_manager.update(clock.tick(FPS)/1000) #updates information on the ui elements
    
    if Visual.screen == "game":
        Visual.update_stat_display(player_stats.get_stats())


        #Y axis is width, X axis is length
        #first moves +right -left, second moves +down -up. 
        if scene.width > scene.length:
            # Vertical rooms
            screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scX)),((width - (scX * scene.length))/2,0))
        if scene.length > scene.width:
            # Horizontal rooms
            screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scY, scene.width * scY)),(0,(height - (scY * scene.width))/2))
        if scene.length == scene.width:
            screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),(0, 0))
        #last ones below are (0,0) as a fallback
        # screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),(0, 0)) 
        for entity in scene.get_all_entities():
            angle = 0
            coordinateDraw = entity.coord
            if 'Enemy' in entity.ID:
                angle = entity.angle_of_sight
                compx = sin(radians(entity.angle_of_sight))
                compy = cos(radians(entity.angle_of_sight))

                for s in range(entity.stopped_at+1):
                    x = (s * compx + entity.coord[0]) * (scale + (width - (scX * scene.length))/2)
                    y = (s * compy + entity.coord[1]) * (scale + (height - (scY * scene.width))/2)
                    if entity.hit:
                        pygame.draw.circle(screen, (255,0,0), (x,y), 3)
                    elif s:
                        pygame.draw.circle(screen, white, (x, y), 3)
            if 'CollisionEntity' not in entity.ID:
                sprite = pygame.transform.scale(entity.sprite, (scale, scale))
                if scene.width > scene.length:
                    screen.blit(rotate_center(sprite, angle), (
                    ((coordinateDraw[0] * scale + (width - (scX * scene.length)) / 2), coordinateDraw[1] * scale)))
                if scene.length > scene.width:
                    screen.blit(rotate_center(sprite, angle), (
                    (coordinateDraw[0] * scale, (coordinateDraw[1] * scale + (height - (scY * scene.width)) / 2))))
                if scene.length == scene.width:
                    screen.blit(rotate_center(sprite, angle),
                                (((coordinateDraw[0] * scale, coordinateDraw[1] * scale))))
        
        screen.blit(tempsurf, (0, 0))
    Visual.ui_manager.draw_ui(screen) #displays the ui elements


#run the program
Main()
