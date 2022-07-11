import threading
import time
import pygame, sys
import cv2  # Import de la bibliothèque OpenCV

import function as f
import bouton as b
import mobs

cursor = pygame.image.load(r"Ressources/cursor.png")  # Chargement image du curseur custom
cursor = pygame.transform.scale(cursor, (50, 50))  # Changement de la taille du curseur
background = pygame.image.load(r'Ressources/fond.png')  # Chargement image de fond

moskigros = f.image_resize(200, 200, r'Ressources/Moskigros_violet.png')  # Chargement image Moskigros Entraînement

stop_thread_detect_ball = threading.Event()  # Initialisations variables permettant l'arrêt des threads
stop_thread_countdown = threading.Event()

kill_cooldown = 0  # Variable Kill Cooldown pour mode Entraînement
score_value = 0  # Valeur du score pour les deux modes de jeu
time_value = 0  # Temps indiqué en secondes
time_value_min_sec = 0  # Temps indiqué convertis en mins / secs
flag_in_game = 0  # Flag indiquant fin du jeu quand Temps
flag_calibrage = 0  # Flag indiquant si le calibrage est fait


# ==================================================================================================================== #

# ==================================================================================================================== #


def main_menu(window):  # Menu du Jeu

    monitor_size = [pygame.display.Info().current_w,
                    pygame.display.Info().current_h]  # Récupération de la taille de l'écran

    window.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))  # Affiche le fond

    pygame.mouse.set_visible(False)  # Désactive la visibilité du curseur de base (souris blanche)

    pygame.display.set_caption("Menu")  # Change le nom de la fenêtre pour "Menu"

    MENU_TEXT = f.get_font(100).render("BUG Touch", True, "#b68f40")  # Texte Menu ''BUG Touch''
    MENU_RECT = MENU_TEXT.get_rect(
        center=((window.get_width() / 2), window.get_height() / 9))  # Placement du rect contenant le text du menu

    BOUTON_JOUER = b.Button(image=pygame.image.load(r'Ressources/Play Rect.png'),  # Création du ''BOUTON_JOUER''
                            pos=((window.get_width() / 2), window.get_height() / 2 - 125),
                            text_input='JOUER', font=f.get_font(40), base_color="#d7fcd4", hovering_color="White")
    BOUTON_REGLES = b.Button(image=pygame.image.load(r'Ressources/Play Rect.png'),  # Création du ''BOUTON_REGLES''
                             pos=((window.get_width() / 2), window.get_height() / 2 + 25),
                             text_input="REGLES", font=f.get_font(40), base_color="#d7fcd4", hovering_color="White")
    BOUTON_QUITTER = b.Button(image=pygame.image.load(r'Ressources/Play Rect.png'),  # Création du ''BOUTON_QUITTER''
                              pos=((window.get_width() / 2), window.get_height() / 2 + 175),
                              text_input="QUITTER", font=f.get_font(40), base_color="#d7fcd4",
                              hovering_color="White")

    while True:

        for button in [BOUTON_JOUER, BOUTON_REGLES, BOUTON_QUITTER]:  # Actualise l'affichage de tout les
            button.change_color(pygame.mouse.get_pos())  # boutons du menu
            button.update(window)

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME

            f.python_fullscreen_event(event, window, monitor_size)
            f.python_quitWindow_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:  # Check clique souris sour un des boutons du Menu
                if BOUTON_JOUER.check_for_input(pygame.mouse.get_pos()):
                    choix_mode_jeu(window, monitor_size)  # Chargement interface ''choix_mode_jeu''
                if BOUTON_REGLES.check_for_input(pygame.mouse.get_pos()):
                    regles(window, monitor_size)  # Chargement interface ''regles''
                if BOUTON_QUITTER.check_for_input(pygame.mouse.get_pos()):
                    pygame.quit()  # Quite le Jeu
                    sys.exit()

        window.blit(MENU_TEXT, MENU_RECT)  # Affichage du text ''BUG Touch'' du menu

        window.blit(cursor, pygame.mouse.get_pos())  # Affichage du curseur customisé

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))
        # Actualisation du fond d'écran en fonction de la taille de la fenêtre


