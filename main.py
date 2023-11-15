from designer import *
from dataclasses import dataclass
from random import randint

CAT_SPEED = 9
JUMP_HEIGHT = 16
MAX_JUMP_TIME = 1
PLATFORM_FALL_SPEED = 9.5  # How fast the game is going/cat is moving
NUM_PLATFORMS = 14  # Number of platforms to start with
MONSTER_FALL_SPEED= 2.5

background_image("https://c4.wallpaperflare.com/wallpaper/826/698/360/cemetery-tombstones-full-moon-road-wallpaper-preview.jpg")

@dataclass
class World:
    cat: DesignerObject
    cat_speed: int
    jumping: bool
    jump_time: float
    platforms: list[DesignerObject]
    monsters: list[DesignerObject]

def create_world() -> World:
    cat = emoji("cat", scale=1.2) # Creating the cat with a specified size
    cat.x = get_width() / 2
    cat.y = get_height() / 2

    platforms = [create_platform() for _ in range(NUM_PLATFORMS)]
    monsters = [create_monster() for _ in range(NUM_PLATFORMS // 2)]
    
    return World(cat, CAT_SPEED, False, 0.0, platforms, monsters)

def move_cat(world: World):
    world.cat.x = get_mouse_x()  # Move the cat horizontally with the mouse

def handle_jump(world: World):
    MAX_JUMP_HEIGHT = 2 * JUMP_HEIGHT

    if world.jumping:
        if world.jump_time < MAX_JUMP_TIME:
            jump_height = JUMP_HEIGHT * (1 - world.jump_time / MAX_JUMP_TIME)
            jump_height = min(jump_height, MAX_JUMP_HEIGHT)
            world.cat.y -= jump_height
            world.jump_time += 0.1
            
            # Updating and creating platforms
            new_platforms = []

            for platform in world.platforms:
                platform.y += PLATFORM_FALL_SPEED

                # Check for platforms that are no longer visible
                if platform.y + platform.height > get_height():
                    platform.x = randint(0, get_width() - int(platform.width))
                    platform.y= 0
                    #new_platforms.append(platform)
                #else:
                    # Replace the platforms that are no longer visible
                    #world.platforms.append(create_platform())

            #world.platforms = new_platforms
            
            #if world.cat.y < get_height() / 2:
                #world.platforms.append(create_platform())
                
        
        else:
            world.jumping = False
            world.jump_time = 0.0

    # Simulate gravity when not jumping
    elif world.cat.y < get_height() - world.cat.height:
        world.cat.y += PLATFORM_FALL_SPEED

def create_platform() -> DesignerObject:
    platform = emoji("⬜")
    platform.scale_x = 2.0  # Make the platform wider
    platform.scale_y = 0.5
    platform.x = randint(0, get_width() - int(platform.width))
    platform.y =  randint(0, get_height() - int(platform.height))
    return platform

def make_platforms(world: World):
    new_platforms = []

    for platform in world.platforms:
        platform.y -= PLATFORM_FALL_SPEED

        # Check for platforms that are no longer visible
        if platform.y + platform.height > 0:
            new_platforms.append(platform)
        else:
            # Replace the platforms that are no longer visible
            new_platforms.append(create_platform())

    world.platforms = new_platforms

def platform_collision(cat: DesignerObject, platform: DesignerObject) -> bool:
    return (
        cat.x < platform.x + platform.width and
        cat.x + cat.width > platform.x and
        cat.y < platform.y + platform.height and
        cat.y + cat.height > platform.y
    )

def handle_platform_collision(world: World):
    for platform in world.platforms:
        if platform_collision(world.cat, platform) and not world.jumping:
            world.jumping = True
            world.jump_time = 0.0
            
def create_monster() -> DesignerObject:
    monster = emoji("bat")  # Using the bat emoji as my monster
    monster.scale_x = 0.5 # How wide it is 
    monster.scale_y = 0.5
    monster.x = randint(0, get_width() - int(monster.width))
    monster.y = randint(0, get_height() - int(monster.height))
    return monster

def make_monster(world: World):
    new_monsters= []
    for monster in world.monsters:
        monster.y += MONSTER_FALL_SPEED
        if monster.y + monster.height > get_height():
            monster.x = randint(0, get_width() - int(monster.width))
            monster.y= 0
            
when("starting", create_world)
when("updating", move_cat)
when("updating", handle_jump)
when("updating", handle_platform_collision)
when("updating", make_monster)
start()
