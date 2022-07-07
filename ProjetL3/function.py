import cv2  # Import de la bibliothèque OpenCV
import numpy as np  # Import de la bibliothèque nunPy
import pygame, sys, argparse, imutils, random, time
from pygame.locals import *

from collections import deque

import class_file as c

coord = [[-10, -10, -10, -10], [-10, -10, -10,-10]]  # Array des coordonnées des 4 points de la surface de Jeux à recalibrer (changer de perspective)
flag = 0  # Variable servant de compteur pour le nombre de coordonnées sélectionné (4 max pour les 4 points formant la zone sur laquelle la perspective sera modifié)

# Création des arguments parse + analyse les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

redLower = (170, 100, 100)  # Limite max et min pour la détection de la balle rouge pour HSV
redUpper = (179, 255, 255)
pts = deque(maxlen=args["buffer"])  # Initialisation des points de suivi de la balle (coord x et y)

x_ball = -200  # Variable prenant la coord 'X' de la balle détecté (-200 = valeur de basse quand pas détecté)
y_ball = -200  # Variable prenant la coord 'Y' de la balle détecté (-200 = valeur de basse quand pas détecté)

Fullscreen = False



# ==================================================================================================================== #

# ==================================================================================================================== #


def image_resize(x, y, nom_image):
    image = pygame.image.load(nom_image)  # Loading de l'image de fond pour le score (rectangle transparent)
    image = pygame.transform.scale(image,(x, y))  # Resizing de l'image de fond pour le score par rapport au para 'x' et 'y'
    return image  # équivalent au nouveau format du fond


def fond_resize(x, y):
    fond = pygame.image.load(r'Play Rect.png')  # Loading de l'image de fond pour le score (rectangle transparent)
    fond = pygame.transform.scale(fond,(x, y))  # Resizing de l'image de fond pour le score par rapport au para 'x' et 'y'
    return fond  # équivalent au nouveau format du fond


# ==================================================================================================================== #

# ==================================================================================================================== #


def reset_coord():
    global flag
    flag = 0  # Reset ''FLAG'' indiquant qu'aucune coord n'a été saisis
    for i in range(0, 4):  # Réinitialise-les coords des 4 points pour le calibrage
        coord[0][i] = -10
        coord[1][i] = -10


# ==================================================================================================================== #

# ==================================================================================================================== #


def draw_point(frame):  # Fonction permettant le dessin des points pour la calibration avec la fenêtre ''frame'' en paramètre

    if coord[0][3] == -10:
        for i in range(0, 4):  # Boucle allant de 0 jusqu'à 3 pour les 4 points
            cv2.circle(frame, (coord[0][i], coord[1][i]), 5, (0, 0, 255),cv2.FILLED)  # Fonction pour le dessin des points avec en arguments :
    if coord[0][3] != -10:  # Si coord du 4ème points différent de celle de basse               # NomDeLaFenêtre | coordonnée X,Y | RadiusCercle | CouleurRGB | RemplissageDuCercle
        change_perspective(frame)  # Alors tous les points sont placés => appelle fonction ''change_perspective''


# ==================================================================================================================== #

# ==================================================================================================================== #


def change_perspective(frame):  # Fonction permettant le changement de perspective + l'affichage de celle-ci avec la fenêtre ''frame'' en paramètre

    width, height = 800, 450    # Largeur et Hauteur de la fenêtre affichant la perspective tranformé
    pts1 = np.float32([[coord[0][0],coord[1][0]],[coord[0][1],coord[1][1]],[coord[0][2],coord[1][2]],[coord[0][3],coord[1][3]]])    # pts1 contient les coord des points sélectionnés dans ''draw_point''
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])      # pts2 contient la caractéristique de la fenêtre d'affichage de la nouvelle perspective

    matrix = cv2.getPerspectiveTransform(pts1,pts2)     # Fonction permettant le changement de perspective prenant en argument "pts1" et "pts2"
    output = cv2.warpPerspective(frame, matrix, (width, height))    # Fonction appliquant la transformation de la perspective en image

    detect_ball(output)

    cv2.imshow("output image", output)  # affiche la fenêtre avec la perspective à plat de la zone sélectionner


# ==================================================================================================================== #

# ==================================================================================================================== #


