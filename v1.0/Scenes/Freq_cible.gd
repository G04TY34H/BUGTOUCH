extends Label

func _process(delta):
	self.text = str("Frequence : ",Autoloader.freq_apparition," Sec\nd'apparition")
