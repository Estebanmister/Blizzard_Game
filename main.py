import pygame, pytmx, random, pygame_gui

from Classes import visuals


class Main():
    clock         = None

    doors         = None
    item          = None

    player        = None
    entities      = []


    Visuals = None

    def __init__(self):
            
        pygame.init()
        
        self.clock = pygame.time.Clock() #makes a clock to check the time
        self.time_delta = self.clock.tick(30)/1000 #used for pygame_gui elements.
        self.Visuals = visuals.Visuals(self.time_delta)
        self.change_screen("title")

        self.update = False #used for moving the entities

        self.doors = [58, 59, 64, 63] #each tile in the TMX file has an ID. this declares what number the IDs 'mean'
        self.item = [65,66]

    def start_game(self):
        #do whatever we need to here

        self.game_loop()

    def change_screen(self, screen):
        self.Visuals.screen = screen
        if self.Visuals.screen == "title":
            self.Visuals.title_container.show()
            self.Visuals.game_container.hide()
        elif self.Visuals.screen == "game":
            self.Visuals.title_container.hide()
            self.Visuals.game_container.show()
            self.load_map()

    def game_loop(self):
        while True:
            self.time_delta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if self.Visuals.screen == "title":
                    if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                        if event.ui_element == self.Visuals.quit_button:
                            pygame.quit()
                            quit()
                        elif event.ui_element == self.Visuals.continue_button:
                            self.change_screen("game")

                elif self.Visuals.screen == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            self.player.move("up")
                            self.update = True
                            
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            self.player.move("down")
                            self.update = True

                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.player.move("left")
                            self.update = True

                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.player.move("right")
                            self.update = True
    
                self.Visuals.ui_manager.process_events(event)

            if self.update: #Triggers when we preform an action
                self.update = False
                #!Method for updating entities (moving them for example) goes here
            
            self.Visuals.blit_all()            

    def load_map(self, mapname = "map"):
        self.Visuals.gameMap = pytmx.load_pygame('Assets/'+mapname+'.tmx') #loads our map from a TMX file
        #NOTICE!!! Im getting an error here and i have 0 clue why. "Found external tileset, but cannot handle type: None". Not sure whats up with it right now but ill figure it out. its midnight and i don't want to keep yall waiting any longer for my code.

game = Main()
game.start_game()
