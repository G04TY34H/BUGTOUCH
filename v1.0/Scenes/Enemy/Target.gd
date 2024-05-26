extends StaticBody2D

var margin = 35  # Marge de sécurité par rapport aux bords

func _ready():
	# Obtenir le sprite enfant de ce nœud
	var sprite = $Sprite
	
	# Obtenir une référence au nœud Autoloader
	var autoloader = get_node("/root/Autoloader")
	
	# Changer la texture du sprite en fonction de la variable is_red dans Autoloader
	if autoloader.is_red:
		sprite.texture = load("res://Scenes/Enemy/purple_target.png")
	else:
		sprite.texture = load("res://Scenes/Enemy/target-logo-contest-.png")
	
	# Récupérer la valeur d'échelle depuis Autoloader
	var scale_factor = autoloader.cible_scale_percent
	
	# Appliquer l'échelle au Sprite
	sprite.scale = sprite.scale * scale_factor

	# Appliquer l'échelle à la CollisionShape2D
	var collision_shape = $Area2D/CollisionShape2D
	if collision_shape:
		collision_shape.scale = collision_shape.scale * scale_factor
		
	# S'assurer que la position aléatoire est différente à chaque lancement
	randomize()
	# La position est désormais définie par le script principal

# Fonction appelée lorsqu'un corps entre dans la zone de collision
func _on_Area2D_body_entered(body):
	# Vérifier si le corps appartient au groupe "ball"
	if body.is_in_group("ball"):
		# Obtenir une référence au nœud Autoloader
		var autoloader = get_node("/root/Autoloader")
		
		# Incrémenter le score de 1
		autoloader.update_score(1)
		
		# Supprimer ce nœud de la scène
		queue_free()

# Fonction appelée lorsque le nœud quitte la scène
func _exit_tree():
	# Obtenir le parent de ce nœud
	var parent = get_parent()
	
	# Si le parent existe, appeler la fonction _on_target_exited sur le parent avec la position de ce nœud
	if parent != null:
		parent._on_target_exited(position)
