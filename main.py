from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random

noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000))

app = Ursina()

selected_block = "grass"

player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 1)
)

block_textures = {
    "grass": load_texture("assets/textures/groundEarth.png"),
    "dirt": load_texture("assets/textures/groundMud.png"),
    "stone": load_texture("assets/textures/wallStone.png"),
    "bedrock": load_texture("assets/textures/stone07.png"),
}

class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position=position,
            model="assets/models/block_model.obj",
            scale=1,
            origin_y=-0.5,
            texture=block_textures.get(block_type),
            collider="box"
        )
        self.block_type = block_type

mini_block = Entity(
    parent=camera,
    model="assets/models/block_model.obj",
    scale=0.2,
    texture=block_textures.get(selected_block),
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -5, 0)
)

min_height = -5
for x in range(-10, 10):
    for z in range(-10, 10):
        height = noise([x * 0.02, z * 0.02])
        height = math.floor(height * 7.5)

        for y in range(height, min_height - 1, -1):
            if y == min_height:
                block = Block((x, y, z), "bedrock")
            elif y == height:
                block = Block((x, y, z), "grass")
            elif height - y > 2:
                block = Block((x, y, z), "stone")
            else:
                block = Block((x, y, z), "dirt")
                
def input(key):
    global selected_block;

    if key == "right mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)

    if key == "left mouse down" and mouse.hovered_entity:
        if mouse.hovered_entity.block_type != "bedrock":
            destroy(mouse.hovered_entity)

    if key == "1":
        selected_block = "grass"
    if key == "2":
        selected_block = "dirt"
    if key == "3":
        selected_block = "stone"

            
def update():
    mini_block.texture = block_textures.get(selected_block)

app.run()