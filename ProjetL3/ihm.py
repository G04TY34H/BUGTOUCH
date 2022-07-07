import threading
import time

import pygame, sys


import cv2  # Import de la bibliothèque OpenCV

import function as f
import class_file as c

cursor = pygame.image.load(r'cursor.png')
cursor = pygame.transform.scale(cursor, (50, 50))
background = pygame.image.load(r'fond.png')

moskito = f.image_resize(100, 100, r'Moskito.png')
moskigros = f.image_resize(200, 200, r'Moskigros_violet.png')

stop_thread = threading.Event()
kill_cooldown = 0
score_value = 0
time_value = 0
flag_in_game = 0

# ==================================================================================================================== #

# ==================================================================================================================== #


def main_menu(window):  # Menu du Jeu

    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

    pygame.display.set_caption("BUG Touch")

    window.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))

    pygame.mouse.set_visible(False)

    pygame.display.set_caption("Menu")

    while True:

        MENU_TEXT = f.get_font(100).render("BUG Touch", True, "#b68f40")  # Texte Menu ''BUG Touch''
        MENU_RECT = MENU_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 9))  # Placement du rect contenant le text du menu

        BOUTON_JOUER = c.Button(image=pygame.image.load(r'Play Rect.png'),  # Création du ''BOUTON_JOUER''
                                pos=((window.get_width() / 2), window.get_height() / 2 - 125),
                                text_input='JOUER', font=f.get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTON_REGLES = c.Button(image=pygame.image.load(r'Play Rect.png'),  # Création du ''BOUTON_REGLES''
                                 pos=((window.get_width() / 2), window.get_height() / 2 + 25),
                                 text_input="REGLES", font=f.get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTON_QUITTER = c.Button(image=pygame.image.load(r'Play Rect.png'),  # Création du ''BOUTON_QUITTER''
                                  pos=((window.get_width() / 2), window.get_height() / 2 + 175),
                                  text_input="QUITTER", font=f.get_font(50), base_color="#d7fcd4",
                                  hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)  # Affichage du text ''BUG Touch'' du menu

        for button in [BOUTON_JOUER, BOUTON_REGLES, BOUTON_QUITTER]:  # Actualise l'affichage de tout les
            button.changeColor(pygame.mouse.get_pos())  # boutons du menu
            button.update(window)

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME

            f.python_fullscreen_event(event, window, monitor_size)
            f.python_quitWindow_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:  # Check clique souris sour un des boutons du Menu
                if BOUTON_JOUER.checkForInput(pygame.mouse.get_pos()):
                    choix_mode_jeu(window, monitor_size)  # Chargement interface ''choix_mode_jeu''
                if BOUTON_REGLES.checkForInput(pygame.mouse.get_pos()):
                    regles(window, monitor_size)  # Chargement interface ''regles''
                if BOUTON_QUITTER.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()  # Quite le Jeu
                    sys.exit()

        window.blit(cursor, pygame.mouse.get_pos())  # Affichage du curseur customisé

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))
        # Actualisation du fond d'écran en fonction de la taille de la fenêtre


# ==================================================================================================================== #

# ==================================================================================================================== #


def thread_detectBall():  # FONCTION CALIBRAGE PERSPECTIVE CAMERA

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Création objet de la class ''cv2 VideoCapture'' nommé ''cap'', c'est via cette class que l'on accède à la caméra / webcam

    global score_value

    while True:

        global kill_cooldown

        if kill_cooldown == 1:
            kill_cooldown = 0
            score_value += 1  # Augmente le score de '1'
            time.sleep(1)

        _, frame = cap.read()  # Lecture du flux vidéo de la caméra ou webcam, return True si lu correctement, False dans le cas contraire

        f.draw_point(frame)  # Fonction qui permet de placer les points pour la calibration. Une fois les 4 points
        # placé elle appelle la fonction ''change_perspective'' qui générera une nouvelle fenêtre avec une perspective à plat

        cv2.imshow("Frame", frame)  # Affiche la fenêtre de capture de la webcam
        cv2.setMouseCallback('Frame', f.click_event)  # Event Click souris sur la fenêtre de vidéo principal

        cv2.waitKey(1)

        if stop_thread.is_set():  # SI ''stop_thread.is_set'' alors arrête du thread et fermeture des windows OpenCV
            cap.release()
            cv2.destroyAllWindows()
            stop_thread.clear()
            break


