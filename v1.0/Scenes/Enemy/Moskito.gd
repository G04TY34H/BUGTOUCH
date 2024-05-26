extends KinematicBody2D

# Variables globales pour la taille de l'écran, la vitesse de déplacement, la direction, le sprite et le centre de l'écran
var screen_size = Vector2.ZERO
var movement_speed = 0
var direction = Vector2.ZERO
var sprite = null
var center_of_screen = Vector2.ZERO

func _ready():
	# Initialiser la taille de l'écran et le centre de l'écran
	screen_size = get_viewport_rect().size
	center_of_screen = screen_size / 2
	
	# Placer l'objet en dehors de l'écran et calculer sa direction de mouvement
	spawn_outside_of_screen()
	calculate_movement()
	
	# Récupérer le sprite de l'objet
	sprite = $Sprite

	# Changer la texture du sprite en fonction de la variable is_red de l'Autoloader
	var autoloader = get_node("/root/Autoloader")
	if autoloader.is_red:
		sprite.texture = load("res://Scenes/Enemy/Moskito_violet.png")
	else:
		sprite.texture = load("res://Scenes/Enemy/Moskito.png")

	# Récupérer la valeur d'échelle depuis Autoloader et appliquer cette échelle au sprite
	var scale_factor = get_node("/root/Autoloader").moskito_scale_percent
	sprite.scale = sprite.scale * scale_factor

	# Appliquer l'échelle à la CollisionShape2D si elle existe
	var collision_shape = $Area2D/CollisionShape2D
	if collision_shape:
		collision_shape.scale = collision_shape.scale * scale_factor

func _process(delta):
	# Mettre à jour la position de l'objet en fonction de sa direction et de sa vitesse de déplacement
	position += direction * movement_speed * delta

	# Si l'objet sort de l'écran, le supprimer
	if is_outside_of_screen():
		queue_free()

	# Ajuster l'orientation du sprite en fonction de la direction de mouvement
	if direction.x < 0:
		sprite.flip_h = true
	else:
		sprite.flip_h = false

func spawn_outside_of_screen():
	# Déterminer les côtés de l'écran où l'objet peut apparaître en fonction des paramètres dans Autoloader
	var autoloader = get_node("/root/Autoloader")
	var possible_sides = []
	
	if autoloader.haut:
		possible_sides.append(0)  # En haut
	if autoloader.droite:
		possible_sides.append(1)  # À droite
	if autoloader.bas:
		possible_sides.append(2)  # En bas
	if autoloader.gauche:
		possible_sides.append(3)  # À gauche
	
	if possible_sides.size() == 0:
		return  # Si aucune direction n'est autorisée, ne rien faire

	# Choisir aléatoirement un côté et placer l'objet en dehors de l'écran de ce côté
	var side = possible_sides[randi() % possible_sides.size()]

	match side:
		0:  # En haut
			position = Vector2(rand_range(0, screen_size.x), -20)
		1:  # À droite
			position = Vector2(screen_size.x + 20, rand_range(0, screen_size.y))
		2:  # En bas
			position = Vector2(rand_range(0, screen_size.x), screen_size.y + 20)
		3:  # À gauche
			position = Vector2(-20, rand_range(0, screen_size.y))

func calculate_movement():
	# Calculer la direction de mouvement vers le centre de l'écran avec une légère variation aléatoire
	var direction_to_center = (center_of_screen - position).normalized()
	direction = (direction_to_center + Vector2(rand_range(-0.5, 0.5), rand_range(-0.5, 0.5))).normalized()
	
	# Définir la vitesse de déplacement en fonction des paramètres de vitesse minimale et maximale dans Autoloader
	movement_speed = rand_range(Autoloader.moskito_speed_min, Autoloader.moskito_speed_max)

func is_outside_of_screen():
	# Vérifier si l'objet est en dehors des limites de l'écran avec une marge de 20 pixels
	return position.x > screen_size.x + 20 or position.x < -20 or position.y > screen_size.y + 20 or position.y < -20

func _on_Area2D_body_entered(body):
	# Détecter la collision avec un objet appartenant au groupe "ball"
	if body.is_in_group("ball"):
		# Incrémenter le score en fonction de la valeur définie dans Autoloader et supprimer l'objet
		var autoloader = get_node("/root/Autoloader")
		autoloader.update_score(autoloader.moskito_pts_value)
		queue_free()
