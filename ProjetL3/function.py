import cv2  # Import de la bibliothèque OpenCV
import numpy as np  # Import de la bibliothèque nunPy
import pygame
import argparse
import imutils
from collections import deque


import  class_file as c

coord = [[-10,-10,-10,-10],[-10,-10,-10,-10]]   # Array des coordonées des points de la surface de Jeux
flag = 0        # Variable servant de compteur pour le nombre de coordonées sélectionné (4 max pour les 4 points formant la zone sur laquelle la perspective sera modifié)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

greenLower = (170,100,100)
greenUpper = (179, 255, 255)
pts = deque(maxlen=args["buffer"])

x_ball = -200
y_ball = -200

# ==================================================================================================================== #

# ==================================================================================================================== #


def fond_resize(x,y):
    fond = pygame.image.load(r'Play Rect.png')    #Loading de l'image de fond pour le score ( rectangle transparent )
    fond = pygame.transform.scale(fond,(x,y)) #Resizing de l'image de fond pour le score par rapport au para 'x' et 'y'
    return(fond)    # équivalent au nouveau format du fond


# ==================================================================================================================== #

# ==================================================================================================================== #


def reset_coord():
    global flag
    flag = 0    # Reset ''FLAG'' indiquant qu'aucune coord n'a été saisis
    for i in range (0,4):    # Réinitialise les coords des 4 points pour la calibrage
        coord[0][i] = -10
        coord[1][i] = -10


# ==================================================================================================================== #

# ==================================================================================================================== #


def draw_point(frame):  # Fonction permettant le dessin des points pour la calibration avec la fenêtre ''frame'' en paramètre

    if coord[0][3] == -10:
        for i in range (0,4):   # Boucle allant de 0 jusqu'à 3 pour les 4 points
            cv2.circle(frame, ((coord[0][i], coord[1][i])), 5, (0, 0, 255), cv2.FILLED)      # Fonction pour le dessin des points avec en arguments :
    if coord[0][3] != -10:       # Si coord du 4ème points différent de celle de basse               # NomDeLaFenêtre | coordonnée X,Y | RadiusCercle | CouleurRGB | RemplissageDuCercle
        change_perspective(frame)   # Alors tout les points sont placé => appelle fonction ''change_perspective''


# ==================================================================================================================== #

# ==================================================================================================================== #


def change_perspective(frame):  # Fonction permettant le changement de perspective + l'affichage de celle-ci avec la fenêtre ''frame'' en paramètre

    width, height = 1920, 1080    # Largeur et Hauteur de la fenêtre affichant la perspective tranformé
    pts1 = np.float32([[coord[0][0],coord[1][0]],[coord[0][1],coord[1][1]],[coord[0][2],coord[1][2]],[coord[0][3],coord[1][3]]])    # pts1 contient les coord des points sélectionné dans ''draw_point''
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])      # pts2 contient les caractéristique de la fenêtre d'affichage de la nouvelle perspective

    matrix = cv2.getPerspectiveTransform(pts1,pts2)     # Fonction permetant le changement de perspective prenant en argunment "pts1" et "pts2"
    output = cv2.warpPerspective(frame, matrix, (width, height))    # Fonction appliquant la transformation de la perspective en image

    detect_ball(output)

    cv2.imshow("output image", output)  # affiche la fenêtre avec la perspective à plat de la zone sélectionner


# ==================================================================================================================== #

# ==================================================================================================================== #


def detect_ball(output):

    blurred = cv2.GaussianBlur(output, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        set_ball_coord(x,y)

        if radius > 10:
            cv2.circle(output, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(output, center, 5, (0, 0, 255), -1)
    else:
        global x_ball, y_ball
        x_ball = -200
        y_ball = -200

    # update the points queue
    pts.appendleft(center)

def set_ball_coord(x, y):
    global x_ball, y_ball
    x_ball = x
    y_ball = y

def get_ball_coord(largeur_window_jeu, hauter_window_jeu):
    new_x = (x_ball*largeur_window_jeu)/1920
    new_y = (y_ball*hauter_window_jeu)/1080
    print('ancien  x : ',x_ball,' | ancien y : ', y_ball)
    print('new  x : ',new_x,' | new y : ', new_y)
    return(new_x,new_y)

# ==================================================================================================================== #

# ==================================================================================================================== #


def click_event(event, x, y, flags, params):    # Fonction appelé lors d'un clique souris
    if event == cv2.EVENT_LBUTTONDOWN:      # Condition ''SI'' Clique Gauche souris
        global flag                       # Variable Global permettant le décompte du nombre de points possé afin de comptabilisé les coords sélectionnés
        if flag <= 3:                   # Condigiton ''SI'' flag <= 3 alors il reste encore des points de coord à saisir, si > alors tout les points on été choisis
            coord[0][flag] = x      # Remplissage de l'array coords avec la coord 'X' de l'emplacement ou a été éffectué le clique souris
            coord[1][flag] = y      # Remplissage de l'array coords avec la coord 'Y' de l'emplacement ou a été éffectué le clique souris
            flag = flag + 1         # Incrémentation de ''flag'', signifiant qu'une coord à été enregistré


# ==================================================================================================================== #

# ==================================================================================================================== #


def retour_button_generator(window):
    fond_RETOUR = pygame.image.load(r'Play Rect.png')  # Rectangle transparent servent de fond pour le bouton ''RETOUR''
    bouton_retour = c.Button(image=pygame.transform.scale(fond_RETOUR, (300, 100)),     # Création bouton ''RETOUR''
                                  pos=((window.get_width() / 7.75), window.get_height() / 1.1),
                                  text_input='RETOUR', font=get_font(40), base_color="#d7fcd4", hovering_color="White")

    bouton_retour.changeColor(pygame.mouse.get_pos())  # SI le curseur passe du le bouton => changement couleur
    bouton_retour.update(window)  # UPDATE du bouton ''RETOUR''
    return(bouton_retour)


# ==================================================================================================================== #

# ==================================================================================================================== #


def get_font(size):  # Return la taille de police souhaité
    return pygame.font.Font(r"font.ttf", size)