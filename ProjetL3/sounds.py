import pygame

import ihm

def get_selected_color():
    return ihm.color_selected

class SoundManager:

    def __init__(self):
        pygame.mixer.init()
        self.sounds ={
            'click': pygame.mixer.Sound("clickwav.wav"),
            'kill_moskito': pygame.mixer.Sound ("kill.mp3")
        }

    def play(self, name):
        self.sounds[name].play()