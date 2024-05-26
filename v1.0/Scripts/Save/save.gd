extends Node

const SAVEFILE = "user://SAVEFILE.save"

var game_data = {
	"master_vol": -10,  # Niveau de volume principal initial
	"music_vol": -10,   # Niveau de volume de la musique initial
	"input_mappings": {}  # Mappages des entrées utilisateur
}

func _ready():
	# Appeler les fonctions de chargement des données et d'application des paramètres lors de l'initialisation du noeud
	load_data()
	apply_settings()

func load_data():
	var file = File.new()
	if file.file_exists(SAVEFILE):
		# Si le fichier de sauvegarde existe, l'ouvrir en lecture et charger les données
		file.open(SAVEFILE, File.READ)
		game_data = file.get_var()
		file.close()
		
		# Vérifier et initialiser input_mappings si nécessaire
		if not game_data.has("input_mappings"):
			game_data["input_mappings"] = {}
			
		# Appliquer les mappages d'input
		apply_input_mappings()
		print("Données chargées : ", game_data)  # Message de débogage pour confirmer le chargement des données
	else:
		# Si le fichier n'existe pas, sauvegarder les données par défaut
		save_data()

func save_data():
	var file = File.new()
	# Ouvrir le fichier de sauvegarde en écriture et stocker les données de jeu
	file.open(SAVEFILE, File.WRITE)
	file.store_var(game_data)
	file.close()
	print("Données enregistrées : ", game_data)  # Message de débogage pour confirmer l'enregistrement des données

func apply_settings():
	# Appliquer les volumes audio configurés dans les données de jeu
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), game_data["master_vol"])
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), game_data["music_vol"])
	print("Paramètres appliqués : Master Volume =", game_data["master_vol"], ", Music Volume =", game_data["music_vol"])  # Message de débogage pour confirmer l'application des paramètres

func apply_input_mappings():
	# Appliquer les mappages d'input définis dans les données de jeu
	for action_name in game_data["input_mappings"].keys():
		InputMap.action_erase_events(action_name)
		for event in game_data["input_mappings"][action_name]:
			var input_event = InputEventKey.new()
			input_event.scancode = event
			InputMap.action_add_event(action_name, input_event)
	print("Mappages d'input appliqués :", game_data["input_mappings"])  # Message de débogage pour confirmer l'application des mappages d'input

func update_master_vol(vol):
	# Mettre à jour le volume principal et enregistrer les données
	game_data["master_vol"] = vol
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), vol)
	save_data()

func update_music_vol(vol):
	# Mettre à jour le volume de la musique et enregistrer les données
	game_data["music_vol"] = vol
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), vol)
	save_data()

func update_input_mapping(action_name, scancode):
	# Mettre à jour les mappages d'input pour une action spécifique
	if not game_data.has("input_mappings"):
		game_data["input_mappings"] = {}

	# Réinitialiser les événements pour cette action et ajouter le nouveau mappage
	game_data["input_mappings"][action_name] = [scancode]
	save_data()
	print("Mappage d'input mis à jour : ", game_data["input_mappings"])  # Message de débogage pour confirmer la mise à jour des mappages d'input
