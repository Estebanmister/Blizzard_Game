from cProfile import run
import pygame, pytmx, random, pygame_gui
from data_loader import *
from Classes import visuals
import os

FPS = 60
white = (255, 255, 255)
width, height = 700, 700

# calculate the sprite scale using screen -- calculation is done in Main()
scY = 0
scX = 0

screen = pygame.display.set_mode((width, height))

placeHolderSprite = pygame.image.load('Assets/Sprites/placeholder.png')
placeHolderSprite = pygame.transform.scale(placeHolderSprite, (70, 70))


def Main():
    clock = pygame.time.Clock()
    run = True

    currentDungeon = load_dungeon('World/Overworld')
    currentScene = currentDungeon.head

    global scY, scX
    scX = width / currentScene.width
    scY = height / currentScene.length

    pygame.display.set_caption("Blizzard")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_display(currentScene)
        currentScene.update_all()


def draw_display(scene):
    screen.blit(pygame.transform.scale(scene.background_image, (width, height)), (0, 0))
    for entity in scene.get_all_entities():
        coordinateDraw = entity.coord
        screen.blit(pygame.transform.scale(entity.sprite, (scX, scY)),
                    ((coordinateDraw[0] * scX, coordinateDraw[1] * scY)))

    pygame.display.update()


Main()
