extends Label

func _process(delta):
	self.text = str("Nombre : ",Autoloader.max_target,"\nde cibles\nimultané MAX")
