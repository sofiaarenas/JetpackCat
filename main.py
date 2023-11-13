from designer import *
from dataclasses import dataclass
from random import randint

CAT_SPEED = 10
JUMP_HEIGHT = 5
MAX_JUMP_TIME = 1

background_image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbm0vfckr_PWnujY7UvBQpgwzLseaEekwKr85kh9tYgrPU_7MEIQ2Rf6LYYLlq0GgdNXY&usqp=CAU")

@dataclass
class World:
    cat: DesignerObject
    cat_speed: int
    moving_left: bool
    moving_right: bool
    jumping: bool
    jump_time: float
    has_jumped: bool
    platforms: list[DesignerObject]

def create_world()-> World:
    return World(create_cat(), CAT_SPEED, False, False, False, False, False, [])

def create_cat()-> DesignerObject:
    cat = emoji("cat", scale= 1.2)
    cat.x = get_width() / 2
    cat.y = get_height() / 2
    return cat

def move_cat(world: World):
    if world.moving_left:
        world.cat.x -= world.cat_speed
        world.cat.flip_x = False
    if world.moving_right:
        world.cat.x += world.cat_speed
        world.cat.flip_x = True

def handle_jump(world: World):
    MAX_JUMP_HEIGHT = 2 * JUMP_HEIGHT  # Adjust the max jump height as needed

    if world.jumping:
        if world.jump_time < MAX_JUMP_TIME:
            jump_height = JUMP_HEIGHT * (1 - world.jump_time / MAX_JUMP_TIME)
            jump_height = min(jump_height, MAX_JUMP_HEIGHT)
            world.cat.y -= jump_height
            world.jump_time += 0.1
            world.has_jumped = True
        else:
            world.jumping = False
            world.jump_time = 0.0

    # If the cat has jumped, start the falling phase
    elif world.has_jumped:
        if world.jump_time < MAX_JUMP_TIME:
            jump_height = JUMP_HEIGHT * (1 - world.jump_time / MAX_JUMP_TIME)
            jump_height = min(jump_height, MAX_JUMP_HEIGHT)
            world.cat.y += jump_height
            world.jump_time += 0.1
        else:
            world.jumping = False
            world.jump_time = 0.0
            world.has_jumped = False


def stop_moving(world: World, keys: str):
    if keys == "left":
        world.moving_left = False
    if keys == "right":
        world.moving_right = False

def start_moving(world: World, keys: str):
    if keys == "left":
        world.moving_left = True
    if keys == "right":
        world.moving_right = True

def handle_space_key(world: World, keys: str):
    if keys == "space":
        world.jumping = not world.jumping
        
def create_platforms()-> DesignerObject:
    platform = emoji("⬜")
    platform.scale_x = .7
    platform.scale_y = .5
    platform.x = randint(0,get_width())
    platform.y = 1
    return platform


def make_platforms(world: World):
    random_chance = randint(1, 100)
    print(len(world.platforms))
    if (len(world.platforms) < 10) and random_chance == 1:
        world.platforms.append(create_platforms())


when("starting", create_world)
when("updating", move_cat)
when("updating", handle_jump)
when("typing", start_moving)
when("typing", handle_space_key)
when("updating", handle_jump)
when("done typing", stop_moving)
when("updating", make_platforms)
start()
