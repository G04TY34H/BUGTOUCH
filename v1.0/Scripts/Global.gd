extends Node

# Variables pour gérer les options et le menu pause
var options_scene_instance = null  # Garder une référence à l'instance des options
var pause_menu_instance: Control = null

func _ready():
	# Permettre le traitement des entrées non gérées
	set_process_unhandled_input(true)

func _unhandled_input(event):
	# Vérifier les entrées du clavier pour les actions spécifiques
	if event is InputEventKey:
		if event.pressed and not event.echo:
			if Input.is_action_just_pressed("Fullscreen"):
				_toggle_fullscreen()
			elif Input.is_action_just_pressed("Windowed"):
				_toggle_windowed()
			elif Input.is_action_just_pressed("Back"):
				SceneHistory.go_back()

func _toggle_fullscreen():
	# Basculer entre le mode plein écran et le mode fenêtré
	OS.window_fullscreen = !OS.window_fullscreen

func _toggle_windowed():
	# Passer en mode fenêtré
	OS.window_fullscreen = false
	
func update_master_vol(vol):
	# Mettre à jour le volume principal et sauvegarder les données
	AudioServer.set_bus_volume_db(0, vol)
	Save.game_data.master_vol = vol
	Save.save_data()
	
func update_music_vol(vol):
	# Mettre à jour le volume de la musique et sauvegarder les données
	AudioServer.set_bus_volume_db(1, vol)
	Save.game_data.music_vol = vol
	Save.save_data()
