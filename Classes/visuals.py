import pygame, pygame_gui

class Visuals():
    def __init__(self, width, height, dictionary):
        self.screen = "title"
        self.window_width = width #display width and height
        self.window_height = height #display width and height
        self.player_stats = None


        self.make_framework()
        self.make_title()
        self.make_game()
        self.update_stat_display(dictionary)

        self.text_label.hide()
        self.player_stats_textbox.hide()

    def make_framework(self):
        self.ui_manager = pygame_gui.UIManager((self.window_width, self.window_height), "Assets/theme.json", True) #manages the elements onscreen

        self.title_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(self.window_width,self.window_height)),manager=self.ui_manager) #a group we can contain the elements within. We use these since the containers can be hidden/shown as we wish.
        self.game_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(self.window_width,self.window_height)),manager=self.ui_manager)
    
    def make_title(self): 
        self.label_data = {"position_x" : 0, "position_y": 50, "height" : 100, "width" : self.window_width}
        self.label = pygame_gui.elements.UILabel(text="Blizzard", relative_rect=pygame.Rect((self.label_data["position_x"], self.label_data["position_y"]), (self.label_data["width"], self.label_data["height"])), manager=self.ui_manager, container=self.title_container, object_id="@title")

        self.continue_button_data = {"position_x" : self.window_width/4, "position_y": self.label_data["position_y"] + 150, "height" : 100, "width" : self.window_width/2}
        self.continue_button = pygame_gui.elements.UIButton(text="Continue Game", relative_rect=pygame.Rect((self.continue_button_data["position_x"], self.continue_button_data["position_y"]), (self.continue_button_data["width"], self.continue_button_data["height"])), manager=self.ui_manager, container=self.title_container)

        self.newgame_button_data = {"position_x" : self.window_width/4, "position_y": self.continue_button_data["position_y"] + self.continue_button_data["height"] + 50, "height" : self.continue_button_data["height"], "width" : self.window_width/2}
        self.newgame_button = pygame_gui.elements.UIButton(text="New Game", relative_rect=pygame.Rect((self.newgame_button_data["position_x"], self.newgame_button_data["position_y"]), (self.newgame_button_data["width"], self.newgame_button_data["height"])), manager=self.ui_manager, container=self.title_container)

        self.quit_button_data = {"position_x" : self.window_width/4, "position_y": self.newgame_button_data["position_y"] + self.newgame_button_data["height"] + 50, "height" : self.newgame_button_data["height"], "width" : self.window_width/2}
        self.quit_button = pygame_gui.elements.UIButton(text="Quit", relative_rect=pygame.Rect((self.quit_button_data["position_x"], self.quit_button_data["position_y"]), (self.quit_button_data["width"], self.quit_button_data["height"])), manager=self.ui_manager, container=self.title_container)

    def make_game(self):
        self.text_label_data = {"position_x" : self.window_width/4, "position_y": self.window_height - 150, "height" : 100, "width" : self.window_width/2}
        self.text_label = pygame_gui.elements.UILabel(text="", relative_rect=pygame.Rect((self.text_label_data["position_x"], self.text_label_data["position_y"]), (self.text_label_data["width"], self.text_label_data["height"])), manager=self.ui_manager, container=self.game_container)

        self.player_stats_data = {"position_x" : 0, "position_y": 0, "height" :  self.window_height/12, "width" : self.window_width/2}
        
        self.player_stats_textbox = pygame_gui.elements.UILabel(text="", relative_rect=pygame.Rect((self.player_stats_data["position_x"], self.player_stats_data["position_y"]), (self.player_stats_data["width"], self.player_stats_data["height"])), manager=self.ui_manager, container=self.game_container)

    def update_stat_display(self, dictionary):
        text = "Hunger: "+ str(dictionary["hunger"]) + "  Thirst: "+ str(dictionary["thirst"]) + "  Sanity: " + str(dictionary["sanity"])
        self.player_stats_textbox.set_text(text)