# ==================================================================================================================== #

# ==================================================================================================================== #


def jouer(window, mode_select, monitor_size):  # Fonction ''JOUER'' Gameplay + affichage de l'interface de jeu

    SCORE_BACKGROUND = f.fond_resize(425, 55)

    global time_value, flag_in_game, score_value

    if mode_select == 2:

        FOND_FIN_JEU = f.fond_resize(950,600)

        FOND_BOUTON_RETOUR_MENU = f.fond_resize(600, 65)
        BOUTON_RETOUR_MENU = c.Button(FOND_BOUTON_RETOUR_MENU,
                                  pos=((window.get_width()/2), window.get_height() / 1.15),
                                  text_input="Retour Menu", font=f.get_font(40), base_color="#d7fcd4",
                                  hovering_color="White")

        flag_in_game = 1
        TIME_BACKGROUND = f.fond_resize(475, 55)
        coutdown = threading.Thread(target=thread_coutdown, args=(15,))
        coutdown.start()

    rect = pygame.Rect(250, 250, 250, 250)

    rect.center = f.generate_coord(window)

    global kill_cooldown

    while True:

        x_ball, y_ball = f.get_ball_coord(window.get_width(), window.get_height())
        # Récupération coord balle, si différent de -200 alors une balle a été détectée

        if rect.collidepoint(x_ball, y_ball):  # SI collision entre moskito et coord balle
            rect.center = f.generate_coord(window)
            kill_cooldown = 1

        elif rect.x > window.get_width() or rect.y > window.get_height():

            rect.center = f.generate_coord(window)

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DE JEU PYGAME
            if event.type == pygame.QUIT:  # Evenement quitter la fenetre (croix en haut à droite)
                stop_thread.set()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:  # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread.set()               # des windows opencv + reset des coords pts calibrage
                    f.reset_coord()
                    main_menu(window)
                if event.key == pygame.K_q:  # SI touche = ''q'' alors arrêt du jeu + du thread window opencv
                    stop_thread.set()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOUTON_RETOUR_MENU.checkForInput(pygame.mouse.get_pos()) and flag_in_game == 0:
                    score_value = 0
                    main_menu(window)

            f.python_fullscreen_event(event, window, monitor_size)

        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),(0, 0))  # Resizing du background pour match le taille de la window

        window.blit(moskigros, rect.center)

        window.blit(SCORE_BACKGROUND,((window.get_width() / 120), window.get_height() / 85))  # Affichage constant FOND score
        show_score(20, 20,35, score_value, window)  # Affichage constant du score pour qu'il s'actualise

        if mode_select == 2:
            window.blit(TIME_BACKGROUND,((window.get_width() / 1.620), window.get_height() / 85))  # Affichage constant FOND score
            countdown = f.get_font(35).render("Temps : " + str(time_value), True, "#b68f40")
            window.blit(countdown, (800, 20))

            if flag_in_game == 0:
                stop_thread.set()
                f.reset_coord()

                window.blit(FOND_FIN_JEU,(165, 80))

                SCORE_TEXT_OBTENUE = f.get_font(70).render("Score Obtenue", True, "#b68f40")
                window.blit(SCORE_TEXT_OBTENUE, (190, 100))

                SCORE_TEXT_VALUE = f.get_font(350).render(str(score_value), True, "#b68f40")
                window.blit(SCORE_TEXT_VALUE, (window.get_width()/2.7, window.get_height()/3.1))

                BOUTON_RETOUR_MENU.changeColor(pygame.mouse.get_pos())
                BOUTON_RETOUR_MENU.update(window)

                window.blit(cursor,pygame.mouse.get_pos())  # Affichage de l'image suivant le curseur permettant un curseur custom

        pygame.display.update()  # Actualise la fenêtre


