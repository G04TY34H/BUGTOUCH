extends Control

# Variables onready pour les différents noeuds de la scène
onready var options = $Options
onready var fond = $TextureRect

func _ready():
	# Définir le titre de la fenêtre
	OS.set_window_title("Bug Touch")
	
	# Jouer la musique au démarrage
	MusicManager.play_music("res://Themes/Music/doodle.mp3")
	
	# Charger la texture de fond à partir du chemin défini dans l'Autoloader
	fond.texture = load(Autoloader.bg_path)

func _on_Jouer_pressed():
	# Changer de scène pour commencer le jeu
	get_tree().change_scene("res://Scenes/Camera_Menu.tscn")

func _on_Options_button_pressed():
	# Afficher les options au centre de l'écran
	options.popup_centered()
	
func _on_Quitter_pressed():
	# Quitter le jeu
	get_tree().quit()

func _on_Fond_pressed():
	# Changer de scène pour l'arrière-plan
	get_tree().change_scene("res://Scenes/Fond.tscn")
