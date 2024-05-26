from godot import exposed, export
from godot import *
import cv2
import numpy as np

import argparse
from collections import deque

@exposed
class Autoload_calibrage(Node2D):
	def _ready(self):
		self.circles = []  # Liste pour stocker les coordonnées des cercles rouges
		self.perspective_transformed = False  # Indicateur pour savoir si la perspective a été transformée
		self.cap = None  # Référence à l'objet de capture vidéo
		self.is_calibrating = False  # Variable pour contrôler l'exécution de la boucle de calibration

	def draw_circles(self, frame):
		for circle in self.circles:
			cv2.circle(frame, circle, 10, (0, 0, 255), -1)

	def mouse_callback(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			# Ajouter les coordonnées du clic à la liste des cercles si le nombre actuel est inférieur à 4
			if len(self.circles) < 4:
				self.circles.append((x, y))
	
	def stop_calibrage(self):
		self.is_calibrating = False
		autoload = self.get_node("/root/Autoloader")
		autoload.is_calibrated = False
	
	def start_calibrage(self):
		self.is_calibrating = True
		autoload = self.get_node("/root/Autoloader")
		
		self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Ouvrir la capture vidéo de la caméra

		# Définir la fonction mouse_callback comme gestionnaire d'événements de souris
		cv2.namedWindow('Calibrage')  # Créer une fenêtre OpenCV
		cv2.setMouseCallback('Calibrage', self.mouse_callback)

		while self.is_calibrating is True:
			_, frame = self.cap.read()  # Lire une frame de la caméra

			if not self.perspective_transformed:
				# Dessiner les cercles rouges sur la frame
				self.draw_circles(frame)

			cv2.imshow("Calibrage", frame)  # Afficher la frame dans une fenêtre OpenCV

			# Ajouter une condition pour quitter la boucle (par exemple, appuyer sur la touche 'q')
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				# Réinitialiser l'état de la calibration et continuer
				self.circles = []
				self.perspective_transformed = False
				continue
			elif key == 27:  # 27 corresponds à la touche 'Esc'
				break

			# Si 4 points ont été sélectionnés, effectuer la transformation de la perspective
			if len(self.circles) == 4 and not self.perspective_transformed:
				autoload.is_calibrated = True
				self.perspective_transformed = True
				self.change_perspective(frame)

		# Libérer la capture vidéo après avoir quitté la boucle
		self.perspective_transformed = False
		self.circles = []
		self.cap.release()
		cv2.destroyAllWindows()
	
	def convert_coordinates(self, ball_coordinates, camera_resolution, godot_resolution):
		# Convertir les coordonnées de la balle
		converted_x = ball_coordinates[0] * (1280 / 1920)
		converted_y = ball_coordinates[1] * (720 / 1080)
		return (converted_x, converted_y)

	def detect_ball(self, frame):
		# Définition de la résolution de la caméra
		camera_resolution = (1920, 1080)  # Résolution de votre caméra

		# Accéder à l'Autoloader pour obtenir la résolution de l'écran Godot
		autoload = self.get_node("/root/Autoloader")
		godot_resolution = autoload.get_screen_resolution()

		if autoload.avec_equipe:
			lower_color_1, upper_color_1 = autoload.get_color_range_1()
			lower_color_2, upper_color_2 = autoload.get_color_range_2()

			self.detect_color(frame, lower_color_1, upper_color_1, camera_resolution, godot_resolution, autoload, "Color 1")
			self.detect_color(frame, lower_color_2, upper_color_2, camera_resolution, godot_resolution, autoload, "Color 2")
		else:
			lower_color, upper_color = autoload.get_color_range()
			self.detect_color(frame, lower_color, upper_color, camera_resolution, godot_resolution, autoload, "Color")

		cv2.imshow("Balle détectée", frame)
		
	def detect_color(self, frame, lower_color, upper_color, camera_resolution, godot_resolution, autoload, color_name):
		# Convertir les valeurs de Vector3 à des tuples
		lower = (int(lower_color.x), int(lower_color.y), int(lower_color.z)) 
		upper = (int(upper_color.x), int(upper_color.y), int(upper_color.z))

		# Convertir l'image en niveaux de gris
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Appliquer un flou pour réduire le bruit et faciliter la détection des cercles
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)

		mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), lower, upper)

		# Effectuer une série de dilatations et d'érosions pour supprimer les petites taches dans le masque
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# Trouver les contours des objets dans le masque
		cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# Initialiser les coordonnées du centre de la balle
		center = None

		# Si au moins un contour est trouvé
		if len(cnts) > 0:
			# Sélectionner le plus gros contour (plus grosse balle)
			contour_select = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(contour_select)
			M = cv2.moments(contour_select)

			# Calculer les coordonnées du centre de la balle
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# Si le rayon répond à une taille minimale
			if radius > 10:
				# Dessiner le cercle autour de la balle
				cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
				# Dessiner un cercle jaune autour de la balle
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
		
		if center is not None:
			# Conversion des coordonnées de la balle
			converted_coordinates = self.convert_coordinates(center, camera_resolution, godot_resolution)
			# Appeler la méthode pour modifier la variable globale
			if color_name == "Color 1":
				autoload.set_calibration_result_1(converted_coordinates[0], converted_coordinates[1])
			elif color_name == "Color 2":
				autoload.set_calibration_result_2(converted_coordinates[0], converted_coordinates[1])
			else:
				autoload.set_calibration_result(converted_coordinates[0], converted_coordinates[1])
			print(f"{color_name} détectée")

	def change_perspective(self, frame):
		width, height = 1920, 1080
		pts1 = np.float32([list(circle) for circle in self.circles])
		pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

		matrix = cv2.getPerspectiveTransform(pts1, pts2)

		# Arrêter d'afficher les cercles rouges
		self.circles = []

		# Libérer le flux vidéo actuel
		self.cap.release()

		# Démarrer un nouveau flux vidéo basé sur la nouvelle perspective
		self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		
		while self.is_calibrating is True:
			_, new_frame = self.cap.read()
			new_output = cv2.warpPerspective(new_frame, matrix, (width, height))

			# Appeler la fonction detect_ball avec la nouvelle perspective
			self.detect_ball(new_output)

			# Ajouter une condition pour quitter la boucle (par exemple, appuyer sur la touche 'q')
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				# Réinitialiser l'état de la calibration et sortir de la boucle
				self.perspective_transformed = False
				break

		# Libérer la capture vidéo après avoir quitté la boucle
		self.perspective_transformed = False
		self.circles = []
		self.cap.release()
		cv2.destroyAllWindows()
