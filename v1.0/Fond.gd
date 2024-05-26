extends Control

onready var fond = $Fond

func _process(delta):
	fond.texture = load(Autoloader.bg_path)
	
func _on_Automne_pressed():
	Autoloader.bg_path = "res://Themes/Style/automne.png"

func _on_Desert_pressed():
	Autoloader.bg_path = "res://Themes/Style/desert.png"

func _on_Hiver_pressed():
	Autoloader.bg_path = "res://Themes/Style/fantasy_forest_hiver.png"

func _on_Pyramide_pressed():
	Autoloader.bg_path = "res://Themes/Style/pyramide.png"

func _on_Plage_pressed():
	Autoloader.bg_path = "res://Themes/Style/plage.png"

func _on_Plaine_pressed():
	Autoloader.bg_path = "res://Themes/Style/plaine.png"

func _on_Foret_pressed():
	Autoloader.bg_path = "res://Themes/Style/fantasy_forest_printemps.png"

func _on_Lave_pressed():
	Autoloader.bg_path = "res://Themes/Style/lave.png"

func _on_Button_Retour_pressed():
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")
