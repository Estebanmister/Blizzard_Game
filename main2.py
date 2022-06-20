import pygame
from data_loader import *
from Classes.player_stats import *
from math import sin, cos, radians
import math

#define some variables, what FPS game will run at
#basic colour tuples to make writing colours easier
#set desired width and height game will run at later
FPS = 60
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
currentDungeon = load_dungeon('World/Dungeons')
currentScene = currentDungeon.head

player_obj = currentScene.get_entity('Player0')
player_stats = PlayerStats()
player_obj.stats = player_stats
#set our screen size
screen = pygame.display.set_mode((width,height))
pygame.display.set_icon(pygame.image.load("Assets/Sprites/playerdown.png"))
##########################################################################
pygame.font.init()

font = pygame.font.SysFont('arial',40)


def drawText(text, font, text_col,x,y):
    img = font.render(text,True, text_col)
    screen.blit(img, (x,y))

def quickText(textToFill):
    global textOnScreen
    if textOnScreen != '':
        drawText(textToFill,font,white,0,(height/4)*3)
        textOnScreen = textToFill
    else:
        pass

def clearText():
    global textOnScreen
    textOnScreen = ''

def displayMenu():
    screen.fill(black)
    drawText("MENU",font,white,width/2,0)

#Stagger player movement, to prevent spam and ultra fast movement
def player_input(keys_pressed):
    global currentScene
    global player_obj
    global scX, scY
    global scale
    global gamePaused
    global textOnScreen

    if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_d]:
        if textOnScreen == '' and not gamePaused:
            if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_a]:
                player_obj.move("up-left")
            elif keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d]:
                player_obj.move("up-right")
            elif keys_pressed[pygame.K_s] and keys_pressed[pygame.K_a]:
                player_obj.move("down-left")
            elif keys_pressed[pygame.K_s] and keys_pressed[pygame.K_d]:
                player_obj.move("down-right")
            elif keys_pressed[pygame.K_w]:
                player_obj.move('down')
            elif keys_pressed[pygame.K_a]:
                player_obj.move('left')
            elif keys_pressed[pygame.K_s]:
                player_obj.move('up')
            elif keys_pressed[pygame.K_d]:
                player_obj.move('right')
    #Open the Menu and Pause the game
    if keys_pressed[pygame.K_ESCAPE]:
        if gamePaused == False:
            gamePaused = True
            pygame.time.delay(650)
        else:
            gamePaused = False
            pygame.time.delay(650)
        
    #Make feature to capture the MOVE up, SAY xyz, MOVE down...
    if keys_pressed[pygame.K_e]:
        command_to_do = player_obj.interact_with()
        if command_to_do == None:
            if textOnScreen == '':
                textOnScreen = "There's nothing to interact with here"
                quickText(textOnScreen)
            else:
                clearText()
        if command_to_do is not None:
            if command_to_do.split(' ')[0] == 'MOVE':
                print(command_to_do.split(' ')[1])
                middle_scene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                if middle_scene != None:
                    currentScene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                    player_obj = currentScene.get_entity('Player0')
                    player_obj.stats = player_stats
                    print(currentScene.ID)
                    scX = width/currentScene.width
                    scY = height/currentScene.length
                    scale = min(scX,scY)
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

        pygame.time.delay(400)

def Main():
    clock = pygame.time.Clock()
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
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys_pressed = pygame.key.get_pressed()
        player_input(keys_pressed)
        
        if gamePaused == True:
            displayMenu()
            clearText()
        else:
            draw_display(currentScene)
            currentScene.update_all()
        if textOnScreen == '':
            pass
        else:
            quickText(textOnScreen)
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


#run the program
Main()