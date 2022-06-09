import pygame, pygame_gui, pytmx

class Visuals():
    screen        = "title" #change to  "title" or "game" to switch what screen is shown. We can use this for future screens too! (like character creation or stat screens.)
    window_width  = None
    window_height = None
    time_delta    = None
    gameScreen    = None
    background    = None
    background    = None
    gameMap       = None
    map_x         = None
    map_y         = None
    window_width  = None
    window_height = None
    gameScreen    = None
    gameMap       = None
    background    = None


    def __init__(self, td):
        self.window_width = 600 #display width and height
        self.window_height = 800 #display width and height
        self.time_delta = td

        self.gameScreen = pygame.display.set_mode((self.window_width, self.window_height)) #creates the window
        self.background =  pygame.Surface((self.window_width, self.window_height)) #creates a surface for us to draw on
        self.background.fill(pygame.Color('#000000')) #fills that surface with the color black
        pygame.display.set_caption('Game') #names the window

        self.tilewidth, self.tileheight = 16, 16

        self.map_x = self.window_width/2 - (self.tilewidth*30)/2 #sets the map to be in the middle of the screen
        self.map_y = self.tilewidth*2

        self.make_framework()
        self.make_title()
        self.make_game()

    def make_framework(self):
        self.ui_manager = pygame_gui.UIManager((self.window_width, self.window_height), "Assets\\theme.json", True) #manages the elements onscreen

        self.title_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(self.window_width,self.window_height)),manager=self.ui_manager) #a group we can contain the elements within. We use these since the containers can be hidden/shown as we wish.
        self.game_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(self.window_width,self.window_height)),manager=self.ui_manager)

    def make_game(self): 
        self.textbox_data = {"position_x" : self.map_x, "position_y": self.map_y*2 + self.tileheight*30, "height" : 200, "width" : self.tilewidth*30/2 - self.tilewidth} #information for a text box below the map
        self.textbox = pygame_gui.elements.UITextBox(html_text="", relative_rect=pygame.Rect((self.textbox_data["position_x"], self.textbox_data["position_y"]), (self.textbox_data["width"], self.textbox_data["height"])), manager=self.ui_manager, container=self.game_container) #creates the text box
    
    def make_title(self): 
        self.label_data = {"position_x" : 0, "position_y": self.map_y*4, "height" : 100, "width" : self.window_width}
        self.label = pygame_gui.elements.UILabel(text="Game Title", relative_rect=pygame.Rect((self.label_data["position_x"], self.label_data["position_y"]), (self.label_data["width"], self.label_data["height"])), manager=self.ui_manager, container=self.title_container)

        self.continue_button_data = {"position_x" : self.window_width/4, "position_y": self.label_data["position_y"] + self.map_y*5, "height" : 100, "width" : self.window_width/2}
        self.continue_button = pygame_gui.elements.UIButton(text="Continue Game", relative_rect=pygame.Rect((self.continue_button_data["position_x"], self.continue_button_data["position_y"]), (self.continue_button_data["width"], self.continue_button_data["height"])), manager=self.ui_manager, container=self.title_container)

        self.newgame_button_data = {"position_x" : self.window_width/4, "position_y": self.continue_button_data["position_y"] + self.continue_button_data["height"] + self.map_y, "height" : self.continue_button_data["height"], "width" : self.window_width/2}
        self.newgame_button = pygame_gui.elements.UIButton(text="New Game", relative_rect=pygame.Rect((self.newgame_button_data["position_x"], self.newgame_button_data["position_y"]), (self.newgame_button_data["width"], self.newgame_button_data["height"])), manager=self.ui_manager, container=self.title_container)

        self.quit_button_data = {"position_x" : self.window_width/4, "position_y": self.newgame_button_data["position_y"] + self.newgame_button_data["height"] + self.map_y, "height" : self.newgame_button_data["height"], "width" : self.window_width/2}
        self.quit_button = pygame_gui.elements.UIButton(text="Quit", relative_rect=pygame.Rect((self.quit_button_data["position_x"], self.quit_button_data["position_y"]), (self.quit_button_data["width"], self.quit_button_data["height"])), manager=self.ui_manager, container=self.title_container)

#===========================================================================

    def blit_all(self): 
        #displays all of the stuff onscreen for us to see. Things 'blitted' first are shown in the back, and things 'blitted' last show at the front.
        self.ui_manager.update(self.time_delta) #updates information on the ui elements
        self.gameScreen.blit(self.background, (0, 0))

        if self.screen == "title":
            self.blit_title()
        elif self.screen == "game":
            self.blit_game()

        self.ui_manager.draw_ui(self.gameScreen) #displays the ui elements
        pygame.display.update() #shows the changes made
        
    def blit_title(self):
        pass

    def blit_game(self):
        for layer in self.gameMap.visible_layers: #for row
            for x, y, gid, in layer: #for column
                try: #since some tiles are empty, we need to put this in a try statement, or it'll crash.
                    tile = self.gameMap.get_tile_image_by_gid(gid) #grabs the tile's image
                    x, y = self.grid(x, y, "pixels") #gets the pixel measurements for the tile
                    self.gameScreen.blit(tile, (x+ self.map_x, y + self.map_y)) #displays the tile
                except:
                    pass

        # for entity in self.entities:
        #     self.gameScreen.blit(entity.image, (entity.x + self.map_x, entity.y + self.map_y)) #enemies, player, etc
    
#===========================================================================

    def grid(self, x, y, type): #todo Find a better way to do this. Tileheight/width is 16.
        if type == "pixels":
            return int(x*self.tilewidth), int(y*self.tileheight)
        if type == "grid":
            return int(x/self.tilewidth), int(y/self.tileheight)
