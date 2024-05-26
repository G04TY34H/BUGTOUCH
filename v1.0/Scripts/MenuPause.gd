extends Control

# Variable pour gérer l'état de pause, avec un setter personnalisé
var is_paused = false setget set_is_paused

# Variable onready pour le noeud des options
onready var options = $Options

func _ready():
	# Permettre le traitement des entrées non gérées
	set_process_unhandled_input(true)

func _unhandled_input(event):
	# Vérifier si l'action pause est pressée
	if event.is_action_pressed("pause"):
		print("test")
		# Afficher ou cacher les options en fonction de leur état actuel
		if options.visible:
			options.hide()
		else:
			# Inverser l'état de pause
			self.is_paused = !is_paused

func set_is_paused(value):
	# Définir l'état de pause et mettre à jour la visibilité
	is_paused = value
	get_tree().paused = is_paused
	visible = is_paused

func _on_Reprendre_pressed():
	# Reprendre le jeu en désactivant la pause
	self.is_paused = false

func _on_Options_button_pause_pressed():
	# Afficher les options au centre de l'écran
	options.popup_centered()
	
func _on_QuitterPartie_pressed():
	# Quitter la partie, réinitialiser le score et arrêter la calibration
	self.is_paused = false
	Autoloader.reset_score()
	Autoloader.stop_calibration()
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")
