extends Node

# Référence à l'AudioStreamPlayer courant
var current_music_player: AudioStreamPlayer = null

# Fonction pour jouer la musique
func play_music(music_path: String):
	# Arrêter la musique courante si elle joue
	if current_music_player != null and current_music_player.playing:
		current_music_player.stop()
		current_music_player.queue_free()

	# Charger et jouer la nouvelle musique
	var new_music = load(music_path)
	current_music_player = AudioStreamPlayer.new()
	current_music_player.stream = new_music
	add_child(current_music_player)
	current_music_player.play()
