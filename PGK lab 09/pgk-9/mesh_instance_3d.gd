extends MeshInstance3D

@export var speed: float = 5.0
@export var LIMIT_X: float = 3.0
@export var LIMIT_Y: float = 2.0

func _process(delta):
	var direction = Vector2.ZERO

	if Input.is_action_pressed("ui_left"):
		direction.x -= 1
	if Input.is_action_pressed("ui_right"):
		direction.x += 1
	if Input.is_action_pressed("ui_up"):
		direction.y += 1
	if Input.is_action_pressed("ui_down"):
		direction.y -= 1

	position.x += direction.x * speed * delta
	position.y += direction.y * speed * delta

	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)
