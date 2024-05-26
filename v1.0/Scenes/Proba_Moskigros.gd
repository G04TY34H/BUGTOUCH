extends Label

func _process(delta):
	self.text = str("Chance : ", Autoloader.moskigros_proba, " %\nD'apparition")
