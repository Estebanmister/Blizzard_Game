import pygame, random


class Sounds:
    current_track = None
    music_volume = 0.15
    sound_volume = 0.05
    
    def __init__(self):
        pygame.mixer.init()

    def play_music(self, track):
        """
        Changes the music, crossfading between the tracks.

        :param track: The music file we want.
        """

        if self.current_track != None:
            self.current_track.fadeout(1000)

        self.current_track = pygame.mixer.Sound("Assets/Music/" + track)
        self.current_track.set_volume(self.music_volume)
        self.current_track.play(loops=-1, fade_ms=1000)

    def play_sound(self, sound):
        """
        Plays a SFX.

        :param sound: the sound effect being played.
        """
        if isinstance(sound, list):
            sound = random.choice(sound)
        sound = pygame.mixer.Sound("Assets\\Sound effects\\" + sound)
        sound.set_volume(self.sound_volume)
        sound.play(0)