# ==================================================================================================================== #

# ==================================================================================================================== #


def thread_detectBall():  # FONCTION CALIBRAGE PERSPECTIVE CAMERA

    cap = cv2.VideoCapture(0,
                           cv2.CAP_DSHOW)  # Création objet de la class ''cv2 VideoCapture'' nommé ''cap'', c'est via cette class que l'on accède à la caméra / webcam

    global score_value, flag_calibrage

    while True:

        global kill_cooldown

        if kill_cooldown == 1:  # Si kill cooldown Up alors on peu tuer un moskito
            kill_cooldown = 0  # Kill CV = 0 empêchant un second kill dans un interval d'1 sec
            score_value += 1  # Augmente le score de '1'
            time.sleep(1)

        _, frame = cap.read()  # Lecture du flux vidéo de la caméra ou webcam, return True si lu correctement, False dans le cas contraire

        f.draw_point(frame)  # Fonction qui permet de placer les points pour la calibration. Une fois les 4 points
        # placé elle appelle la fonction ''change_perspective'' qui générera une nouvelle fenêtre avec une perspective à plat

        cv2.imshow("Frame", frame)  # Affiche la fenêtre de capture de la webcam
        cv2.setMouseCallback('Frame', f.click_event)  # Event Click souris sur la fenêtre de vidéo principal

        cv2.waitKey(1)

        if stop_thread_detect_ball.is_set():  # SI ''stop_thread.is_set'' alors arrête du thread et fermeture des windows OpenCV
            cap.release()
            cv2.destroyAllWindows()
            stop_thread_detect_ball.clear()
            flag_calibrage = 0
            break


# ==================================================================================================================== #

# ==================================================================================================================== #

