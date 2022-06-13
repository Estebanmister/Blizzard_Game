from cProfile import run
import pygame, pytmx, random, pygame_gui
from data_loader import *
from Classes import visuals
import os

#define some variables, what FPS game will run at
#a basic white tuple to make writing colors easier
#set desired width and height game will run at later
FPS = 60
white = (255, 255, 255)
width, height = 700, 700

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


def player_movement(keys_pressed):
    if keys_pressed[pygame.K_a]:
        print("works")
        player_obj.move('left')
    if keys_pressed[pygame.K_d]:
        player_obj.move('right')
        print("works")
    if keys_pressed[pygame.K_w]:
        player_obj.move('up')
        print("works")
    if keys_pressed[pygame.K_s]:
        player_obj.move('down')
        print("works")

placeHolderSprite =  pygame.image.load('Assets/Sprites/placeholder.png')
placeHolderSprite = pygame.transform.scale(placeHolderSprite,(70,70))

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