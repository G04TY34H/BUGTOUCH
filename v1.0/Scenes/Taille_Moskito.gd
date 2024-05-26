extends Label

func _process(delta):
	self.text = str("Taille : ",Autoloader.moskito_scale_percent*100," %")

