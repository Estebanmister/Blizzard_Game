import csv
from Classes.dungeon import Dungeon
from Classes.scene import Scene
from pygame.image import load
from Classes.entity import Entity
from Classes.player import Player

entity_types = {'entity': Entity, 'player': Player}

# This code may look like dark magic, but I swear i will be commenting how everything works as soon as i can.
# - Esteban


def load_dungeon(filename):
    """
    Load a dungeon, the scenes, link the scenes, and add entities.
    :param filename: The FOLDER of the .csv (NOT the csv file itself)
    :return: Dungeon object
    """
    filename = filename.strip('/')
    with open(filename+"/dungeon.csv") as dungeonf:
        scenesf = open(filename+"/scenes.csv")
        scenes_unformated = csv.DictReader(scenesf)
        scenesdict = {'':None}
        for scene in scenes_unformated:
            back = ''
            if scene['background_image']:
                back = load(scene['background_image'])
            entities = []
            if scene['entities']:
                entity_params = scene['entities'].split(';')
                for param in entity_params:
                    if param != '':
                        things = param.split('*')
                        entities.append(entity_types[things[0]]([int(things[2]), int(things[3])], load(things[1]), args=things[4:]))
            scenesdict[scene['ID']] = Scene(scene['ID'], int(scene['length']), int(scene['width']), back, music=scene['music'])
            for entity in entities:
                scenesdict[scene['ID']].append_entity(entity)
        dungeondict = list(csv.DictReader(dungeonf))
        dungeon = Dungeon(head=scenesdict[dungeondict[0]['ID']])
        dungeon.head.linked_rooms = {'left': scenesdict[dungeondict[0]['left']], 'right': scenesdict[dungeondict[0]['right']],
                                     'up': scenesdict[dungeondict[0]['up']], 'down': scenesdict[dungeondict[0]['down']]}
        for scene in dungeondict[1:]:
            dungeon.get(scene['ID']).linked_rooms = {'left': scenesdict[scene['left']], 'right': scenesdict[scene['right']],
                                                     'up': scenesdict[scene['up']], 'down': scenesdict[scene['down']]}
        return dungeon
