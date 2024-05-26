extends Label

func _process(delta):
	self.text = str("Vitesse Min : ", Autoloader.moskigros_speed_min, "\nVitesse Max : ", Autoloader.moskigros_speed_max)