def jouer(window, mode_select, select_temps, monitor_size,
          selected_time_value):  # Fonction ''JOUER'' Gameplay + affichage de l'interface de jeu

    SCORE_BACKGROUND = f.fond_resize(425, 55)

    global time_value, flag_in_game, score_value

    FOND_BOUTON_RETOUR_MENU = f.fond_resize(600, 65)
    BOUTON_RETOUR_MENU = b.Button(FOND_BOUTON_RETOUR_MENU,
                                  pos=((window.get_width() / 2), window.get_height() / 1.15),
                                  text_input="Retour Menu", font=f.get_font(40), base_color="#d7fcd4",
                                  hovering_color="White")

    if select_temps == 2:  # Mode sélectionné Avec Temps

        FOND_FIN_JEU = f.fond_resize(950, 600)  # Initialisation des éléments composant la fenêtre de fin du jeu
        stop_thread_countdown.clear()  # Lorsque le temps et à zéro
        flag_in_game = 1
        TIME_BACKGROUND = f.fond_resize(475, 55)
        coutdown = threading.Thread(target=thread_coutdown, args=(selected_time_value,))
        coutdown.start()  # Lance le thread permettant le décompte du jeu

    if mode_select == 1:  # SI mode entraînement sélectionné
        rect_hitbox_moskigros_entrainement = pygame.Rect(0, 0, 250, 250)  # Première initialisation du moskigros
        rect_hitbox_moskigros_entrainement.center = f.generate_coord(window)  # Entraînement
        global kill_cooldown

    if mode_select == 2:  # SI Mode SAUV'Ki'Piou sélectionné
        mobs_class = mobs.mobs_class(selected_time_value)  # Initialisation d'un Objet mob_class
        # Update et spawn de mobs est prise en charge dans cet objet
    while True:

        x_ball, y_ball = f.get_ball_coord(window.get_width(), window.get_height())
        # Récupération coord balle, si différent de -200 alors une balle a été détectée

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DE JEU PYGAME
            if event.type == pygame.QUIT:  # Evenement quitter la fenetre (croix en haut à droite)
                stop_thread_detect_ball.set()   # SET() = Stop Thread
                stop_thread_countdown.set()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:  # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread_detect_ball.set()  # des windows opencv + reset des coords pts calibrage
                    stop_thread_countdown.set()  # SET() = Stop Thread
                    f.reset_coord()
                    time_value = 0
                    score_value = 0
                    if mode_select == 2:    # Reset valeur mode de jeu SAUV'Ki'Piou
                        mobs_class.score_value_mobs = 0

                        for mob in mobs_class.list_mobs:    # Suppression de tous les objets de la list_mobs
                            mobs_class.list_mobs.remove(mob)  # Elle est composée de Moskito, Moskigros et de Pious

                    main_menu(window)
                if event.key == pygame.K_q:  # SI touche = ''q'' alors arrêt du jeu + du thread window opencv
                    stop_thread_detect_ball.set()  # SET() = Stop Thread
                    stop_thread_countdown.set()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    # BOUTON Retour au menu de l'onglet fin du jeu mode avec TEMPS
                if BOUTON_RETOUR_MENU.check_for_input(pygame.mouse.get_pos()) and flag_in_game == 0:
                    time_value = 0
                    score_value = 0
                    if mode_select == 2:    # SI Mode SAUV'Ki'Piou alors Reset tous les variables
                        mobs_class.score_value_mobs = 0

                        for mob in mobs_class.list_mobs:
                            mobs_class.list_mobs.remove(mob)

                    main_menu(window)  # Retour au menu de jeu

            f.python_fullscreen_event(event, window, monitor_size)  # Evenement Fullscreen SI 'f' pressé

        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),
                    (0, 0))  # Resizing du background pour match le taille de la window

        # ==================================================================================================================== #
        # MODE JEU ENTRAINEMENT
        if mode_select == 1:

            window.blit(moskigros, rect_hitbox_moskigros_entrainement.center)   # Affichage du Moskigros mode Entraînement

            if rect_hitbox_moskigros_entrainement.collidepoint(x_ball,y_ball):  # SI collision entre moskito et coord balle
                rect_hitbox_moskigros_entrainement.center = f.generate_coord(window)
                kill_cooldown = 1

            elif rect_hitbox_moskigros_entrainement.x > window.get_width() or rect_hitbox_moskigros_entrainement.y > window.get_height():
                rect_hitbox_moskigros_entrainement.center = f.generate_coord(window)
                # SI le Moskigros apparait en dehors de la fenêtre alors on relance le générateur de coordonnée jusqu'à
                # ce qu'il soit dans la fenêtre

        # ==================================================================================================================== #
        # MODE JEU SAUV KI PIOU

        if mode_select == 2:
            mobs_class.update_mobs(window)  # Méthode Update de l'objet mobs_class, c'est dans update que s'effectue
            score_value = mobs_class.get_score_value()  # le spawn des moustiques et le check collisions avec la balle

        # ==================================================================================================================== #
        # MODE JEU AVEC TEMPS

        if select_temps == 2:
            window.blit(TIME_BACKGROUND, ((window.get_width() / 1.620), window.get_height() / 85))
            countdown = f.get_font(35).render("Temps : " + str(time_value), True, "#b68f40")
            window.blit(countdown, (800, 20))   # Affichage de l'interface Temps avec décompte

            if flag_in_game == 0:   # SI FLAG == 0 alors temps écoulé
                stop_thread_detect_ball.set()  # Arrêt des threads
                stop_thread_countdown.set()
                f.reset_coord()

                window.blit(FOND_FIN_JEU, (165, 80))    # Affichage Interface fin de jeu Mode Avec temps

                SCORE_TEXT_OBTENUE = f.get_font(70).render("Score Obtenu", True, "#b68f40")
                window.blit(SCORE_TEXT_OBTENUE, (210, 100))

                # Affichage différent en fonctions du nombre de points gagné, dépendant du nombre de points amassé
                # l'affichage serra différente pour centrer le score.
                if score_value < 0:
                    SCORE_TEXT_VALUE = f.get_font(350).render(str(score_value), True, "#b68f40")
                    window.blit(SCORE_TEXT_VALUE, (window.get_width() / 4.2, window.get_height() / 3.1))
                elif score_value < 10:
                    SCORE_TEXT_VALUE = f.get_font(350).render(str(score_value), True, "#b68f40")
                    window.blit(SCORE_TEXT_VALUE, (window.get_width() / 2.7, window.get_height() / 3.1))
                else:
                    SCORE_TEXT_VALUE = f.get_font(350).render(str(score_value), True, "#b68f40")
                    window.blit(SCORE_TEXT_VALUE, (window.get_width() / 4.2, window.get_height() / 3.1))

                BOUTON_RETOUR_MENU.change_color(pygame.mouse.get_pos())
                BOUTON_RETOUR_MENU.update(window)   # SI curseur survole bouton retour alors changement de couleur text

                window.blit(cursor,pygame.mouse.get_pos())  # Affichage de l'image suivant le curseur permettant un curseur custom

        # ==================================================================================================================== #

        window.blit(SCORE_BACKGROUND,((window.get_width() / 120), window.get_height() / 85))  # Affichage constant FOND score
        show_score(20, 20, 35, score_value, window)  # Affichage constant du score pour qu'il s'actualise

        pygame.display.update()  # Actualise la fenêtre


