extends Label

func _process(delta):
	if !Autoloader.avec_temps:
		self.text = str("Sans Temps")
	else:
		self.text = str("Temps : %02d : %02d" % time_left_to_live())

func time_left_to_live():
	var time_left = Autoloader.temps
	var minute = floor(time_left / 60)
	var second = int(time_left) % 60
	return [minute, second]
