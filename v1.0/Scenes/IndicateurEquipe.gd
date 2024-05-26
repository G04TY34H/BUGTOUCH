extends Label

func _process(delta):
	if !Autoloader.avec_equipe:
		self.text = str("Sans Equipe")
	else:
		self.text = str("Avec Equipe")
