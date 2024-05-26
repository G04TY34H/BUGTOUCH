extends KinematicBody2D

var autoloader

func _ready():
	autoloader = get_node("/root/Autoloader")
	add_to_group("ball")
	
func _process(delta):
	var ball_coordinates = autoloader.coord_ball
	position = Vector2(ball_coordinates.x, ball_coordinates.y)
	

