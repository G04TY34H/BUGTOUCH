import threading
import pygame, random, sys
from pygame.locals import *

import cv2  # Import de la bibliothèque OpenCV
import numpy as np  # Import de la bibliothèque nunPy

import function as f
import class_file as c

cursor = pygame.image.load(r'cursor.png')
cursor = pygame.transform.scale(cursor, (50, 50))
background = pygame.image.load(r'fond.png')

cursor = pygame.image.load(r'cursor.png')
cursor = pygame.transform.scale(cursor, (50, 50))
background = pygame.image.load(r'fond.png')

stop_thread = threading.Event()


# ==================================================================================================================== #

# ==================================================================================================================== #


def show_score(x, y, score_value, window):
    score = f.get_font(60).render("Score : " + str(score_value), True, "#b68f40")
    window.blit(score, (x, y))


# ==================================================================================================================== #

# ==================================================================================================================== #


def main_menu(window):  # Menu du Jeu

    pygame.display.set_caption("Insect Touch")

    window.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))

    pygame.mouse.set_visible(False)

    pygame.display.set_caption("Menu")

    while True:

        MENU_TEXT = f.get_font(100).render("BUG Touch", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 9))

        BOUTON_JOUER = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                 pos=((window.get_width() / 2), window.get_height() / 2 - 125),
                                 text_input='JOUER', font=f.get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTON_REGLES = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                  pos=((window.get_width() / 2), window.get_height() / 2 + 25),
                                  text_input="REGLES", font=f.get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTON_QUITTER = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                   pos=((window.get_width() / 2), window.get_height() / 2 + 175),
                                   text_input="QUITTER", font=f.get_font(50), base_color="#d7fcd4",
                                   hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [BOUTON_JOUER, BOUTON_REGLES, BOUTON_QUITTER]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(window)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_q:  # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == VIDEORESIZE:
                if window.get_width() < 1152:
                    window = pygame.display.set_mode((1152, window.get_height()), pygame.RESIZABLE)
                    pygame.display.update()
                elif window.get_height() < 648:
                    window = pygame.display.set_mode((window.get_width(), 648), pygame.RESIZABLE)
                    pygame.display.update()
                else:
                    window = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    window.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
                    pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOUTON_JOUER.checkForInput(pygame.mouse.get_pos()):
                    choix_mode_jeu(window)
                if BOUTON_REGLES.checkForInput(pygame.mouse.get_pos()):
                    regles(window)
                if BOUTON_QUITTER.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        window.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))


# ==================================================================================================================== #

# ==================================================================================================================== #


def thread_cv2():   # FONCTION CALIBRAGE PERSPECTIVE CAMERA

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Création objet de la class ''cv2 VideoCapture'' nommé ''cap'', c'est via cette class que l'on accède à la caméra / webcam

    while True:
        _, frame = cap.read()  # Lecture du flux vidéo de la caméra ou webcam, return True si lu correctement, False dans le cas contraire

        f.draw_point(frame)  # Fonction qui permet de placer les points pour la calibration. Une fois les 4 points
                             # placé elle appelle la fonction ''change_perspective'' qui générera une nouvelle fenêtre avac une perspective à plat

        cv2.imshow("Frame", frame)  # Affiche la fenêtre de capture de la webcam
        cv2.setMouseCallback('Frame', f.click_event)  # Event Click souris sur le fenêtre de vidéo principal

        cv2.waitKey(1)

        if stop_thread.is_set():    # SI ''stop_thread.is_set'' alos arrête du thread et fermeture des windows OpenCV
            cap.release()
            cv2.destroyAllWindows()
            stop_thread.clear()
            break


# ==================================================================================================================== #

# ==================================================================================================================== #


