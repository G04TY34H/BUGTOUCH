extends Label

func _process(delta):
	self.text = str("Equipe 1 : ", Autoloader.score_1)
