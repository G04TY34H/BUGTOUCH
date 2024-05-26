extends Label

func _process(delta):
	self.text = str("Apparition : ",Autoloader.freq_apparition,"\ntoute les Secs")

