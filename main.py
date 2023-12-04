from designer import *
from dataclasses import dataclass
from random import randint

CAT_SPEED = 9
JUMP_HEIGHT = 16
MAX_JUMP_TIME = 1
PLATFORM_FALL_SPEED = 9 # How fast the game is going/cat is moving
NUM_PLATFORMS = 16  # Number of platforms to start with
MONSTER_FALL_SPEED= 3
COIN_FALL_SPEED= 2
COINS= 8 # Number of coins to start with


set_window_size(1024, 768)
background_image("https://c4.wallpaperflare.com/wallpaper/826/698/360/cemetery-tombstones-full-moon-road-wallpaper-preview.jpg")

@dataclass
class World:
    cat: DesignerObject
    cat_speed: int
    jumping: bool
    jump_time: float
    platforms: list[DesignerObject]
    monsters: list[DesignerObject]
    coins: list[DesignerObject]
    bullets: list[DesignerObject]
    collected_coins: int
    score_display: DesignerObject
    ghosts: list[DesignerObject]

def create_world() -> World:
    cat = emoji("cat", scale=1.2) # Creating the cat with a specified size
    cat.x = get_width() / 2
    cat.y = get_height() / 2

    platforms = [create_platform() for _ in range(NUM_PLATFORMS)]
    monsters = [create_monster() for _ in range(NUM_PLATFORMS // 2)] # Fewer monsters when divided by a larger number 
    coins = [create_coin() for _ in range(COINS)]
    bullets= []
    collected_coins = 0  # Initialize collected coins
    score_display= text("deepskyblue", "0", 23, get_width() - 100,20, font_name='papyrus')
    ghosts= []

    return World(cat, CAT_SPEED, False, 0.0, platforms, monsters, coins, bullets, collected_coins, score_display, ghosts)

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
        
        else:
            world.jumping = False
            world.jump_time = 0.0

    # Simulate gravity when not jumping
    elif world.cat.y < get_height() - world.cat.height:
        world.cat.y += PLATFORM_FALL_SPEED
        
 
def handle_space_key(world: World, keys: str): # The cat can also jump since it has a "jetpack" equipped
    if keys == "space":
        world.jumping = not world.jumping

def create_platform() -> DesignerObject:
    platform = emoji("⬜")
    platform.scale_x = 2.2 # Make the platform wider
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
    monster.scale_x = 0.5 # How wide the monster is 
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
            
    while len(world.monsters) < NUM_PLATFORMS // 3:
        monster = create_monster()
        world.monsters.append(monster)
        
            
def grow_monsters(world: World): # Scaling theme initiated in my game
    for monster in world.monsters:
        monster.scale_x += .001
        monster.scale_y += .001
        
def create_coin() -> DesignerObject:
    coin = emoji("🧶")  # Using the yarn emoji
    coin.scale_x = 0.5
    coin.scale_y = 0.5
    coin.x = randint(0, get_width() - int(coin.width))
    coin.y = randint(0, get_height() - int(coin.height))
    return coin

def make_coins(world: World):
    # Making the coins appear at random intervals througout the screen falling down
    for coin in world.coins:
        coin.y += COIN_FALL_SPEED
        if coin.y + coin.height > get_height():
            coin.x = randint(0, get_width() - int(coin.width))
            coin.y= 0.0
    # Makes the coins keep appearing instead of stopping after only collecting the starting number, which was 8 coins         
    while len(world.coins) < NUM_PLATFORMS // 3:
        coin = create_coin()
        world.coins.append(coin)
            
def handle_shoot_key(world: World, keys: str):
    # When pressing the "s" key, the user can shoot bullets to destroy the bats
    if keys == "s":
        create_bullet(world)

def create_bullet(world: World):
    bullet = emoji("💥")  # Create a bullet emoji
    bullet.x = world.cat.x + world.cat.width / 2  # Set bullet's initial position
    bullet.y = world.cat.y - 20  # Adjust bullet's initial y position above the cat
    bullet.speed_y = -15  # Set bullet's speed
    world.bullets.append(bullet)  # Add the bullet to the list of bullets

def shoot_bullets(world: World):
    for bullet in world.bullets:
        bullet.y += bullet.speed_y
        
        # Check collision between bullets and monsters
        for monster in world.monsters:
            if colliding(bullet, monster):
                world.bullets.remove(bullet)  # Remove the bullet
                world.monsters.remove(monster)  # Remove the monster
                destroy(bullet)  # Destroy the bullet
                destroy(monster)  # Destroy the monster
                break  # Exit the loop as the bullet hit a monster
            
        # Remove bullets that have gone off the screen
        if bullet.y > 1024:
            world.bullets.remove(bullet)
            
def collect_coins(world: World):
    for coin in world.coins:
        if colliding(world.cat, coin):
            world.coins.remove(coin)  # Remove the collected coin
            destroy(coin)  # Destroy the coin
            world.collected_coins += 1  # Increase collected coins counter
            update_score_display(world)  # Update the score display
            
            if world.collected_coins >= 10:  
                world.monsters.append(create_different_monster())  # Add the ghost to the list of monsters
               
def update_score_display(world: World):
    # Update the displayed score
    set_text(world.score_display, f"Score: {world.collected_coins}")
  
def create_different_monster() -> DesignerObject:
    # Define the creation of a different type of monster
    ghost = emoji("ghost")  # For example, using the ghost emoji as a different monster
    ghost.scale_x = 0.5  # Adjust size if needed
    ghost.scale_y = 0.5
    ghost.x = randint(0, get_width() - int(ghost.width))
    ghost.y = randint(0, get_height() - int(ghost.height))
    return ghost

def grow_ghosts(world: World): # Scaling theme initiated in my game
    for monster in world.ghosts:
        ghost.scale_x += .001
        ghost.scale_y += .001
        
def display_game_over(score):
    # Create a game over message and display it across the screen with the score
    game_over_text = text("red", "Game Over", 85, get_width() / 2, get_height() / 2 - 50, font_name='papyrus')
    show(game_over_text)
    score_text = text("deepskyblue", f"Yarns Collected: {score}", 40, get_width() / 2, get_height() / 2 + 50, font_name='papyrus')
    show(score_text)
   

def cat_falling(world: World):
    if world.cat.y > 720:
        display_game_over(world.collected_coins)  # Pass the collected coins as the score parameter
        pause()

def check_collision(world: World) -> bool:
    # Check for collision between the cat and monsters
    for monster in world.monsters:
        if colliding(world.cat, monster):
            display_game_over(world.collected_coins)  # Pass the collected coins as the score parameter
            pause()  # Exit the function to stop the game

           
when("starting", create_world)
when("updating", move_cat)
when("updating", handle_jump)
when("updating", cat_falling)
when("typing", handle_space_key)
when("updating", handle_platform_collision)
when("updating", make_monster)
when("updating", grow_monsters)
when("updating", make_coins)
when("typing", handle_shoot_key)
when("updating", shoot_bullets)
when("updating", collect_coins)
when("updating", grow_ghosts)
when("updating", check_collision)
start()
