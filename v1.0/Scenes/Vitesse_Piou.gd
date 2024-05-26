extends Label

func _process(delta):
	self.text = str("Vitesse Min : ", Autoloader.piou_speed_min, "\nVitesse Max : ", Autoloader.piou_speed_max)