# ==================================================================================================================== #

# ==================================================================================================================== #

def thread_coutdown(time_sec):  # Thread pour décompte du temps
    global time_value, flag_in_game

    while time_sec > -1:    # Tant qu'il reste du temps
        mins, secs = divmod(time_sec, 60)   # Conversion nb secondes en minutes et secondes

        time_value = '{:02d}:{:02d}'.format(mins, secs)

        time.sleep(1)
        time_sec -= 1   # - 1 chaque seconde

        if stop_thread_countdown.is_set():  # SI ''stop_thread.is_set'' alors arrête du thread et fermeture des windows OpenCV
            stop_thread_countdown.clear()
            time_value = 0
            break

    flag_in_game = 0    # Indique fin du décompte et donc fin de la parti de jeu


# ==================================================================================================================== #

# ==================================================================================================================== #


def show_score(x, y, size_font, score_value_show, window):  # Fonction d'affichage du score en jeu
    score = f.get_font(size_font).render("Score : " + str(score_value_show), True, "#b68f40")
    window.blit(score, (x, y))


# ==================================================================================================================== #

# ==================================================================================================================== #


def choix_mode_jeu(window, monitor_size):
    global flag_calibrage

    pygame.display.set_caption("Choix mode de Jeu")  # Change le nom de la fenêtre pour "Choix mode de jeu"
    fond_bouton_mode = f.fond_resize(475, 85)  # Retourne ''Play Rect.png'' avec les Largeur et Hauteur indiquer
    fond_bouton_temps = f.fond_resize(115, 50)
    fond_bouton_calibrage = f.fond_resize(650, 85)

    fond_show_time_selected = f.fond_resize(195, 50)

    base_color_temps1 = "#d7fcd4"
    base_color_mode1 = "#d7fcd4"
    hovering_color_temps1 = 'white'
    hovering_color_mode1 = 'white'

    base_color_temps2 = "#d7fcd4"
    base_color_mode2 = "#d7fcd4"
    hovering_color_temps2 = 'white'
    hovering_color_mode2 = 'white'

    base_color_calibrage = "#d7fcd4"
    hovering_color_calibrage = 'white'

    base_color_jouer = "#d7fcd4"
    hovering_color_jouer = 'white'

    select_temps = 0
    mode_select = 0
    selected_time_value = 0

    mins, secs = divmod(selected_time_value, 60)
    time_value_converti = '{:02d}:{:02d}'.format(mins, secs)

    BOUTON_PLUS_TEMPS = b.Button(image=fond_bouton_temps,  # Création du ''BOUTON_SANS_TEMPS''
                                 pos=((window.get_width() / 2 + 260), window.get_height() / 1.95),
                                 text_input='+15', font=f.get_font(30), base_color="#d7fcd4",
                                 hovering_color='white')

    BOUTON_MOINS_TEMPS = b.Button(image=fond_bouton_temps,  # Création du ''BOUTON_SANS_TEMPS''
                                  pos=((window.get_width() / 2 + 130), window.get_height() / 1.95),
                                  text_input='-15', font=f.get_font(30), base_color="#d7fcd4",
                                  hovering_color='white')

    while True:

        SHOW_TOTAL_TIME_TEXT = f.get_font(35).render(time_value_converti, True, 'white')  # Texte Menu ''BUG Touch''
        SHOW_TOTAL_TIME_RECT = SHOW_TOTAL_TIME_TEXT.get_rect(center=((window.get_width() / 2 + 434), window.get_height() / 1.95))  # Placement du rect contenant le text du menu

        CHOIX_TEXT = f.get_font(65).render("Choix Mode de Jeu", True, "#b68f40")  # Création text ''Choix Mode de Jeu''
        CHOIX_RECT = CHOIX_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 10))

        CALIBRAGE_TEXT = f.get_font(65).render("Calibrage", True, "#b68f40")  # Création text ''Calibrage''
        CALIBRAGE_RECT = CALIBRAGE_TEXT.get_rect(center=((window.get_width() / 2), window.get_height() / 2 + 75))

        BOUTON_SANS_TEMPS = b.Button(image=fond_bouton_mode,  # Création du ''BOUTON_SANS_TEMPS''
                                     pos=((window.get_width() / 2 + 300), window.get_height() / 2 - 175),
                                     text_input='Sans Temps', font=f.get_font(35), base_color=base_color_temps1,
                                     hovering_color=hovering_color_temps1)
        BOUTON_AVEC_TEMPS = b.Button(image=fond_bouton_mode,  # Création du ''BOUTON_AVEC_TEMPS''
                                     pos=((window.get_width() / 2 + 300), window.get_height() / 2 - 75),
                                     text_input="Avec Temps", font=f.get_font(35), base_color=base_color_temps2,
                                     hovering_color=hovering_color_temps2)
        BOUTON_CALIBRAGE = b.Button(image=fond_bouton_calibrage,  # Création du ''BOUTON_CALIBRAGE''
                                    pos=((window.get_width() / 2), window.get_height() / 2 + 175),
                                    text_input="Calibrer Caméra", font=f.get_font(35), base_color=base_color_calibrage,
                                    hovering_color=hovering_color_calibrage)
        BOUTON_JOUER = b.Button(image=pygame.image.load(r'Ressources/Play Rect.png'),  # Création du ''BOUTON_JOUER''
                                pos=((window.get_width() / 1.2), window.get_height() / 1.1),
                                text_input="JOUER", font=f.get_font(40), base_color=base_color_jouer,
                                hovering_color=hovering_color_jouer)

        BOUTON_MODE_ENTRAINEMENT = b.Button(image=fond_bouton_mode,  # Création du ''BOUTON_SANS_TEMPS''
                                            pos=((window.get_width() / 2 - 300), window.get_height() / 2 - 175),
                                            text_input='Entraînement', font=f.get_font(35), base_color=base_color_mode1,
                                            hovering_color=hovering_color_mode1)

        BOUTON_SAUV_KI_PIOU = b.Button(image=fond_bouton_mode,  # Création du ''BOUTON_SANS_TEMPS''
                                       pos=((window.get_width() / 2 - 300), window.get_height() / 2 - 75),
                                       text_input="Sauv'Ki'Piou", font=f.get_font(35), base_color=base_color_mode2,
                                       hovering_color=hovering_color_mode2)

        BOUTON_RETOUR = f.retour_button_generator(window)  # Création d'un bouton retour ramenant au menu du jeu

        window.blit(CHOIX_TEXT, CHOIX_RECT)  # Affichage du text ''Choix Mode de Jeu''
        window.blit(CALIBRAGE_TEXT, CALIBRAGE_RECT)  # Affichage du text ''Calibrage''

        for button in [BOUTON_SANS_TEMPS, BOUTON_AVEC_TEMPS, BOUTON_RETOUR, BOUTON_CALIBRAGE,
                       BOUTON_JOUER, BOUTON_MODE_ENTRAINEMENT, BOUTON_SAUV_KI_PIOU]:
            button.change_color(pygame.mouse.get_pos())  # Affichage de tous les boutons du menu ''choix_mode_jeu''
            button.update(window)

        if select_temps == 2:

            window.blit(fond_show_time_selected, (window.get_width() / 2 + 334, window.get_height() / 2 - 16))
            window.blit(SHOW_TOTAL_TIME_TEXT, SHOW_TOTAL_TIME_RECT)  # Affichage du temps sélectionné

            for button in [BOUTON_PLUS_TEMPS, BOUTON_MOINS_TEMPS]:
                button.change_color(pygame.mouse.get_pos())  # Affichage de tous les boutons du menu ''choix_mode_jeu''
                button.update(window)

        if f.coord[0][3] != -10:  # SI coord différent de celle de base alors calibrage fait → changement couleur text bouton
            hovering_color_calibrage = "#b68f40"
            base_color_calibrage = "#FFD700"

        if (f.coord[0][3] != -10) and select_temps != 0 and mode_select != 0 and (
                selected_time_value != 0 or select_temps == 1):  # SI calibrage fait ET mode sélectionné → changement couleur text bouton
            hovering_color_jouer = "#00adf0"  # Le changement de couleur indique qu'il est possible de lancer le jeu
            base_color_jouer = "#0088f0"
        else:
            hovering_color_jouer = 'white'  # Le changement de couleur indique qu'il est possible de lancer le jeu
            base_color_jouer = "#d7fcd4"

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME
            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:  # SI touche = ECHAP alors retour au menu du jeu + fermeture
                    stop_thread_detect_ball.set()  # des windows opencv + reset des coords pts calibrage
                    stop_thread_countdown.set()
                    f.reset_coord()
                    main_menu(window)
                if event.key == pygame.K_q:
                    stop_thread_detect_ball.set()
                    stop_thread_countdown.set()
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEMOTION:
                window.blit(cursor, pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN:  # EVENT clique souris
                if BOUTON_RETOUR.check_for_input(
                        pygame.mouse.get_pos()):  # SI clique sur bouton retour alors ramène au menu du jeu
                    stop_thread_detect_ball.set()  # des windows opencv + reset des coords pts calibrage
                    stop_thread_countdown.set()
                    f.reset_coord()
                    main_menu(window)

                if BOUTON_SANS_TEMPS.check_for_input(pygame.mouse.get_pos()):  # Check SI le bouton a été sélectionné
                    base_color_temps1 = "#FFD700"
                    hovering_color_temps1 = "#b68f40"
                    base_color_temps2 = "#d7fcd4"
                    hovering_color_temps2 = "white"
                    select_temps = 1  # Mode sélectionné : 1 => Sans Temps

                if BOUTON_AVEC_TEMPS.check_for_input(pygame.mouse.get_pos()):  # Check SI le bouton a été sélectionné
                    base_color_temps1 = "#d7fcd4"
                    hovering_color_temps1 = "white"
                    base_color_temps2 = "#FFD700"
                    hovering_color_temps2 = "#b68f40"
                    select_temps = 2  # Temps sélectionné : 2 => Avec Temps

                if BOUTON_MODE_ENTRAINEMENT.check_for_input(
                        pygame.mouse.get_pos()):  # Check SI le bouton a été sélectionné
                    base_color_mode1 = "#FFD700"
                    hovering_color_mode1 = "#b68f40"
                    base_color_mode2 = "#d7fcd4"
                    hovering_color_mode2 = "white"
                    mode_select = 1  # Temps sélectionné : 1 => Mode Entraînement

                if BOUTON_SAUV_KI_PIOU.check_for_input(pygame.mouse.get_pos()):  # Check SI le bouton a été sélectionné
                    base_color_mode1 = "#d7fcd4"
                    hovering_color_mode1 = "white"
                    base_color_mode2 = "#FFD700"
                    hovering_color_mode2 = "#b68f40"
                    mode_select = 2  # Mode sélectionné : 2 => Mode SAUV KI PIOU => Classique

                if BOUTON_PLUS_TEMPS.check_for_input(pygame.mouse.get_pos()):
                    selected_time_value += 15
                    mins, secs = divmod(selected_time_value, 60)
                    time_value_converti = '{:02d}:{:02d}'.format(mins, secs)

                if BOUTON_MOINS_TEMPS.check_for_input(pygame.mouse.get_pos()):
                    if selected_time_value > 0:
                        selected_time_value -= 15
                    else:
                        selected_time_value = 0

                    mins, secs = divmod(selected_time_value, 60)
                    time_value_converti = '{:02d}:{:02d}'.format(mins, secs)

                if BOUTON_CALIBRAGE.check_for_input(pygame.mouse.get_pos()) and flag_calibrage == 0:
                    if f.coord[0][0] == -10:  # Lance le thread pour le calibrage
                        flag_calibrage = 1
                        thread_window_cv2 = threading.Thread(
                            target=thread_detectBall)  # Création thread pour le calibrage de la perspective
                        thread_window_cv2.start()  # Démarrage du thread

                if BOUTON_JOUER.check_for_input(pygame.mouse.get_pos()) and (
                        f.coord[0][3] != -10) and select_temps != 0 and mode_select != 0 and (
                        selected_time_value != 0 or select_temps == 1):
                    jouer(window, mode_select, select_temps, monitor_size,
                          selected_time_value)  # SI Calibrage ET mode sélectionné → lance le jeu si cliquer

            f.python_fullscreen_event(event, window, monitor_size)

        window.blit(cursor,
                    pygame.mouse.get_pos())  # Affichage de l'image suivant le curseur permettant un curseur custom

        pygame.display.update()  # Actualise la fenêtre
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),
                    (0, 0))  # Resizing du background pour match le taille de la window


