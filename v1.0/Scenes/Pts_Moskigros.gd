extends Label

func _process(delta):
	self.text = str("Points : ", Autoloader.moskigros_pts_value)