# ==================================================================================================================== #

# ==================================================================================================================== #


def thread_coutdown(time_sec):

    global time_value, flag_in_game

    while time_sec > -1:
        mins, secs = divmod(time_sec, 60)

        time_value = '{:02d}:{:02d}'.format(mins, secs)

        time.sleep(1)
        time_sec -= 1

    flag_in_game = 0



# ==================================================================================================================== #

# ==================================================================================================================== #


def show_score(x, y,size_font, score_value, window):  # Fonction d'affichage du score en jeu
    score = f.get_font(size_font).render("Score : " + str(score_value), True, "#b68f40")
    window.blit(score, (x, y))


# ==================================================================================================================== #

# ==================================================================================================================== #


def choix_mode_jeu(window, monitor_size):
    pygame.display.set_caption("Choix mode de Jeu")
    fond_bouton_mode = f.fond_resize(550, 85)  # Retourne ''Play Rect.png'' avec les Largeur et Hauteur indiquer
    fond_bouton_calibrage = f.fond_resize(800, 85)

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

        CHOIX_TEXT = f.get_font(60).render("Choix Modes de Jeu", True, "#b68f40")  # Création text ''Choix Mode de Jeu''
        CHOIX_RECT = CHOIX_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 9))

        CALIBRAGE_TEXT = f.get_font(60).render("Calibrage", True, "#b68f40")  # Création text ''Calibrage''
        CALIBRAGE_RECT = CALIBRAGE_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 2))

        BOUTON_MODE_1 = c.Button(image=fond_bouton_mode,  # Création du ''BOUTON_MODE_1''
                                 pos=((window.get_width() / 2 - 300), window.get_height() / 2 - 125),
                                 text_input='Sans Temps', font=f.get_font(40), base_color=base_color_mode1,
                                 hovering_color=hovering_color_mode1)
        BOUTON_MODE_2 = c.Button(image=fond_bouton_mode,  # Création du ''BOUTON_MODE_2''
                                 pos=((window.get_width() / 2 + 300), window.get_height() / 2 - 125),
                                 text_input="Avec Temps", font=f.get_font(40), base_color=base_color_mode2,
                                 hovering_color=hovering_color_mode2)
        BOUTON_CALIBRAGE = c.Button(image=fond_bouton_calibrage,  # Création du ''BOUTON_CALIBRAGE''
                                    pos=((window.get_width() / 2), window.get_height() / 2 + 125),
                                    text_input="Calibrer Caméra", font=f.get_font(40), base_color=base_color_calibrage,
                                    hovering_color=hovering_color_calibrage)
        BOUTON_JOUER = c.Button(image=pygame.image.load(r'Play Rect.png'),  # Création du ''BOUTON_JOUER''
                                pos=((window.get_width() / 1.2), window.get_height() / 1.1),
                                text_input="JOUER", font=f.get_font(45), base_color=base_color_jouer,
                                hovering_color=hovering_color_jouer)

        BOUTON_RETOUR = f.retour_button_generator(window)  # Création d'un bouton retour ramenant au menu du jeu

        window.blit(CHOIX_TEXT, CHOIX_RECT)  # Affichage du text ''Choix Mode de Jeu''
        window.blit(CALIBRAGE_TEXT, CALIBRAGE_RECT)  # Affichage du text ''Calibrage''

        for button in [BOUTON_MODE_1, BOUTON_MODE_2, BOUTON_RETOUR, BOUTON_CALIBRAGE, BOUTON_JOUER]:
            button.changeColor(pygame.mouse.get_pos())  # Affichage de tous les boutons du menu ''choix_mode_jeu''
            button.update(window)

        if f.coord[0][3] != -10:  # SI coord différent de celle de base alors calibrage fait → changement couleur text bouton
            hovering_color_calibrage = "#b68f40"
            base_color_calibrage = "#FFD700"

        if (f.coord[0][3] != -10) and mode_select != 0:  # SI calibrage fait ET mode sélectionné → changement couleur text bouton
            hovering_color_jouer = "#00adf0"  # Le changement de couleur indique qu'il est possible de lancer le jeu
            base_color_jouer = "#0088f0"

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME
            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:  # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread.set()  # des windows opencv + reset des coords pts calibrage
                    f.reset_coord()
                    main_menu(window)
                if event.key == pygame.K_q:
                    stop_thread.set()
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEMOTION:
                window.blit(cursor, pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN:  # EVENT clique souris
                if BOUTON_RETOUR.checkForInput(pygame.mouse.get_pos()):  # SI clique sur bouton retour alors ramène au menu du jeu
                    stop_thread.set()  # des windows opencv + reset des coords pts calibrage
                    f.reset_coord()
                    main_menu(window)

                if BOUTON_MODE_1.checkForInput(pygame.mouse.get_pos()):  # Check SI le bouton a été sélectionné
                    base_color_mode1 = "#FFD700"
                    hovering_color_mode1 = "#b68f40"
                    base_color_mode2 = 'white'
                    hovering_color_mode2 = "#d7fcd4"
                    mode_select = 1  # Mode sélectionné : 1 => Sans Temps

                if BOUTON_MODE_2.checkForInput(pygame.mouse.get_pos()):  # Check SI le bouton a été sélectionné
                    base_color_mode1 = "white"
                    hovering_color_mode1 = "#d7fcd4"
                    base_color_mode2 = "#FFD700"
                    hovering_color_mode2 = "#b68f40"
                    mode_select = 2  # Mode sélectionné : 2 => Avec Temps

                if BOUTON_CALIBRAGE.checkForInput(pygame.mouse.get_pos()):
                    if f.coord[0][3] == -10:  # Lance le thread pour le calibrage
                        thread_window_cv2 = threading.Thread(target=thread_detectBall)  # Création thread pour le calibrage de la perspective
                        thread_window_cv2.start()  # Démarrage du thread

                if BOUTON_JOUER.checkForInput(pygame.mouse.get_pos()) and (f.coord[0][3] != -10) and mode_select != 0:
                    jouer(window, mode_select,monitor_size)  # SI Calibrage ET mode sélectionné → lance le jeu si cliquer

            f.python_fullscreen_event(event, window, monitor_size)

        window.blit(cursor,pygame.mouse.get_pos())  # Affichage de l'image suivant le curseur permettant un curseur custom

        pygame.display.update()  # Actualise la fenêtre
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),(0, 0))  # Resizing du background pour match le taille de la window


# ==================================================================================================================== #

# ==================================================================================================================== #


def regles(window, monitor_size):  # Fenêtre règles / comment jouer / touches utilisables

    while True:

        BOUTON_RETOUR = f.retour_button_generator(window)  # Création ''BOUTON_RETOUR''

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME
            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:  # SI touche = ECHAP alors retour au menu du jeu
                    main_menu(window)

            f.python_fullscreen_event(event, window, monitor_size)
            f.python_quitWindow_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:  # EVENT clique souris
                if BOUTON_RETOUR.checkForInput(
                        pygame.mouse.get_pos()):  # SI clique sur bouton retour alors ramène au menu du jeu
                    main_menu(window)

        BOUTON_RETOUR.changeColor(pygame.mouse.get_pos())  # Actualisation du ''BOUTON_RETOUR''
        BOUTON_RETOUR.update(window)

        window.blit(cursor,
                    pygame.mouse.get_pos())  # Affichage de l'image suivant le curseur permettant un curseur custom

        pygame.display.update()  # Actualise la fenêtre
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),
                    (0, 0))  # Resizing du background pour match le taille de la window