# ==================================================================================================================== #

# ==================================================================================================================== #


def regles(window, monitor_size):  # Fenêtre règles / comment jouer / touches utilisables

    pygame.display.set_caption("Règles")

    rule = pygame.image.load(r'Ressources/Rule.png')
    rule = pygame.transform.scale(rule, (1280, 720))

    fond_RETOUR = pygame.image.load(
        r'Ressources/Play Rect.png')  # Rectangle transparent servant de fond pour le bouton ''RETOUR''

    BOUTON_RETOUR = b.Button(image=pygame.transform.scale(fond_RETOUR, (190, 60)),  # Création bouton ''RETOUR''
                             pos=((window.get_width() / 2), window.get_height() / 1.05),
                             text_input='RETOUR', font=f.get_font(20), base_color="#d7fcd4", hovering_color="White")

    while True:

        for event in pygame.event.get():  # LECTURE DES EVENT DANS LA FENETRE DES REGLES PYGAME
            if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
                if event.key == pygame.K_ESCAPE:  # SI touche = ECHAP alors retour au menu du jeu
                    main_menu(window)

            f.python_fullscreen_event(event, window, monitor_size)
            f.python_quitWindow_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:  # EVENT clique souris
                if BOUTON_RETOUR.check_for_input(
                        pygame.mouse.get_pos()):  # SI clique sur bouton retour alors ramène au menu du jeu
                    main_menu(window)

        window.blit(rule, (0, 0))

        BOUTON_RETOUR.change_color(pygame.mouse.get_pos())  # Actualisation du ''BOUTON_RETOUR''
        BOUTON_RETOUR.update(window)

        window.blit(cursor,
                    pygame.mouse.get_pos())  # Affichage de l'image suivant le curseur permettant un curseur custom
        pygame.display.update()  # Actualise la fenêtre
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())),
                    (0, 0))  # Resizing du background pour match le taille de la window
