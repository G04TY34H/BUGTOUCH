import pygame                   # Import de la Bibliothèque PyGame
from pygame.locals import *

import ihm as i # Import le fichier ''ihm'' pour pouvoir appeller ''main_menu'' dans ''ihm''

pygame.init()   # Initialise la biblio Pygame
window = pygame.display.set_mode((1280, 720), HWSURFACE | DOUBLEBUF | RESIZABLE) # Création de la fenêtre de l'application

i.main_menu(window) # Fonction démarrage de l'applicaiton appelle l'interace du menu du jeu

