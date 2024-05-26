extends Label

func _process(delta):
	self.text = str("Points : ", Autoloader.moskito_pts_value)
