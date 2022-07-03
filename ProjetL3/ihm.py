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

# ==================================================================================================================== #


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"font.ttf", size)

# ==================================================================================================================== #


def show_score(x, y, score_value, window):
    score = get_font(60).render("Score : " + str(score_value), True, "#b68f40")
    window.blit(score, (x, y))

# ==================================================================================================================== #

# ==================================================================================================================== #


def main_menu(window):  # Menu du Jeu

    pygame.display.set_caption("Insect Touch")

    window.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))

    pygame.mouse.set_visible(False)

    pygame.display.set_caption("Menu")

    while True:

        MENU_TEXT = get_font(100).render("BUG Touch", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 9))

        BOUTTON_JOUER = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                 pos=((window.get_width() / 2), window.get_height() / 2 - 125),
                                 text_input='JOUER', font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTTON_REGLES = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                  pos=((window.get_width() / 2), window.get_height() / 2 + 25),
                                  text_input="REGLES", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTTON_QUITTER = c.Button(image=pygame.image.load(r'Play Rect.png'),
                                   pos=((window.get_width() / 2), window.get_height() / 2 + 175),
                                   text_input="QUITTER", font=get_font(50), base_color="#d7fcd4",
                                   hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [BOUTTON_JOUER, BOUTTON_REGLES, BOUTTON_QUITTER]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(window)

        for event in pygame.event.get():
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
                if BOUTTON_JOUER.checkForInput(pygame.mouse.get_pos()):
                    jouer(window)
                if BOUTTON_REGLES.checkForInput(pygame.mouse.get_pos()):
                    regles(window)
                if BOUTTON_QUITTER.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        window.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))

# ==================================================================================================================== #


def jouer(window):

    SCORE_BACKGROUND_IMAGE = pygame.image.load(r'Play Rect.png')
    SCORE_BACKGROUND = pygame.transform.scale(SCORE_BACKGROUND_IMAGE, (700, 85))

    score_value = 0
    rect = pygame.Rect(60, 60, 60, 60);

    cap = cv2.VideoCapture(0)  # Création objet de la class ''cv2 VideoCapture'' nommé ''cap'', c'est via cette class que l'on accède à la caméra / webcam
    cv2.startWindowThread()



    while True:

        _, frame = cap.read()  # Lecture du flux vidéo de la caméra ou webcam, return True si lu correctement, False dans le cas contraire

        f.draw_point(frame)  # Fonction qui permet de placer les points pour la calibration. Une fois les 4 points
                             # placé elle appelle la fonction ''change_perspective'' qui générera une nouvelle fenêtre avac une perspective à plat

        cv2.imshow("Frame", frame)  # Affiche la fenêtre de capture de la webcam

        cv2.setMouseCallback('Frame', f.click_event)  # Event Click souris sur le fenêtre de vidéo principal

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cap.release()
                    cv2.destroyAllWindows()
                    f.reset_coord()
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
                    pygame.display.update()

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if rect.collidepoint(event.pos):
                    x = random.randrange(window.get_width())
                    y = random.randrange(window.get_height())
                    rect.center = (x, y);
                    score_value += 1
                elif rect.x > window.get_width() or rect.y > window.get_height():
                    x = random.randrange(window.get_width())
                    y = random.randrange(window.get_height())
                    rect.center = (x, y);

        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))

        pygame.draw.circle(window, (255, 255, 0), rect.center, 50, 50)
        window.blit(SCORE_BACKGROUND, ((window.get_width() / 120), window.get_height() / 50))
        show_score(30, 30, score_value, window)


        window.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()

# ==================================================================================================================== #


def regles(window):
    while True:

        fond_RETOUR = pygame.image.load(r'Play Rect.png')

        BOUTTON_RETOUR = c.Button(image=pygame.transform.scale(fond_RETOUR, (300, 100)),
                                  pos=((window.get_width() / 7.75), window.get_height() / 1.1),
                                  text_input='RETOUR', font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        BOUTTON_RETOUR.changeColor(pygame.mouse.get_pos())
        BOUTTON_RETOUR.update(window)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(window)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOUTTON_RETOUR.checkForInput(pygame.mouse.get_pos()):
                    main_menu(window)

        window.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))
