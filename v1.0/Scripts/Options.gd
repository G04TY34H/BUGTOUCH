extends Popup

# Précharger la scène du bouton d'entrée et initialiser les variables onready pour les noeuds de la scène
onready var input_button_scene = preload("res://Scenes/InputButton.tscn")
onready var action_list = $PanelContainer/MarginContainer/VBoxContainer/ScrollContainer/ActionsList
onready var master_slider = $OptionsContainer/Audio/Master
onready var music_slider = $OptionsContainer/Audio/Music
onready var fond = $TextureRect

# Exporter les chemins des boutons pour le mode fenêtré et la musique
export (NodePath) var window_mode_button_path: NodePath
export (NodePath) var music_button_path: NodePath

# Initialiser les variables pour les boutons d'option et d'autres paramètres
var window_mode_button: OptionButton = null
var music_button: OptionButton = null
var mainmenu_scene_instance = null
var is_remapping = false
var action_to_remap = null
var remapping_button = null

func _ready():
	# Créer la liste des actions à afficher
	_create_action_list()
	
	# Charger la texture de fond à partir du chemin défini dans l'Autoloader
	fond.texture = load(Autoloader.bg_path)
	
	# Initialiser les sliders de volume avec les valeurs sauvegardées
	master_slider.value = Save.game_data["master_vol"]
	music_slider.value = Save.game_data["music_vol"]

	# Obtenir les noeuds des boutons d'option
	window_mode_button = get_node(window_mode_button_path)
	music_button = get_node(music_button_path)

	# Connecter les signaux des boutons d'option à leurs fonctions respectives
	window_mode_button.connect("item_selected", self, "_on_window_mode_selected")
	music_button.connect("item_selected", self, "_on_music_selected")

	# Sélectionner les options par défaut pour le mode fenêtré et la musique
	window_mode_button.select(0)  # Fenêtré par défaut
	music_button.select(0)  # Musique 1 par défaut

func _create_action_list():
	# Liste des actions à afficher
	var actions_to_display = ["Fullscreen", "Windowed", "Back", "pause"]
	for action_name in actions_to_display:
		# Récupérer la liste des événements pour chaque action
		var action_events = InputMap.get_action_list(action_name)
		if action_events.size() > 0:
			var input_event = action_events[0]
			if input_event is InputEventKey or input_event is InputEventJoypadButton:
				# Ajouter l'action à l'interface utilisateur avec la touche assignée
				_add_action_to_ui(action_name, input_event.as_text())
			else:
				# Ajouter l'action à l'interface utilisateur sans touche assignée
				_add_action_to_ui(action_name, "Assigner")
		else:
			# Ajouter l'action à l'interface utilisateur sans touche assignée
			_add_action_to_ui(action_name, "Assigner")

func _add_action_to_ui(action_name, input_text):
	# Instancier le bouton d'entrée et l'ajouter à la liste des actions
	var input_button_instance = input_button_scene.instance()
	action_list.add_child(input_button_instance)

	# Mettre à jour le texte des labels d'action et de saisie
	var action_label = input_button_instance.get_node("MarginContainer/HBoxContainer/ActionLabel")
	action_label.text = action_name

	var input_label = input_button_instance.get_node("MarginContainer/HBoxContainer/InputLabel")
	input_label.text = input_text

	# Connecter le signal de pression du bouton d'entrée à la fonction de remapping
	input_button_instance.connect("pressed", self, "_on_input_button_pressed", [action_name, input_button_instance])

func _on_input_button_pressed(action_name, button_instance):
	if is_remapping:
		return  # Empêche le remapping si une opération est déjà en cours

	# Initialiser le processus de remapping
	is_remapping = true
	action_to_remap = action_name
	remapping_button = button_instance
	remapping_button.get_node("MarginContainer/HBoxContainer/InputLabel").text = "Appuyez sur une touche..."

func _input(event):
	if not is_remapping:
		return

	if event is InputEventKey and event.pressed and not event.echo:
		# Ajouter ou mettre à jour le mappage d'entrée
		InputMap.action_erase_events(action_to_remap)
		var new_event = InputEventKey.new()
		new_event.scancode = event.scancode
		InputMap.action_add_event(action_to_remap, new_event)

		# Mettre à jour l'affichage de l'action dans la liste des actions
		_update_action_list(remapping_button, new_event)
		
		# Sauvegarder le nouveau mappage d'entrée
		Save.update_input_mapping(action_to_remap, event.scancode)

		# Réinitialiser le statut de remappage
		is_remapping = false
		action_to_remap = null
		remapping_button = null

func _update_action_list(button, event):
	# Mettre à jour le texte du label d'entrée avec la nouvelle touche assignée
	var input_label = button.get_node("MarginContainer/HBoxContainer/InputLabel")
	input_label.text = OS.get_scancode_string(event.scancode)

func _on_RetourFromOptions_pressed():
	# Cacher le popup des options
	hide()

func _on_Master_value_changed(value):
	# Afficher le nouveau volume master pour le débogage et mettre à jour le volume global
	print("Nouveau volume master : ", value)
	Global.update_master_vol(value)

func _on_Music_value_changed(value):
	# Afficher le nouveau volume de la musique pour le débogage et mettre à jour le volume global
	print("Nouveau volume music : ", value)
	Global.update_music_vol(value)

func _on_OptionButton_item_selected(index):
	# Basculer entre le mode fenêtré et le plein écran en fonction de la sélection
	if index == 0:
		Global._toggle_windowed()
	elif index == 1:
		Global._toggle_fullscreen()

func _on_OptionButton2_item_selected(index):
	# Changer la musique en fonction de la sélection
	var music_path = ""
	if index == 0:
		music_path = "res://Themes/Music/doodle.mp3"
	elif index == 1:
		music_path = "res://Themes/Music/BrandonMorris-LoadingScreenLoop-cc0-qmix.mp3"

	# Jouer la musique sélectionnée
	MusicManager.play_music(music_path)
