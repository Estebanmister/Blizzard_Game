# data_loader.py
# Esteban, Richard, Utkarsh, Sam
# June 21, 2022

import csv
from Classes.dungeon import Dungeon
from Classes.scene import Scene
from pygame.image import load
from Classes.entity import Entity
from Classes.player import Player
from Classes.collisionentity import CollisionEntity
from Classes.door import Door
from Classes.enemy import Enemy
from Classes.finaldoor import FinalDoor
from Classes.consumables import WaterBottle, CannedFood
from Classes.notes import Notes


entity_types = {'note':Notes,'bottle':WaterBottle , 'can':CannedFood , 'finaldoor': FinalDoor, 'entity': Entity, 'player': Player, 'wall': CollisionEntity, 'door': Door, 'enemy':Enemy}


def load_dungeon(filename):
    """
    Load a dungeon, the scenes, link the scenes, and add entities.
    :param filename: The FOLDER of the .csv (NOT the csv file itself)
    :return: Dungeon object
    """
    filename = filename.strip('/')
    # Load two files: the linked scenes file (dungeon.csv)
    # And the scene properties file (scenes.csv)
    with open(filename+"/dungeon.csv") as dungeonf:
        scenesf = open(filename+"/scenes.csv")
        scenes_unformated = csv.DictReader(scenesf)
        # This dictionary will be populated with scene objects, and IDs as keys
        scenesdict = {'':None}
        for scene in scenes_unformated:
            # For each entry in the csv
            if scene['ID'] == '':
                # skip empty lines
                continue
            print("LOADING " + scene['ID'])
            back = ''
            if scene['background_image']:
                # In the case of having a background image, load it as a pygame.Surface
                back = load(scene['background_image'])
            # Create an empty list that will hold all of the entity objects in the scene
            entities = []
            if scene['entities']:
                entity_params = scene['entities'].split(';')
                # The entity parameter is separated by semicolons, and each entry gives the info to make an entity
                for param in entity_params:
                    if param != '':
                        things = param.split('*')
                        # The first parameter is always the type of entity
                        # The entity_types dict will return an initializer function according to the type
                        # The second and third parameter are the x, y positions of the entity
                        # The third parameter is the address to an image to use as sprite
                        # The rest of the parameters are all loaded into an optional argument, 'args'
                        entities.append(entity_types[things[0]]([int(things[2]), int(things[3])], load(things[1]), args=things[4:]))
            # Create this scene corresponding to this line, with everything we have so far
            scenesdict[scene['ID']] = Scene(scene['ID'], int(scene['length']), int(scene['width']), back, music=scene['music'])
            for entity in entities:
                # And now append all the entities (which also sets the correct index for each one)
                scenesdict[scene['ID']].append_entity(entity)
        # Load the _D_ungeon position _Dict_ionary entries into dungeondict
        dungeondict = list(csv.DictReader(dungeonf))
        # Crete a dungeon head object for the Graph dungeon map
        # Set the 'head' to the first scene in our dungeon dictionary entries
        dungeon = Dungeon(head=scenesdict[dungeondict[0]['ID']])
        # Link the head rooms.
        # Each scene in dungeondict has four directions, that point towards other IDs for other scenes
        dungeon.head.linked_rooms = {'left': scenesdict[dungeondict[0]['left']], 'right': scenesdict[dungeondict[0]['right']],
                                     'up': scenesdict[dungeondict[0]['up']], 'down': scenesdict[dungeondict[0]['down']]}
        for scene in dungeondict[1:]:
            # For each scene ID in the dungeondict after the head:
            # Find that scene, and set the lined rooms to what they should be
            # As of 22 Jun, this will never end in an infinite loop
            dungeon.get(scene['ID']).linked_rooms = {'left': scenesdict[scene['left']], 'right': scenesdict[scene['right']],
                                                     'up': scenesdict[scene['up']], 'down': scenesdict[scene['down']]}
        return dungeon
