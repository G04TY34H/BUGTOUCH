# SceneHistory.gd
extends Node

var scene_history = []


func go_to_scene(scene_path: String, clear_history: bool = false):
	if clear_history:
		scene_history.clear()

	var current_scene = get_tree().current_scene
	if current_scene != null:
		var path = current_scene.filename  # Assurez-vous que c'est le chemin complet
		print("Adding scene to history: ", path)
		scene_history.append(path)
	get_tree().change_scene(scene_path)

func go_back():
	if scene_history.size() > 0:
		var previous_scene_path = scene_history.pop_back()
		print("Returning to scene: ", previous_scene_path)
		get_tree().change_scene(previous_scene_path)
	else:
		print("No previous scene in history.")
		
		