def choix_mode_jeu(window):

    fond_bouton_mode = f.fond_resize(550 , 85)
    fond_bouton_calibrage = f.fond_resize(800 , 85)


    base_color_mode1 = 'white'
    hovering_color_mode1 = "#d7fcd4"

    base_color_mode2 = 'white'
    hovering_color_mode2 = "#d7fcd4"

    base_color_calibrage = 'white'
    hovering_color_calibrage = "#d7fcd4"

    base_color_jouer = 'white'
    hovering_color_jouer = "#d7fcd4"

    mode_select = 0

    while True:

        CHOIX_TEXT = f.get_font(68).render("Choix Modes de Jeu", True, "#b68f40")
        CHOIX_RECT = CHOIX_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 9))

        CALIBRAGE_TEXT = f.get_font(70).render("Calibrage", True, "#b68f40")
        CALIBRAGE_RECT = CALIBRAGE_TEXT.get_rect(center=((window.get_width()/2), window.get_height()/2))

        BOUTON_MODE_1 = c.Button(image=fond_bouton_mode,
                                 pos=((window.get_width() / 2 - 300), window.get_height() / 2 - 125),
                                 text_input='Sans Temps', font=f.get_font(50), base_color=base_color_mode1,
                                 hovering_color=hovering_color_mode1)
        BOUTON_MODE_2 = c.Button(image=fond_bouton_mode,
                                 pos=((window.get_width() / 2 + 300), window.get_height() / 2 - 125),
                                 text_input="Avec Temps", font=f.get_font(50), base_color=base_color_mode2,
                                 hovering_color=hovering_color_mode2)
        BOUTON_CALIBRAGE = c.Button(image=fond_bouton_calibrage,
                                 pos=((window.get_width() / 2), window.get_height() / 2+125),
                                 text_input="Calibrer Caméra", font=f.get_font(50), base_color=base_color_calibrage,
                                 hovering_color=hovering_color_calibrage)
        BOUTON_JOUER = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                pos=((window.get_width() / 1.2), window.get_height() / 1.1),
                                 text_input="JOUER", font=f.get_font(60), base_color=base_color_jouer,
                                 hovering_color=hovering_color_jouer)

        BOUTON_RETOUR = f.retour_button_generator(window)

        window.blit(CHOIX_TEXT, CHOIX_RECT)
        window.blit(CALIBRAGE_TEXT, CALIBRAGE_RECT)


        for button in [BOUTON_MODE_1,BOUTON_MODE_2,BOUTON_RETOUR,BOUTON_CALIBRAGE,BOUTON_JOUER]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(window)

        if f.coord[0][3] != -10:
            hovering_color_calibrage = "#b68f40"
            base_color_calibrage = "#FFD700"

        if (f.coord[0][3] != -10) and mode_select != 0:
            hovering_color_jouer = "#00adf0"
            base_color_jouer = "#0088f0"

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME
            if event.type == pygame.KEYDOWN:    # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:    # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread.set()               # des windows opencv + reset des coords pts calibrage
                    f.reset_coord()
                    main_menu(window)
                if event.key == pygame.K_q:
                    stop_thread.set()
                    pygame.quit()
                    sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:  # EVENT clique souris
                if BOUTON_RETOUR.checkForInput(pygame.mouse.get_pos()):  # SI clique sur bouton retour alors ramène au menu du jeu
                    stop_thread.set()               # des windows opencv + reset des coords pts calibrage
                    f.reset_coord()
                    main_menu(window)

                if BOUTON_MODE_1.checkForInput(pygame.mouse.get_pos()):
                    base_color_mode1 = "#FFD700"
                    hovering_color_mode1 = "#b68f40"
                    base_color_mode2 = 'white'
                    hovering_color_mode2 = "#d7fcd4"
                    mode_select = 1

                if BOUTON_MODE_2.checkForInput(pygame.mouse.get_pos()):
                    base_color_mode1 = "white"
                    hovering_color_mode1 = "#d7fcd4"
                    base_color_mode2 = "#FFD700"
                    hovering_color_mode2 = "#b68f40"
                    mode_select = 2

                if BOUTON_CALIBRAGE.checkForInput(pygame.mouse.get_pos()):
                    if f.coord[0][3] == -10:    # Lance le thread pour le calibrage
                        thread_window_cv2 = threading.Thread(target=thread_cv2)  # Création thread pour la calibrage de la perspective
                        thread_window_cv2.start()  # Démarrage du thread

                if BOUTON_JOUER.checkForInput(pygame.mouse.get_pos()) and (f.coord[0][3] != -10) and mode_select != 0:
                    jouer(window,mode_select)



            elif event.type == VIDEORESIZE:
                if window.get_width() < 1152:
                    window = pygame.display.set_mode((1152, window.get_height()), pygame.RESIZABLE)
                    pygame.display.update()
                elif window.get_height() < 648:
                    window = pygame.display.set_mode((window.get_width(), 648), pygame.RESIZABLE)
                    pygame.display.update()
                else:
                    window = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    window.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
                    pygame.display.flip()

        window.blit(cursor, pygame.mouse.get_pos())  # Affichage de l'image suivant le cursuer  permetant un curseur custom

        pygame.display.update()  # Actualise la fenêtre
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),(0, 0))  # Resizing du background pour match le taille de la window


