extends Label

func _process(delta):
	self.text = str("Couleur : ",Autoloader.couleur_selected)
