extends Label

func _process(delta):
	self.text = str("Vitesse Min : ", Autoloader.moskito_speed_min, "\nVitesse Max : ", Autoloader.moskito_speed_max)
	
