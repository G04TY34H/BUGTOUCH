extends Label

func _process(delta):
	self.text = str("Chance : ", Autoloader.piou_proba, " %\nD'apparition")
