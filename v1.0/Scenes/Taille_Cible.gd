extends Label

func _process(delta):
	self.text = str("Taille : ",Autoloader.cible_scale_percent*100," %")

