from designer import *
from dataclasses import dataclass
from random import randint

CAT_SPEED = 9 
JUMP_HEIGHT = 16 # Maximum height the cat can reach when jumping
MAX_JUMP_TIME = 1 # The maximum duration of time the cat character can ascend during a jump
PLATFORM_FALL_SPEED = 9 # The vertical speed at which platforms fall or move downwards.
NUM_PLATFORMS = 16  # Number of platforms to start with
MONSTER_FALL_SPEED= 3 # The vertical speed at which monsters fall or move downwards
COIN_FALL_SPEED= 2  # The vertical speed at which coins fall or move downwards
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

    platforms = [create_platform() for platform in range(NUM_PLATFORMS)]
    monsters = [create_monster() for monster in range(NUM_PLATFORMS // 2)] # Fewer monsters when divided by a larger number 
    coins = [create_coin() for coin in range(COINS)]
    bullets= []
    collected_coins = 0  # Initialize collected coins
    score_display= text("deepskyblue", "0", 23, get_width() - 100,20, font_name='papyrus')
    ghosts= []

    return World(cat, CAT_SPEED, False, 0.0, platforms, monsters, coins, bullets, collected_coins, score_display, ghosts)

def move_cat(world: World):
    world.cat.x = get_mouse_x()  # Move the cat horizontally with the mouse

def handle_jump(world: World):
    """
    This function simulates jumping and gravity mechanics for the cat in the game. It handles the jumping behavior of the cat
    within the game. It calculates the jump height based on time and adjusts the cat's vertical position.
    Additionally, it manages the creation and updating of platforms while the cat is in motion.
    """
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
        
 
def handle_space_key(world: World, keys: str): # The cat can also jump since it has a "jetpack" equipped by pressing spacekey
    if keys == "space":
        world.jumping = not world.jumping

def create_platform() -> DesignerObject:
    # Creating the platforms
    platform = emoji("⬜")
    platform.scale_x = 2.2 # Make the platform wider
    platform.scale_y = 0.5
    platform.x = randint(0, get_width() - int(platform.width))
    platform.y =  randint(0, get_height() - int(platform.height))
    return platform

def make_platforms(world: World):
    """
    Updates the positions of platforms and replaces those that have moved off-screen.

    This function iterates through each platform in the world, moving them according to the
    PLATFORM_FALL_SPEED. Platforms that move off the top of the screen are no longer visible,
    and new platforms are created to replace them.
    """
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
    """
    Checks if the cat is colliding with a platform.

    Parameters:
    cat (DesignerObject): The cat character object.
    platform (DesignerObject): The platform object.

    Returns:
    bool: True if the cat is colliding with the platform, False otherwise.
    """
    return (
        cat.x < platform.x + platform.width and
        cat.x + cat.width > platform.x and
        cat.y < platform.y + platform.height and
        cat.y + cat.height > platform.y
    )

def handle_platform_collision(world: World):
    """
    Checks for collisions between the cat and platforms in the game world and initiates a jump if a collision is detected.

    This function iterates through each platform in the world and uses the `platform_collision` function to check
    for a collision with the cat. If a collision is detected and the cat is not already jumping, it sets the world's
    jumping state to True and resets the jump time to allow the cat to jump off the platform.
    """
    for platform in world.platforms:
        if platform_collision(world.cat, platform) and not world.jumping:
            world.jumping = True
            world.jump_time = 0.0
            
def create_monster() -> DesignerObject:
    """
    This function generates a monster DesignerObject using the bat emoji as the monster image.
    It sets the scale, width, and height for the monster, positions it randomly within the game window,
    and returns the created monster object.
    """
    monster = emoji("bat")  # Using the bat emoji as my monster
    monster.scale_x = 0.5 # How wide the monster is 
    monster.scale_y = 0.5
    monster.x = randint(0, get_width() - int(monster.width))
    monster.y = randint(0, get_height() - int(monster.height))
    return monster


def make_monster(world: World):
    """
    This function moves each monster down the screen at a constant fall speed. If a monster moves past the bottom of the screen,
    it is repositioned to the top at a random horizontal location. If there are fewer monsters than a third of the number of
    platforms, new monsters are created and added to the world until this condition is met.
    """
    new_monsters= []
    for monster in world.monsters:
        monster.y += MONSTER_FALL_SPEED
        if monster.y + monster.height > get_height():
            monster.x = randint(0, get_width() - int(monster.width))
            monster.y= 0
            
    while len(world.monsters) < NUM_PLATFORMS // 3:
        monster = create_monster()
        world.monsters.append(monster)
        
            
def grow_monsters(world: World):
    """
    Gradually increases the size of the monster.

    This function iterates through each monster in the world (the bat) and increments its scale in both the x and y
    dimensions by a small amount. This simulates a scaling theme where monsters grow in size over time, making the
    game progressively more challenging.
    """
    for monster in world.monsters:
        monster.scale_x += .001
        monster.scale_y += .001
        
def create_coin() -> DesignerObject:
    """
    Creates a coin object represented by an emoji and initializes its size and position.

    This function creates a new coin object using a yarn emoji, sets its scale to half the original size,
    and randomly positions it within the bounds of the game screen. The coin's x and y coordinates are set
    to random values so they appear randomly on the screen.
    """
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
    # When pressing the "S" key, the user can shoot bullets to destroy the bats
    if keys == "s":
        create_bullet(world)

def create_bullet(world: World):
    bullet = emoji("💥")  # Create a bullet emoji
    bullet.x = world.cat.x + world.cat.width / 2  # Set bullet's initial position
    bullet.y = world.cat.y - 20  # Adjust bullet's initial y position above the cat
    bullet.speed_y = -15  # Set bullet's speed
    world.bullets.append(bullet)  # Add the bullet to the list of bullets

def shoot_bullets(world: World):
    """
    Updates the positions of bullets, checks for collisions with monsters, and handles the removal and destruction of bullets and monsters.

    This function iterates through each bullet in the world, updating its position based on its speed. It checks for collisions
    between each bullet and the monsters in the world. If a collision is detected, both the bullet and the monster are removed
    from the world and destroyed. The function also removes any bullets that have gone off the screen.
    """
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

def grow_ghosts(world: World):
# Makes the ghosts gradually get bigger in size
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
    """
    This function checks the cat's y-coordinate to determine if it has fallen off the bottom of the screen.
    If the cat's y-coordinate is greater than the defined threshold (720), it calls the `display_game_over`
    function to show the game over screen with the number of collected coins as the score, and then pauses the game.
    """
    if world.cat.y > 720: 
        display_game_over(world.collected_coins)  # Pass the collected coins as the score parameter
        pause()

def check_collision(world: World) -> bool:
    """
    This function iterates through the monsters in the game world and checks for collisions with the cat.
    If a collision is detected, it displays the game over message with the collected coins as the score parameter
    and pauses the game before exiting the function to stop the game execution.
    """
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
