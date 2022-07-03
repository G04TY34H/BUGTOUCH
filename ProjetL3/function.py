import cv2  # Import de la bibliothèque OpenCV
import numpy as np  # Import de la bibliothèque nunPy


coord = [[-10,-10,-10,-10],[-10,-10,-10,-10]]   # Array des coordonées des points de la surface de Jeux
flag = 0        # Variable servant de compteur pour le nombre de coordonées sélectionné (4 max pour les 4 points formant la zone sur laquelle la perspective sera modifié)



# ==================================================================================================================== #

def reset_coord():
    global flag
    flag = 0
    for i in range (0,4):
        coord[0][i] = -10
        coord[1][i] = -10

# ==================================================================================================================== #


def draw_point(frame):  # Fonction permettant le dessin des points pour la calibration avec la fenêtre ''frame'' en paramètre

    for i in range (0,4):   # Boucle allant de 0 jusqu'à 3 pour les 4 points
        cv2.circle(frame, ((coord[0][i], coord[1][i])), 5, (0, 0, 255), cv2.FILLED)      # Fonction pour le dessin des points avec en arguments :
    if coord[0][3] != -10:       # Si coord du 4ème points différent de celle de basse               # NomDeLaFenêtre | coordonnée X,Y | RadiusCercle | CouleurRGB | RemplissageDuCercle
        change_perspective(frame)   # Alors tout les points sont placé => appelle fonction ''change_perspective''


# ==================================================================================================================== #


def change_perspective(frame):  # Fonction permettant le changement de perspective + l'affichage de celle-ci avec la fenêtre ''frame'' en paramètre

    width, height = 800, 450    # Largeur et Hauteur de la fenêtre affichant la perspective tranformé
    pts1 = np.float32([[coord[0][0],coord[1][0]],[coord[0][1],coord[1][1]],[coord[0][2],coord[1][2]],[coord[0][3],coord[1][3]]])    # pts1 contient les coord des points sélectionné dans ''draw_point''
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])      # pts2 contient les caractéristique de la fenêtre d'affichage de la nouvelle perspective

    matrix = cv2.getPerspectiveTransform(pts1,pts2)     # Fonction permetant le changement de perspective prenant en argunment "pts1" et "pts2"
    output = cv2.warpPerspective(frame, matrix, (width, height))    # Fonction appliquant la transformation de la perspective en image

    cv2.imshow("output image", output)  # affiche la fenêtre avec la perspective à plat de la zone sélectionner


# ==================================================================================================================== #


def click_event(event, x, y, flags, params):    # Fonction appelé lors d'un clique souris
    if event == cv2.EVENT_LBUTTONDOWN:      # Condition ''SI'' Clique Gauche souris
        global flag                       # Variable Global permettant le décompte du nombre de points possé afin de comptabilisé les coords sélectionnés
        if flag <= 3:                   # Condigiton ''SI'' flag <= 3 alors il reste encore des points de coord à saisir, si > alors tout les points on été choisis
            coord[0][flag] = x      # Remplissage de l'array coords avec la coord 'X' de l'emplacement ou a été éffectué le clique souris
            coord[1][flag] = y      # Remplissage de l'array coords avec la coord 'Y' de l'emplacement ou a été éffectué le clique souris
            flag = flag + 1         # Incrémentation de ''flag'', signifiant qu'une coord à été enregistré

