import pygame, os, csv
# By Esteban
# To be commented.

x = 10
y = 10
currentID = ""

all_scenes = []
current_back = None
all_sprites = os.listdir("Assets/Sprites")
screen = pygame.display.set_mode((x,y))
tempsurf = pygame.Surface((x*50,y*50), flags=pygame.SRCALPHA)
def createScene():
    global currentID, x, y, current_back, tempsurf, screen
    currentID = input("Scene ID")
    x = int(input('x:'))
    y = int(input('y:'))
    back = input("background image:")
    current_back = pygame.image.load(back)
    all_scenes.append({'ID': currentID, 'length':x, 'width':y, 'background_image':back, 'music':'', 'entities':''})
    tempsurf = pygame.Surface((x*50,y*50), flags=pygame.SRCALPHA)
createScene()


run = True
# Player args: Assets/Sprites/playerup.png*Assets/Sprites/playerdown.png*Assets/Sprites/playerleft.png*Assets/Sprites/playerright.png
entity = {'type': 'entity', 'sprite':"Assets/Sprites/placeholder.png", 'x':0,'y':0, 'args':''}
types = ['can','bottle','note','entity','wall','player','door','enemy']
entities = []
i = 0
image_i = 0
count = 50
toggle = False

clock = pygame.time.Clock()
while run:
    #screen.fill((0,0,0))
    screen.blit(pygame.transform.scale(current_back, (x*50, y*50)), (0,0))
    screen.blit(tempsurf, (0,0))
    pos = pygame.mouse.get_pos()
    screen.blit(pygame.transform.scale(pygame.image.load(entity['sprite']), (50,50)), pos)
    pygame.display.update()
    screen = pygame.display.set_mode((x*50,y*50))

    for event in pygame.event.get():
        clock.tick(60)
        if event.type == pygame.QUIT:
            run = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            toggle = True
        if toggle and event.type == pygame.MOUSEBUTTONUP:
            entity['x'] = pos[0]//50
            entity['y'] = pos[1]//50
            tempsurf.blit(pygame.transform.scale(pygame.image.load(entity['sprite']), (50, 50)),
                          (entity['x'] * 50, entity['y'] * 50))
            ent = ""
            for vl in entity.values():
                ent += str(vl) + "*"
            ent = ent.strip('*')
            all_scenes[-1]['entities'] += ent + ';'
            print("ENTITY ADDED")
            #print(all_scenes[-1]['entities'])
        if keys[pygame.K_s]:
            if count == 0:
                filename = input("save_as?")
                with open(filename, "w+") as f:
                    writer = csv.DictWriter(f, fieldnames=['ID','length','width','background_image','music','entities'])
                    writer.writeheader()
                    writer.writerows(all_scenes)
                count = 50
            else:
                count -= 1
        if keys[pygame.K_c]:
            createScene()
        if keys[pygame.K_v]:
            if count == 0:
                i += 1
                if i > len(types)-1:
                    i = 0
                entity['type'] = types[i]
                print("ENTITY TYPE: " + types[i])
                count = 50
            else:
                count -= 1
        if keys[pygame.K_n]:
            if count == 0:
                image_i += 1
                if image_i > len(all_sprites)-1:
                    image_i = 0
                if '.png' not in all_sprites[image_i]:
                    image_i += 1
                entity['sprite'] = 'Assets/Sprites/' + all_sprites[image_i]
                print(entity['sprite'])
                count = 50
            else:
                count -= 1
        if keys[pygame.K_m]:
            if count == 0:
                image_i -= 1
                if image_i < 0:
                    image_i = len(all_sprites)-1
                if '.png' not in all_sprites[image_i]:
                    image_i -= 1
                entity['sprite'] = 'Assets/Sprites/' + all_sprites[image_i]
                print(entity['sprite'])
                count = 50
            else:
                count -= 1
        if keys[pygame.K_b]:
            if count == 0:
                amounts = {'can': 0,'bottle': 0,'note': 0,'entity': 0, 'player':4, 'door': 0, 'wall':0, 'enemy':4}
                if types[i] == 'player':
                    entity['args'] = "*Assets/Sprites/playerup.png*Assets/Sprites/playerdown.png*Assets/Sprites/playerleft.png*Assets/Sprites/playerright.png"
                else:
                    print(types[i] + " HAS " + str(amounts[types[i]]) +
                          " ARGUMENTS (Read class docstring to see what they do)")
                    for arg_counter in range(amounts[types[i]]):
                        entity['args'] += input("args>") + "*"
                count = 50
            else:
                count -= 1