# ==================================================================================================================== #

# ==================================================================================================================== #


def jouer(window,mode_select):  # Fonction ''JOUER'' Gameplay + affichage de l'interface de jeu

    SCORE_BACKGROUND = f.fond_resize(700,85)

    score_value = 0 # Valeur du score initilisé à 0
    rect = pygame.Rect(200, 200, 200, 200);


    while True:

        x_ball, y_ball = f.get_ball_coord(window.get_width(), window.get_height())

        if rect.collidepoint(x_ball, y_ball):
            x = random.randrange(window.get_width())
            y = random.randrange(window.get_height())
            rect.center = (x, y);
            score_value += 1
        elif rect.x > window.get_width() or rect.y > window.get_height():
            x = random.randrange(window.get_width())
            y = random.randrange(window.get_height())
            rect.center = (x, y);

        for event in pygame.event.get():    # LECTURE DES EVENT DANS LA FENETRE DE JEU PYGAME
            if event.type == pygame.QUIT:   # Evenement quitter la fenetre (croix en haut à doitre)
                stop_thread.set()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:    # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:    # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread.set()               # des windows opencv + reset des coords pts calibrage
                    f.reset_coord()
                    main_menu(window)
                if event.key == pygame.K_q:
                    stop_thread.set()
                    pygame.quit()
                    sys.exit()

            elif event.type == VIDEORESIZE:     #jouer EVENT changement taille fenêtre  (Le min / max font en sorte qu'au minimum la fenêtre reste en 19:9)
                if window.get_width() < 1152:   # Si largeur < au minimum taille fenêtre alors resize au minimum
                    window = pygame.display.set_mode((1152, window.get_height()), pygame.RESIZABLE)
                    pygame.display.update()
                elif window.get_height() < 648:     # Si hautuer < au minimum taille fenêtre alors resize au minimum
                    window = pygame.display.set_mode((window.get_width(), 648), pygame.RESIZABLE)
                    pygame.display.update()
                else:       # SI resize supérieur au minimum alors resize le background en conséquence par rapport à la nouvelle taille fenêtre
                    window = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    window.blit(pygame.transform.scale(background, event.dict['size']), (0, 0)) # Resizing du fond
                    pygame.display.update()

        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0)) # Resizing du background pour match le taille de la window

        pygame.draw.circle(window, (255, 255, 0), rect.center, 200, 200)  # Déssine cercles jaune à des coordonée random contenu dans ''rect.cent''
        window.blit(SCORE_BACKGROUND, ((window.get_width() / 120), window.get_height() / 50))   # Affichage constant FOND score
        show_score(30, 30, score_value, window)     # Affichage constant du score pour qu'il s'actualise


        window.blit(cursor, pygame.mouse.get_pos())     # Affichage de l'image suivant le cursuer  permetant un curseur custom

        pygame.display.update()     # Actualise la fenêtre


# ==================================================================================================================== #

# ==================================================================================================================== #


def regles(window): # Fenêtre règles / comment jouer / touches utilisable

    while True:

        BOUTON_RETOUR = f.retour_button_generator(window)

        for event in pygame.event.get():    # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME
            if event.type == pygame.KEYDOWN:    # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:    # SI touche = ECHAP alors retour au menu du jeu
                    main_menu(window)
                if event.key == pygame.K_q:  # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread.set()
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:    # EVENT clique souris
                if BOUTON_RETOUR.checkForInput(pygame.mouse.get_pos()): # SI clique sur bouton retour alors ramène au menu du jeu
                    main_menu(window)

            elif event.type == VIDEORESIZE:
                if window.get_width() < 1152:
                    window = pygame.display.set_mode((1152, window.get_height()), pygame.RESIZABLE)
                    pygame.display.update()
                elif window.get_height() < 648:
                    window = pygame.display.set_mode((window.get_width(), 648), pygame.RESIZABLE)
                    pygame.display.update()
                else:
                    window = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    window.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
                    pygame.display.flip()

        BOUTON_RETOUR.changeColor(pygame.mouse.get_pos())
        BOUTON_RETOUR.update(window)

        window.blit(cursor, pygame.mouse.get_pos())  # Affichage de l'image suivant le cursuer  permetant un curseur custom

        pygame.display.update()     # Actualise la fenêtre
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0)) # Resizing du background pour match le taille de la window


