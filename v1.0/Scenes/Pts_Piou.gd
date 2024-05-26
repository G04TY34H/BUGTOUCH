extends Label

func _process(delta):
	self.text = str("Points : ", Autoloader.piou_pts_value)
