extends Node2D

# Précharger les scènes pour les différents types d'ennemis et d'objets amicaux
var moskigro_scene = preload("res://Scenes/Enemy/Moskigros.tscn")
var moskito_scene = preload("res://Scenes/Enemy/Moskito.tscn")
var piou_scene = preload("res://Scenes/Friend/Piou.tscn")
var ball_scene = preload("res://Scenes/balle.tscn")

var screen_size = Vector2.ZERO  # Taille de l'écran

# Variables onready pour les différents noeuds de la scène
onready var labelTemps = $TextureRect/LabelTemps
onready var current_score_label = $TextureRect/Score
onready var ScoreLabel_1 = $EndScreen/ScoreLabel_1
onready var ScoreLabel_2 = $EndScreen/ScoreLabel_2
onready var timer = $Countdown
onready var timer_spawn = $TimerSpawn
onready var end_screen = $EndScreen
onready var score_label = $EndScreen/ScoreLabel
onready var control_equipe = $Control_Equipe
onready var return_button = $EndScreen/ReturnButton
onready var rejouer = $EndScreen/Rejouer
onready var pause_menu = $CanvasLayer/MenuPause
onready var fond = $TextureRect

func _ready():
	# Si l'option avec_equipe est activée, cacher l'affichage du score individuel et montrer le contrôle d'équipe
	if Autoloader.avec_equipe:
		current_score_label.visible = false
		control_equipe.visible = true
	
	# Charger la texture de fond à partir du chemin défini dans l'Autoloader
	fond.texture = load(Autoloader.bg_path)
	
	# Afficher le menu pause si le jeu est en pause
	show_pause_menu_if_paused()
	
	# Définir le temps d'attente du timer_spawn à partir de la fréquence définie dans l'Autoloader
	timer_spawn.wait_time = Autoloader.freq_apparition_sauvkipiou
	
	# Obtenir la taille de l'écran
	screen_size = get_viewport_rect().size
	
	# Instancier la balle et l'ajouter à la scène
	var ball_instance = ball_scene.instance()
	add_child(ball_instance)
	
	# Cacher l'écran de fin de partie
	end_screen.visible = false

	# Récupérer la variable 'avec_temps' de l'Autoloader et ajuster le timer et l'affichage en conséquence
	var autoloader = get_node("/root/Autoloader")
	if !autoloader.avec_temps:
		timer.stop()
		labelTemps.visible = false
		
func _process(delta):
	# Mettre à jour l'affichage du temps restant si l'option avec_temps est activée
	if get_node("/root/Autoloader").avec_temps:
		labelTemps.text = "%02d : %02d" % time_left_to_live()
	
	# Mettre à jour l'affichage du score actuel
	current_score_label.text = "Score : " + str(get_node("/root/Autoloader").score)

func show_pause_menu_if_paused():
	# Afficher le menu pause si le jeu est en pause
	if get_tree().paused:
		pause_menu.visible = true

func _on_TimerSpawn_timeout():
	# Générer des ennemis uniquement si le timer de compte à rebours est actif ou si l'option avec_temps est désactivée
	var autoloader = get_node("/root/Autoloader")
	if autoloader.avec_temps and timer.time_left > 0 or not autoloader.avec_temps:
		var random_value = randi() % 101  # Utiliser randi() % 101 pour obtenir une valeur aléatoire entre 0 et 100
		
		# Générer un type d'ennemi en fonction de la probabilité définie dans l'Autoloader
		if random_value < autoloader.moskigros_proba:
			var moskigro = moskigro_scene.instance()
			add_child(moskigro)
		elif random_value < autoloader.moskigros_proba + autoloader.moskito_proba:
			var moskito = moskito_scene.instance()
			add_child(moskito)
		elif random_value < autoloader.moskigros_proba + autoloader.moskito_proba + autoloader.piou_proba:
			var piou = piou_scene.instance()
			add_child(piou)

func _on_Countdown_timeout():
	# Afficher l'écran de fin de partie et arrêter la génération d'ennemis lorsque le compte à rebours est terminé
	show_end_screen()
	timer_spawn.stop()

func show_end_screen():
	# Afficher l'écran de fin de partie et les scores
	var autoloader = get_node("/root/Autoloader")
	end_screen.visible = true
	
	# Afficher les scores individuels ou d'équipe en fonction des paramètres de jeu
	if !Autoloader.avec_equipe:
		score_label.visible = true
		score_label.text = "Fin de partie\nVotre score : " + str(autoloader.score)
	else:
		ScoreLabel_1.visible = true
		ScoreLabel_1.text = "Equipe 1 : " + str(autoloader.score_1)
		ScoreLabel_2.visible = true
		ScoreLabel_2.text = "Equipe 2 : "  + str(autoloader.score_2)

	# Supprimer tous les ennemis et objets de la scène
	remove_all_targets()
	
	# Cacher l'affichage du temps et du score actuel
	labelTemps.visible = false
	current_score_label.visible = false

func _on_ReturnButton_pressed():
	# Réinitialiser le score et arrêter la calibration avant de retourner au menu principal
	var autoloader = get_node("/root/Autoloader")
	autoloader.reset_score()
	autoloader.stop_calibration()
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")

func _on_Rejouer_pressed():
	# Réinitialiser le score et recharger la scène actuelle pour rejouer
	var autoloader = get_node("/root/Autoloader")
	autoloader.reset_score()
	get_tree().reload_current_scene()

func remove_all_targets():
	# Supprimer tous les objets de type KinematicBody2D de la scène
	for obj in get_children():
		if obj is KinematicBody2D:
			remove_child(obj)
			obj.queue_free()

func time_left_to_live():
	# Calculer le temps restant au format minutes et secondes
	var time_left = timer.time_left
	var minute = floor(time_left / 60)
	var second = int(time_left) % 60
	return [minute, second]
