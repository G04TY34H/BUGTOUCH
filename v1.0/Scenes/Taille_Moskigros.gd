extends Label

func _process(delta):
	self.text = str("Taille : ",Autoloader.moskigros_scale_percent*100," %")

