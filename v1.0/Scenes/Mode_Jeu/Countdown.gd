extends Timer

func _ready():
	var autoloader = get_node("/root/Autoloader")
	wait_time = autoloader.temps
	start()