def detect_ball(output):  # MODULE DE DETECTION DE BALLE ROUGE

    blurred = cv2.GaussianBlur(output, (11, 11),0)  # Floute la window output et la convertie en un espace de couleur HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, redLower, redUpper)  # Construit un masque pour la couleur ''rouge''
    mask = cv2.erode(mask, None, iterations=2)  # Effectue une série de dilatations et d'érosions pour supprimer
    mask = cv2.dilate(mask, None, iterations=2)  # toutes les petites taches laissées dans le masque

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  # Trouve le contour de la balle dans le mask et trouve-les coords 'X' et 'Y'
    center = None  # correspondant au centre de la balle

    if len(cnts) > 0:  # SI un contour est trouvé, C.A.D une balle
        contour_select = max(cnts, key=cv2.contourArea)  # Selectionne le plus gros contour (plus grosse balle)
        ((x, y), radius) = cv2.minEnclosingCircle(contour_select)
        M = cv2.moments(contour_select)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        set_ball_coord(x, y)  # SET les coords de la balle à chaque fois qu'elle est détecté

        if radius > 10:  # Si le rayon répond à une taille minimale
            cv2.circle(output, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(output, center, 5, (0, 0, 255), -1)  # Dessine un cercle jaune autour de la balle
    else:
        global x_ball, y_ball  # Quand pas de balle trouvée reset les coords 'x' et 'y' de la balle
        x_ball = -200
        y_ball = -200

    # Update emplacement du point rouge centrale de la balle
    pts.appendleft(center)


def set_ball_coord(x, y):
    global x_ball, y_ball
    x_ball = x
    y_ball = y

def get_ball_coord(largeur_window_jeu, hauteur_window_jeu):
    new_x = (x_ball*largeur_window_jeu)/800
    new_y = (y_ball*hauteur_window_jeu)/450
    return(new_x,new_y)



# ==================================================================================================================== #

# ==================================================================================================================== #


def click_event(event, x, y, flags, params):  # Fonction appelée lors d'un clique souris
    if event == cv2.EVENT_LBUTTONDOWN:  # Condition ''SI'' Clique Gauche souris
        global flag  # Variable Global permettant le décompte du nombre de points posé afin de comptabiliser les coords sélectionnés
        if flag <= 3:  # Condition ''SI'' flag <= 3 alors il reste encore des points de coord à saisir, si > alors tous les points ont été choisis
            coord[0][flag] = x  # Remplissage de l'array coords avec la coord 'X' de l'emplacement ou a été effectués le clique souris
            coord[1][flag] = y  # Remplissage de l'array coords avec la coord 'Y' de l'emplacement ou a été effectué le clique souris
            flag = flag + 1  # Incrémentation de ''flag'', signifiant qu'une coord a été enregistré


# ==================================================================================================================== #

# ==================================================================================================================== #


def retour_button_generator(window):
    fond_RETOUR = pygame.image.load(r'Play Rect.png')  # Rectangle transparent servant de fond pour le bouton ''RETOUR''
    bouton_retour = c.Button(image=pygame.transform.scale(fond_RETOUR, (250, 80)),  # Création bouton ''RETOUR''
                             pos=((window.get_width() / 7.75), window.get_height() / 1.1),
                             text_input='RETOUR', font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    bouton_retour.changeColor(pygame.mouse.get_pos())  # SI le curseur passe sur le bouton → changement couleur
    bouton_retour.update(window)  # UPDATE du bouton ''RETOUR''
    return bouton_retour


# ==================================================================================================================== #

# ==================================================================================================================== #


def get_font(size):  # Return la taille de police souhaitée
    return pygame.font.Font(r"font.ttf", size)


# ==================================================================================================================== #

# ==================================================================================================================== #


def python_fullscreen_event(event, window, monitor_size):

    global Fullscreen

    if event.type == KEYDOWN:
        if event.key == K_f:
            Fullscreen = not Fullscreen
            if Fullscreen:
                pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            else:
                pygame.display.set_mode((window.get_width(), window.get_height()))

# ==================================================================================================================== #

# ==================================================================================================================== #


def python_quitWindow_event(event):
    if event.type == pygame.KEYDOWN:  # EVENT APPUIE TOUCHE CLAVIER
        if event.key == pygame.K_q:  # SI touche = ECHAP alors arrêt du jeu
            pygame.quit()
            sys.exit()

    if event.type == pygame.QUIT:  # Evenement quitter la fenêtre (croix en haut à droite)
        pygame.quit()
        sys.exit()

# ==================================================================================================================== #

# ==================================================================================================================== #


def generate_coord(window):
    x = random.randint(115, window.get_width() - 115)  # Randomize nouvelle coord X avec max largeur de la fenêtre

    y = random.randint(65, window.get_height() - 65)  # Randomize nouvelle coord Y avec max hauteur de la fenêtre

    rect_center = (x, y)  # ''rect.center'' équivaut aux coord du moskito

    return rect_center

# ==================================================================================================================== #

# ==================================================================================================================== #



