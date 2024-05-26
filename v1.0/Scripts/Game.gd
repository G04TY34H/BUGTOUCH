extends Node2D
onready var pause_menu = $CanvasLayer/MenuPause


func _ready():
	$AnimationPlayer.play("test animation")
	show_pause_menu_if_paused()
	

func show_pause_menu_if_paused():
	if get_tree().paused:
		pause_menu.visible = true
