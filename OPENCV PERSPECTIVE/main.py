import cv2  # Import de la bibliothèque OpenCV
import numpy as np  # Import de la bibliothèque nunPy

import Function as f    # Import du fichier ''Function'' as 'f'

''' ====================================================================== '''

cap = cv2.VideoCapture(0) # Création objet de la class ''cv2 VideoCapture'' nommé ''cap'', c'est via cette class que l'on accède à la caméra / webcam

while True:

    _, frame = cap.read() # Lecture du flux vidéo de la caméra ou webcam, return True si lu correctement, False dans le cas contraire

    f.draw_point(frame)     # Fonction qui permet de placer les points pour la calibration. Une fois les 4 points
                            # placé elle appelle la fonction ''change_perspective'' qui générera une nouvelle fenêtre avac une perspective à plat

    cv2.imshow("Frame", frame)  # Affiche la fenêtre de capture de la webcam

    cv2.setMouseCallback('Frame', f.click_event)  # Event Click souris sur le fenêtre de vidéo principal

    key = cv2.waitKey(1)        # Si Touche ECHAP alors Fermeture des fenêtres ouvertes
    if key == 27:
        break
