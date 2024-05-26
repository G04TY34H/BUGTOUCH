extends Label

func _process(delta):
	self.text = str("Equipe 2 : ", Autoloader.score_2)
