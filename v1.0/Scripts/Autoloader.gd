extends Node2D

var calibration_thread : Thread

var coord_ball = Vector2.ZERO

var lowerColor = Color(0, 0, 0)  
var upperColor = Color(0, 0, 0) 

var lowerColor_1 = Color(0, 0, 0) 
var upperColor_1 = Color(0, 0, 0) 

var lowerColor_2 = Color(0, 0, 0) 
var upperColor_2 = Color(0, 0, 0) 

var score = 0

var is_calibrated = false

var avec_temps = false
var temps = 0

var gauche = true
var droite = true
var bas = true
var haut = true
var cam = true

var is_red = true

var bg_path = "res://Themes/Style/fantasy_forest_printemps.png"

var couleur_selected = "Rouge"

#=== EQUIPE ===#

var avec_equipe = false

var couleur_selected_1 = "Rouge"
var couleur_selected_2 = "Bleu"

var score_1 = 0
var score_2 = 0

#=== STATS ====#

var freq_apparition_sauvkipiou = 1

#=== Cible ===#

var cible_scale_percent = 1

var max_target = 5

var freq_apparition = 1

#=== Moskito ===#
var moskito_speed_min = 50
var moskito_speed_max = 300

var moskito_scale_percent = 1
var moskito_pts_value = 2

var moskito_proba = 40

#=== Moskigros ===#
var moskigros_speed_min = 20
var moskigros_speed_max = 150

var moskigros_scale_percent = 1
var moskigros_pts_value = 1

var moskigros_proba = 40

#=== Piou ===#
var piou_speed_min = 40
var piou_speed_max = 250

var piou_scale_percent = 1
var piou_pts_value = -1

var piou_proba = 20

func _ready():
	print("Version Bug Touch 0.01a")
	pass

func _process(delta):
	pass
		
func update_score(points):
	score += points

func reset_score():
	score_1=0
	score_2=0
	score = 0

func set_color_range(lower, upper):
	lowerColor = lower
	upperColor = upper
	print("Color range updated to lower:", lowerColor, " upper:", upperColor)

func get_color_range():
	return [lowerColor, upperColor]

func get_screen_resolution():
	return get_viewport().size

func start_calibration():
	calibration_thread = Thread.new()
	calibration_thread.start(self, "_calibration_thread_function")

func stop_calibration():
	if calibration_thread:
		if calibration_thread.is_active():
			AutoloadCalibrage.stop_calibrage()
			calibration_thread.wait_to_finish()

func _calibration_thread_function():
	# Fonction de calibration à exécuter dans le thread
	AutoloadCalibrage.start_calibrage()
	print("Calibration thread finished.")

func set_calibration_result(x, y):
	# Mettre à jour calibration_result avec les nouvelles valeurs x et y
	coord_ball = Vector2(x, y)

func show_final_score():
	var screen_size = get_viewport().size

	# Création du Label pour afficher le score
	var score_label = Label.new()
	score_label.text = "Fin de partie. Votre score : " + str(score)
	score_label.rect_min_size = Vector2(300, 50)
	score_label.rect_position = Vector2((screen_size.x - 300) / 2, (screen_size.y - 50) / 2)
	score_label.add_color_override("font_color", Color(1, 1, 1))  # Blanc
	add_child(score_label)

	# Création du bouton pour retourner au menu principal
	var return_button = Button.new()
	return_button.text = "Retour au menu principal"
	return_button.rect_min_size = Vector2(300, 50)
	return_button.rect_position = Vector2((screen_size.x - 300) / 2, (screen_size.y - 50) / 2 + 60)
	return_button.connect("pressed", self, "_on_return_button_pressed")
	add_child(return_button)

func _on_return_button_pressed():
	stop_calibration()
	reset_score()  # Réinitialisez le score
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")
