from cProfile import run
from glob import glob
from pickle import NONE
from re import T
import pygame, random
from data_loader import *
import os
import math

#define some variables, what FPS game will run at
#a basic white tuple to make writing colors easier
#set desired width and height game will run at later
FPS = 60
black = (0,0,0)
white = (255, 255, 255)
width, height = 700, 700
#calculate the sprite scale using screen -- calculation is done in Main()
scY = 0
scX = 0
scale = 0
#imports from other files, scene, player object
currentDungeon = load_dungeon('World/Overworld')
currentScene = currentDungeon.head
player_obj = currentScene.get_entity('Player0') 
#set our screen size
screen = pygame.display.set_mode((width,height))

##########################################################################
pygame.font.init()

font = pygame.font.SysFont('arial',40)


def drawText(text, font, text_col,x,y):
    img = font.render(text,True, text_col)
    screen.blit(img, (x,y))

def displayMenu():
    screen.fill(0,0,0)


#Stagger player movement, to prevent spam and ultra fast movement
def player_movement(keys_pressed):
    global currentScene
    global player_obj
    global scX
    global scY
    global scale

    if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_d]:
        if keys_pressed[pygame.K_w]:
            player_obj.move('down')
        elif keys_pressed[pygame.K_a]:
            player_obj.move('left')
        elif keys_pressed[pygame.K_s]:
            player_obj.move('up')
        elif keys_pressed[pygame.K_d]:
            player_obj.move('right')
        pygame.time.delay(400)

    #Make feature to capture the MOVE up, SAY xyz, MOVE down...
    if keys_pressed[pygame.K_e]:
        command_to_do = player_obj.interact_with()
        if command_to_do == None:
            print("there's interact with here")
            return
        if command_to_do.split(' ')[0] == 'MOVE':
            print(command_to_do.split(' ')[1])
            middle_scene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
            if middle_scene != None:
                currentScene = currentScene.linked_rooms[command_to_do.split(' ')[1]]
                player_obj = currentScene.get_entity('Player0')
                print(currentScene.ID)
                scX = width/currentScene.width
                scY = height/currentScene.length
                scale = scX
 
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

    scX = width/currentScene.width
    scY = height/currentScene.length
    scale = scX

    pygame.display.set_caption("Blizzard")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed)
        draw_display(currentScene)
            

def draw_display(scene):
    screen.fill(black)
    #new solution
    #down is width side is length
    #first moves +right -left, second moves +down -up. 
    #I flipped the order of scene.length/2 and scene.width/2
    if scene.width > scene.length:
        screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),((width - (scX * scene.length))/2,0))
        print("WIDTH IS MORE")
    if scene.length > scene.width:
        screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),(0,(height - (scY * scene.width))/2))
        print("LENGTH IS MORE")
    if scene.length == scene.width:
        screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),(0, 0))
    #last ones below are (0,0) as a fallback
    # screen.blit(pygame.transform.scale(scene.background_image,(scene.length * scX, scene.width * scY)),(0, 0)) 
    for entity in scene.get_all_entities():        
        coordinateDraw = entity.coord
        if scene.width > scene.length:
            screen.blit(pygame.transform.scale(entity.sprite,(scale,scale)),(((coordinateDraw[0]* scale + (width - (scX * scene.length))/2),coordinateDraw[1]*scale)))
        if scene.length > scene.width:
            screen.blit(pygame.transform.scale(entity.sprite,(scale,scale)),((coordinateDraw[0]* scale,(coordinateDraw[1]*scale + (height - (scY * scene.height))/2))))
        if scene.length == scene.width:
            screen.blit(pygame.transform.scale(entity.sprite,(scale,scale)),(((coordinateDraw[0]* scale,coordinateDraw[1]*scale))))
    pygame.display.update()

#displayMenu()

Main()