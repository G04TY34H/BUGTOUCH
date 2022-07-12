import pygame  # Import de la Bibliothèque PyGame

import ihm as i  # Import le fichier ''ihm'' pour pouvoir appeler ''main_menu'' dans ''ihm''

pygame.init()  # Initialise la biblio Pygame

window = pygame.display.set_mode((1280, 720))  # Création de la fenêtre de l'application

i.main_menu(window)  # Fonction démarrage de l'application appelle l'interface du menu du jeu
