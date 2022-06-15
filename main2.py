from cProfile import run
from glob import glob
from pickle import NONE
from re import T
import pygame, random


from data_loader import *
import os
#define some variables, what FPS game will run at
#a basic white tuple to make writing colors easier
#set desired width and height game will run at later
FPS = 60
white = (255, 255, 255)
width, height = 700, 700

counter = 40
FPS = 60
white = (255,255,255)
width, height = 700,700

#calculate the sprite scale using screen -- calculation is done in Main()
scY = 0
scX = 0

#imports from other files, scene, player object
currentDungeon = load_dungeon('World/Overworld')
currentScene = currentDungeon.head
player_obj = currentScene.get_entity('Player0') 

#set our screen size
screen = pygame.display.set_mode((width,height))

#load a placeholder sprite
placeHolderSprite =  pygame.image.load('Assets/Sprites/placeholder.png')
placeHolderSprite = pygame.transform.scale(placeHolderSprite,(70,70))

#Stagger player movement, to prevent spam and ultra fast movement
def player_movement(keys_pressed):
    global currentScene
    global player_obj

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
                #currentScene.append_entity(Player((5,5),placeHolderSprite,args=['Assets/Sprites/placeholder.png','Assets/Sprites/placeholder.png','Assets/Sprites/placeholder.png','Assets/Sprites/placeholder.png']))
                player_obj = currentScene.get_entity('Player0')
                print(currentScene.ID)

placeHolderSprite =  pygame.image.load('Assets/Sprites/placeholder.png')

def Main():
    clock = pygame.time.Clock()
    run = True
    
    global keys_pressed
    global currentDungeon
    global currentScene
    global player_obj
    global scY, scX

    scX = width/currentScene.width
    scY = height/currentScene.length
    global placeHolderSprite
    placeHolderSprite = pygame.transform.scale(placeHolderSprite,(scX/10,scY/10))

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
    screen.blit(pygame.transform.scale(scene.background_image,(width,height)),(0,0)) 
    for entity in scene.get_all_entities():
        coordinateDraw = entity.coord 
        screen.blit(pygame.transform.scale(entity.sprite,(scX,scY)),((coordinateDraw[0]* scX,coordinateDraw[1]*scY)))
    pygame.display.update()

Main()