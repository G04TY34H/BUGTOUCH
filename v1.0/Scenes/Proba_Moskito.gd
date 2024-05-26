extends Label

func _process(delta):
	self.text = str("Chance : ", Autoloader.moskito_proba, " %\nD'apparition")
