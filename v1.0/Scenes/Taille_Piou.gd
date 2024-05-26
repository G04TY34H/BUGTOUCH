extends Label

func _process(delta):
	self.text = str("Taille : ",Autoloader.piou_scale_percent*100," %")

