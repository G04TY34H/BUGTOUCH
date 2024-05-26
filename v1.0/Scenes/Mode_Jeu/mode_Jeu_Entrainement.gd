extends Node2D

# Précharger les scènes pour les cibles et les balles
var target_scene = preload("res://Scenes/Enemy/Target.tscn")
var ball_scene = preload("res://Scenes/balle.tscn")

# Variables pour gérer les cibles
var max_targets = Autoloader.max_target
var current_target_count = 0
var target_positions = []

# Variables onready pour les différents noeuds de la scène
onready var labelTemps = $TextureRect/LabelTemps
onready var current_score_label = $TextureRect/Score
onready var timer = $Countdown
onready var timer_spawn = $TimerSpawn
onready var end_screen = $EndScreen
onready var score_label = $EndScreen/ScoreLabel
onready var return_button = $EndScreen/ReturnButton
onready var rejouer = $EndScreen/Rejouer
onready var pause_menu = $CanvasLayer/MenuPause
onready var fond = $TextureRect

func _ready():
	# Charger la texture de fond à partir du chemin défini dans l'Autoloader
	fond.texture = load(Autoloader.bg_path)
	
	# Afficher le menu pause si le jeu est en pause
	show_pause_menu_if_paused()
	
	# Instancier une balle et l'ajouter à la scène
	var ball_instance = ball_scene.instance()
	add_child(ball_instance)
	
	# Définir le temps d'attente du timer_spawn à partir de la fréquence définie dans l'Autoloader
	timer_spawn.wait_time = Autoloader.freq_apparition
	end_screen.visible = false
	
	# Récupérer la variable 'avec_temps' de l'Autoloader et ajuster le timer et l'affichage en conséquence
	var autoloader = get_node("/root/Autoloader")
	if !autoloader.avec_temps:
		timer.stop()
		labelTemps.visible = false

func _process(delta):
	# Mettre à jour l'affichage du temps restant
	labelTemps.text = "%02d : %02d" % time_left_to_live()
	
	# Mettre à jour l'affichage du score actuel
	current_score_label.text = "Score : " + str(get_node("/root/Autoloader").score)

func show_pause_menu_if_paused():
	# Afficher le menu pause si le jeu est en pause
	if get_tree().paused:
		pause_menu.visible = true

func _on_Button_Retour_pressed():
	# Réinitialiser le score, arrêter la calibration et retourner au menu principal
	var autoloader = get_node("/root/Autoloader")
	autoloader.reset_score()
	autoloader.stop_calibration()
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")

func _on_TimerSpawn_timeout():
	# Générer une nouvelle cible si le nombre de cibles actuel est inférieur au maximum autorisé
	if current_target_count < max_targets:
		var target_instance = target_scene.instance()
		
		# Trouver une position valide pour la nouvelle cible
		var valid_position = get_valid_position(target_instance)
		if valid_position != null:
			target_instance.position = valid_position
			add_child(target_instance)
			target_positions.append(valid_position)
			current_target_count += 1
			# Connecter le signal tree_exiting de la cible pour gérer sa suppression
			target_instance.connect("tree_exiting", self, "_on_target_exited", [valid_position])
	else:
		pass

func _on_target_exited(position):
	# Décrémenter le nombre de cibles actuel et supprimer la position de la cible de la liste des positions
	current_target_count -= 1
	for target_pos in target_positions:
		if target_pos == position:
			target_positions.erase(target_pos)
			break

func get_valid_position(target_instance):
	# Obtenir la taille de l'écran et définir les marges et distances minimales
	var screen_size = get_viewport_rect().size
	var margin = 50 
	var min_distance = 50 * Autoloader.cible_scale_percent
	var max_attempts = 50

	# Essayer de trouver une position valide pour la nouvelle cible
	for i in range(max_attempts):
		var x_position = rand_range(margin, screen_size.x - margin)
		var y_position = rand_range(margin, screen_size.y - margin)
		var position = Vector2(x_position, y_position)

		var valid = true
		for target_pos in target_positions:
			if position.distance_to(target_pos) < min_distance:
				valid = false
				break

		if valid:
			return position
	return null

func time_left_to_live():
	# Calculer le temps restant au format minutes et secondes
	var time_left = timer.time_left
	var minute = floor(time_left / 60)
	var second = int(time_left) % 60
	return [minute, second]

func _on_Countdown_timeout():
	# Afficher l'écran de fin de partie lorsque le compte à rebours est terminé
	show_end_screen()

func show_end_screen():
	# Afficher l'écran de fin de partie et les scores
	var autoloader = get_node("/root/Autoloader")
	end_screen.visible = true
	score_label.text = "Fin de partie\nVotre score : " + str(autoloader.score)
	
	# Supprimer toutes les cibles et arrêter le timer_spawn
	remove_all_targets()
	timer_spawn.stop()
	
	# Cacher l'affichage du temps et du score actuel
	labelTemps.visible = false
	current_score_label.visible = false

func _on_ReturnButton_pressed():
	# Réinitialiser le score, arrêter la calibration et retourner au menu principal
	var autoloader = get_node("/root/Autoloader")
	autoloader.reset_score()
	autoloader.stop_calibration()
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")

func remove_all_targets():
	# Supprimer toutes les cibles de la scène et réinitialiser le compteur de cibles
	for child in get_children():
		if child is StaticBody2D and child.has_method("queue_free"):
			child.queue_free()
	current_target_count = 0
	target_positions.clear()

func _on_Rejouer_pressed():
	# Réinitialiser le score et recharger la scène actuelle pour rejouer
	var autoloader = get_node("/root/Autoloader")
	autoloader.reset_score()
	get_tree().reload_current_scene()
