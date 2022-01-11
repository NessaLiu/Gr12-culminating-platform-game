# ICS4U Culminating Project - "Summer Showdown Platform Game"
# Vanessa Liu
# Date: June 2021
# Purpose: Create a platform game using Python and Pygame

# import modules and initialize them
import pygame
import csv
import random
import imgbutton

pygame.init()
pygame.mixer.init()

# initialize the screen dimensions
SCREEN_WIDTH = 700 # constant
SCREEN_HEIGHT = 450 # constant
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # set screen size
pygame.display.set_caption("WELCOME TO THE SUMMER SHOWDOWN PLATFORM GAME!") # set game caption

# set frame rate
clock = pygame.time.Clock()
FPS = 60 # frames per second

# define game variables
start = False # track if the player starts game
finished = False # track if player completes all levels
MAX_LVLS = 3
GRAVITY = 0.7
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS # size of individual tiles
TILE_TYPES = 29 # unique tiles
level = 1 # game level starts at 1
SCROLL_LIMIT = 200 # track when to start scrolling
scroll_left = False
scroll_right = False
scroll = 0 # for background image location
scroll_speed = 1 # how fast screen scrolls
background_scroll = 0

# music and sound effects
shoot_sfx = pygame.mixer.Sound('sounds/shoot.mp3')
damage_sfx = pygame.mixer.Sound('sounds/dmg.mp3')
bg_music = pygame.mixer.music.load('sounds/bg_music.mp3')
shoot_sfx.set_volume(0.7)
damage_sfx.set_volume(0.7)
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1) # music repeats indefinitely

# define player variables
move_right = False
move_left = False
player_attack = False

'''load in images'''
# button images
play_btn_img = pygame.image.load('buttons/play.png').convert_alpha()
exit_btn_img = pygame.image.load('buttons/exit.png').convert_alpha()
try_again_img = pygame.image.load('buttons/try_again.png').convert_alpha()
game_over_img = pygame.image.load('buttons/game_over.png').convert_alpha()

# background images
trees1_img = pygame.image.load('background/trees1.png').convert_alpha()
trees2_img = pygame.image.load('background/trees2.png').convert_alpha()
mountain_img = pygame.image.load('background/mountain.png').convert_alpha()
sky_img = pygame.image.load('background/sky.png').convert_alpha()

# player and enemy images stored in list of a list --> # (0 = idle, 1 = run, 2 = jump, 3 = attack, 4 = die)
playerIdle = [pygame.image.load('player/pi0.png'), pygame.image.load('player/pi1.png'), pygame.image.load('player/pi2.png'), pygame.image.load('player/pi3.png')]
playerRun = [pygame.image.load('player/pr0.png'), pygame.image.load('player/pr1.png'), pygame.image.load('player/pr2.png'), pygame.image.load('player/pr3.png'), pygame.image.load('player/pr4.png'), pygame.image.load('player/pr5.png')]
playerJump = [pygame.image.load('player/pj0.png')]
playerAttack = [pygame.image.load('player/pa0.png'), pygame.image.load('player/pa1.png'), pygame.image.load('player/pa2.png'), pygame.image.load('player/pa3.png'), pygame.image.load('player/pa4.png'), pygame.image.load('player/pa5.png'), pygame.image.load('player/pa6.png'), pygame.image.load('player/pa7.png'), pygame.image.load('player/pa8.png')]
playerDie = [pygame.image.load('player/pd0.png'), pygame.image.load('player/pd1.png'), pygame.image.load('player/pd2.png'), pygame.image.load('player/pd3.png'), pygame.image.load('player/pd4.png'), pygame.image.load('player/pd5.png'), pygame.image.load('player/pd6.png')]
player_animations = [playerIdle, playerRun, playerJump, playerAttack, playerDie]

enemyIdle = [pygame.image.load('enemy/ei0.png'), pygame.image.load('enemy/ei1.png'), pygame.image.load('enemy/ei2.png'), pygame.image.load('enemy/ei3.png'), pygame.image.load('enemy/ei4.png'), pygame.image.load('enemy/ei5.png'), pygame.image.load('enemy/ei6.png'), pygame.image.load('enemy/ei7.png')]
enemyRun = [pygame.image.load('enemy/er0.png'), pygame.image.load('enemy/er1.png'), pygame.image.load('enemy/er2.png'), pygame.image.load('enemy/er3.png'), pygame.image.load('enemy/er4.png'), pygame.image.load('enemy/er5.png'), pygame.image.load('enemy/er6.png'), pygame.image.load('enemy/er7.png')]
enemyJump = []
enemyAttack = [pygame.image.load('enemy/ea0.png'), pygame.image.load('enemy/ea1.png'), pygame.image.load('enemy/ea2.png'), pygame.image.load('enemy/ea3.png'), pygame.image.load('enemy/ea4.png'), pygame.image.load('enemy/ea5.png'), pygame.image.load('enemy/ea6.png')]
enemyDie = [pygame.image.load('enemy/ed0.png'), pygame.image.load('enemy/ed1.png'), pygame.image.load('enemy/ed2.png'), pygame.image.load('enemy/ed3.png'), pygame.image.load('enemy/ed4.png')]
enemy_animations = [enemyIdle, enemyRun, enemyJump, enemyAttack, enemyDie]

# tile images (store tiles in list)
img_list = []
for x in range(TILE_TYPES): # add each tile to the img list
    img = pygame.image.load(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# arrow image
projectile_img = pygame.image.load('img/icons/projectile.png').convert_alpha()

# item boxes' images
health_box_img = pygame.image.load('items/healthpack.png').convert_alpha()
health_box_img = pygame.transform.scale(health_box_img, (int(health_box_img.get_width() * 0.1), int(health_box_img.get_height() * 0.1)))
ammo_box_img = pygame.image.load('items/ammo.png').convert_alpha()
ammo_box_img = pygame.transform.scale(ammo_box_img, (int(ammo_box_img.get_width() * 0.1), int(ammo_box_img.get_height() * 0.1)))
item_boxes = {
    'health'    : health_box_img,
    'ammo'      : ammo_box_img,
}

# define colours and font
BG = (255, 248, 115)#(200, 230, 150)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('couriernewbold', 25)

'''------------ FUNCTIONS ------------'''

def write_text(text, font, text_colour, x, y):
    '''This function writes text onto the screen with specific fonts and colours.'''
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))

def draw_bg():
    '''This function draws the background of the game.'''
    # fill with solid colour
    screen.fill(BG)
    width = sky_img.get_width()
    # background images
    for x in range(6): # keep repeating background images
        screen.blit(sky_img, ((x * width) - background_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - background_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 180))
        screen.blit(trees1_img, ((x * width) - background_scroll * 0.7, SCREEN_HEIGHT - trees1_img.get_height() - 100))
        screen.blit(trees2_img, ((x * width) - background_scroll * 0.8, SCREEN_HEIGHT - trees2_img.get_height()))
# end of draw_bg() function

def restart_lvl():
    '''This function is used when restarting a level to reset the level.'''
    # empty all groups
    enemy_group.empty()
    projectile_group.empty()
    item_box_group.empty()
    deco_group.empty()
    water_group.empty()
    exit_group.empty()

    # reset map's data by making an empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS  # one row (starts with empty tile)
        data.append(r)

    return data
# end of restart_lvl() function

'''------------ CLASSES ------------'''

class Character(pygame.sprite.Sprite):
    '''
    This class creates a single character (whether it be the player's character or other enemies)
    which includes its own unique attributes, possible actions and updates.
    '''

    # initialize the attributes
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True # condition for certain actions
        self.char_type = char_type
        self.speed = speed # character's speed (constant)
        self.ammo = ammo # changes
        self.start_ammo = ammo # won't change
        self.attack_cooldown = 0
        self.health = 100 # track character's health
        self.max_health = self.health # all character's have same max health
        self.coins = 0 # track how many coins were collected
        self.direction = 1 # player's direction (1 = right, -1 = left)
        self.jump = False
        self.in_air = True # assume player is in air until they land on something
        self.vel_y = 0 # vertical velocity
        self.flip = False # track if player flip's direction
        self.animation_list = [] # list of images in the character's animation
        self.frame_index = 0 # index of the animation list
        self.action_index = 0 # (0 = idle, 1 = run, 2 = jump, 3 = attack, 4 = die)
        self.update_time = pygame.time.get_ticks() # tracks when the animation was last updated
        # attributes for enemy ai only
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,100,20) # vision range for enemies to see player
        self.idle = False
        self.idle_counter = 0

        if self.char_type == 'player':
            self.animation_list = player_animations
        else:
            self.animation_list = enemy_animations
        img = self.animation_list[self.action_index][self.frame_index]
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)) )
        # create a boundary rectangle box for the image and set the location at it's center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width() # image width
        self.height = self.image.get_height() # image height

    #end of initialization

    def update(self):
        '''This method handles all the necessary updates for the character.'''

        # call different update methods
        self.update_animation()
        self.alive_check()
        # update attack cool-down
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1 # slowly decrease the cool down

    def move(self, move_left, move_right):
        '''This method controls the movement of the character.'''
        # reset movement variables
        dx = 0 # change in x direction
        dy = 0 # change in y direction

        #screen variable
        scroll = 0

        # change movement variables depending on which way character is moving (left vs right)
        if move_left:
            dx = -self.speed # speed moving in negative direction
            self.flip = True # the player's image flips
            self.direction = -1 # player facing left
        if move_right:
            dx = self.speed # speed moving in positive direction
            self.flip = False  # the player's image is no longer flipped
            self.direction = 1  # player facing right

        # jump
        if self.jump and self.in_air == False: # can't jump more than once at a time
            self.vel_y = -12 # player jumps
            self.jump = False # reset jump state
            self.in_air = True

        # apply gravity and update the y displacement
        self.vel_y += GRAVITY # gravity brings it back down slowly
        if self.vel_y > 12:
            self.vel_y = self.vel_y # if y velocity goes past a value, set it back
        dy += self.vel_y

        # check collision w/ map tiles
        for tile in map.block_list:
            # each tile stored in tuple (img at [0], rectangle at [1])
            # check x-direction --> use img's rectangle to check collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0 # if the new point creates a collision, the player will not move past
            # check y-direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check collision for block under or above player
                # if player is jumping when the collision happens, set their y-velocity to 0 so they stop moving
                if self.vel_y < 0:
                    self.vel_y = 0
                    # update their vertical position
                    dy = tile[1].bottom - self.rect.top
                # if player is moving down when the collision happens, set their y-velocity
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    # update their vertical position
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check if player reaches end of level (collision with exit sign)
        lvl_passed = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            lvl_passed = True # they completed the level

        # check if player collected a coin
        if pygame.sprite.spritecollide(self, coin_group, True):
            self.coins += 1

        # check if player falls into water or off the map
        if pygame.sprite.spritecollide(self, water_group, False) or self.rect.bottom > SCREEN_WIDTH:
            self.health = 0

        # make sure player can't go off the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                # if the next horizontal movement will move player off the screen,
                # set their horizontal displacement to 0
                dx = 0

        # update the image's rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update screen's scrolling based on player position
        if self.char_type == 'player':
            # check character going off screen or reaches the end of the level
            if (self.rect.right > SCREEN_WIDTH - SCROLL_LIMIT and background_scroll < (map.length_lvl * TILE_SIZE) - SCREEN_WIDTH)\
                    or (self.rect.left < SCROLL_LIMIT and background_scroll > abs(dx)):
                # keep playing in same position but background moves
                self.rect.x -= dx
                scroll = -dx # scroll at the pace player moves in the opposite direction

        # return the scroll value and pass boolean
        return scroll, lvl_passed
    # end of move method

    def attack(self):
        '''This method creates projectiles for the character's attack and handles the actions after an attack occurs.'''

        # create projectile instance and add it to the group
        # attack if the cool-down is over and the character has ammo
        if self.attack_cooldown == 0 and self.ammo > 0:
            self.attack_cooldown = 7
            if self.char_type == 'player': # character is the player
                if self.frame_index == 8: # last frame in player's attack animation
                    # play shooting sound effect
                    shoot_sfx.play()
                    projectile = Projectile(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),
                                            self.rect.centery + 10, self.direction)
                    projectile_group.add(projectile)
                    self.ammo -= 1 # reduce ammo
            else: # character is an enemy
                if self.frame_index == 6: # last frame in enemy's attack animation
                    # play shooting sound effect
                    shoot_sfx.play()
                    projectile = Projectile(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),
                                            self.rect.centery + 10, self.direction)
                    projectile_group.add(projectile)
                    self.ammo -= 1  # reduce ammo
    # end of attack method

    def ai(self):
        '''This method is for the enemy ai to move, shoot, etc.'''

        # complete ai functions if enemy is alive and player is still alive
        if self.alive and player.alive:
            # use random module's randint method to create random integer for setting idle to true
            if self.idle == False and random.randint(1,200) == 1:
                self.update_action(0) # action index 0 = idle
                self.idle = True
                self.idle_counter = 50

            # check if the player is within enemy's vision
            if self.vision.colliderect(player.rect) and player.alive:
                # stop moving, face player and attack
                self.update_action(3) # action index 3 = attack
                self.attack()

            # otherwise, if they don't see they player, they continue moving
            else:
                # if not idle, enemy will be moving left/right
                if self.idle == False:
                    # moving right
                    if self.direction == 1:
                        ai_move_right = True
                    else: # moving left
                        ai_move_right = False
                    ai_move_left = not ai_move_right # move left is the opposite of move right
                    # call move method for the enemy
                    self.move(ai_move_left, ai_move_right)
                    self.update_action(1) # action index 1 = run
                    self.move_counter += 1
                    # update enemy's vision range as they move
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    # when the move counter reaches a certain value, change direction and move back same amount
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    # enemy is idle and decrease idle counter
                    self.idle_counter -= 1
                    # once counter reaches 0, they are no longer idle
                    if self.idle_counter <= 0:
                        self.idle = False
        elif player.alive == False: # if the player dies, enemies become idle
            self.update_action(0) # action index 0 = idle

        # scroll enemies as player moves
        self.rect.x += scroll

    # end of ai method

    def update_animation(self):
        '''This method will flip through the different animation frames of the character's action.'''

        ANIMATION_COOLDOWN = 100 # used for tracking when a frame should change
        # update character's image to its current frame
        self.image = self.animation_list[self.action_index][self.frame_index]

        # check if enough time has passed to change animation frame
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks() # reset timer
            self.frame_index += 1 # increase frame

        # if animation frames run out, reset it
        if self.frame_index >= len(self.animation_list[self.action_index]):
            # if the action is 'die', don't reset
            if self.action_index == 4:
                self.frame_index = len(self.animation_list[self.action_index])-1
            else: # reset for other animations
                self.frame_index = 0
    # end of update_animation method

    def update_action(self, new_action):
        '''This method will change the action of the character when needed'''
        # check if there is a new action - if so, update it
        if new_action != self.action_index:
            self.action_index = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    # end of update_action method

    def alive_check(self):
        '''This method check's if the character is alive'''

        # if the character is dead, change its attributes
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4) # index 4 = die

    # end of alive_check method

    def draw(self):
        '''
        This method inside the Character class is used to display the character image onto the screen.
        '''
        # draw the character, keeping track of it's flip state
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    # end of draw method

class World():
    '''This class is for creating the world. This includes all tiles in the game as well as
    the player, enemies and items.'''
    def __init__(self):
        self.block_list = [] # store obstacle blocks in a list (eg. dirt blocks)

    def examine_data(self, data):
        '''This method processes the world data.'''

        # get length of 1 row the world data (tiles in the level) to know where the end is
        self.length_lvl = len(data[0])

        # iterate through each value in level data file
        for y, row in enumerate(data): # iterate through rows
            for x, tile in enumerate(row): # iterate through columns in each row
                if tile >= 0: # no tile value if -1
                    img = img_list[tile]
                    # create rectangle for the tile image and position it accordingly
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect) # tuple to store each tile data

                    # dirt blocks (0-9 and 28) are obstacles
                    if tile >= 0 and tile <= 9 or tile == 28:
                        self.block_list.append(tile_data)
                    # water blocks (10-14)
                    elif tile >= 10 and tile <= 14:
                        water_block = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water_block)
                    # decoration blocks (15-21)
                    elif tile >=15 and tile <= 21:
                        decoration_block = Deco(img, x * TILE_SIZE, y * TILE_SIZE)
                        deco_group.add(decoration_block)
                    # player tile = 24 --> create a player
                    elif tile == 24:
                        player = Character('player', x * TILE_SIZE, y * TILE_SIZE, 1, 3, 20)
                        health_bar = HealthBar(10, 10, player.health, player.max_health)
                    # enemy tile = 25 --> create enemy
                    elif tile == 25:
                        enemy = Character('enemy', x * TILE_SIZE, y * TILE_SIZE, 1, 2, 20)
                        enemy_group.add(enemy)
                    # health pack = 22
                    elif tile == 22:
                        item_box = Item('health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    # ammo box = 23
                    elif tile == 23:
                        item_box = Item('ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    # coin = 26
                    elif tile == 26:
                        coin = Coin(img, x * TILE_SIZE, y * TILE_SIZE)
                        coin_group.add(coin)
                    # exit tile = 26
                    elif tile == 27:
                        exit_block = ExitSign(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit_block)

        # return the player and their health bar (local variable right now)
        return player, health_bar
    # end of examine_data() method

    def draw_tiles(self):
        '''This method is used to actually draw out each tile into the map.'''
        for tile in self.block_list:
            # each tile is a tuple with image at index 0 and its corresponding rectangle at index 1
            # change x position for scrolling (using x-coord of rectangle)
            tile[1][0] += scroll
            # draw the tile on the screen
            screen.blit(tile[0], tile[1])
    # end of draw_tiles() method

# end of World() class

'''------------ BLOCK CLASSES ------------'''

class Deco(pygame.sprite.Sprite):
    '''This method uses the sprite class and handles the decorative blocks in the map
    that the player does not interact with. (eg. rocks, shrubs, etc.)'''
    # initialize attributes
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # create rectangle for the image and its location
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # update positions of deco blocks as screen scrolls
        self.rect.x += scroll
# end of Deco() class

class Water(pygame.sprite.Sprite):
    '''This method uses the sprite class and handles the water blocks in the map
    that the player can interact with.'''
    # initialize attributes
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # create rectangle for the image and its location
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # update positions of water blocks as screen scrolls
        self.rect.x += scroll
# end of Water() class

class Coin(pygame.sprite.Sprite):
    '''This method uses the sprite class and handles the coin blocks in the map
    that the player can interact with.'''
    # initialize attributes
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # create rectangle for the image and its location
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # update positions of water blocks as screen scrolls
        self.rect.x += scroll
# end of Water() class

class ExitSign(pygame.sprite.Sprite):
    '''This method uses the sprite class and handles the exit sign block in the map
    that the player interacts with to signal the end of the level.'''
    # initialize attributes
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # create rectangle for the image and its location
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # update positions of exit block as screen scrolls
        self.rect.x += scroll
# end of ExitSign() class

'''------------ OTHER CLASSES ------------'''

class Item(pygame.sprite.Sprite):
    '''This class represents the different collectible items and uses the sprite class.'''

    # initialize attributes
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        '''This method checks if the player interacts with an item box'''

        # update positions of item boxes as screen scrolls
        self.rect.x += scroll

        # look for collision with item box and player
        if pygame.sprite.collide_rect(self, player):
            # check what item it is and adjust stats
            if self.item_type == 'health':
                player.health += 25
                # health cannot exceed max health so keep it as it's max health
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'ammo':
                # increase ammo
                player.ammo += 15
            # delete the item after collision
            self.kill()

    # end of update method
# end of Item class

class HealthBar():
    '''This class is used to visually display how much the player has left using
    a sequence of images.'''

    # initialize attributes
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        '''This method draws the health bar and shows new health.'''
        # update current health
        self.health = health

        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150*ratio, 20))
    # end of draw method
# end of HealthBar class

class Projectile(pygame.sprite.Sprite):
    '''This class represents the different arrows used for shooting and uses the sprite class.'''

    # initialize attributes
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 # speed is constant for all projectiles

        # change projectile image direction based on player's direction
        if direction == 1:
            self.image = pygame.transform.flip(projectile_img, True, False)
        else:
            self.image = projectile_img

        # create rectangle around the image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    # end of initialization

    def update(self):
        '''This method moves the projectile and handles the effects of the movement.'''
        # horizontally move considering speed, direction and scroll
        self.rect.x += (self.direction * self.speed) + scroll
        # check if projectile moves off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill # delete arrow

        # check block collision with projectile
        # if the arrow collides with a block tile, delete i
        for tile in map.block_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # check character collision with projectile
        # check if character is hit by arrow
        if pygame.sprite.spritecollide(player, projectile_group, False):
            if player.alive:
                # play damage sound effect
                damage_sfx.play()
                player.health -= 5 # decrease player health
                self.kill() # delete arrow if player is alive

        # check if enemy is hit by arrow (look through all enemies contained in group)
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, projectile_group, False):
                if enemy.alive:
                    # play damage sound effect
                    damage_sfx.play()
                    enemy.health -= 25 # decrease enemy health
                    self.kill() # delete arrow if enemy is alive
    # end of update method
# end of Projectile class

'''------------ SETUP ------------'''

# create image buttons
play_btn = imgbutton.ImageButton(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 - 40, play_btn_img, 3)
exit_btn = imgbutton.ImageButton(SCREEN_WIDTH // 2 + 85, SCREEN_HEIGHT // 2 - 40, exit_btn_img, 3)
try_again_btn = imgbutton.ImageButton(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT //2 - 75, try_again_img, 0.5)

#create sprite groups
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
deco_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS # one row (starts with empty tile)
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',') # delimiter tells what separates values (comma)
    for x, row in enumerate(reader): # use enumerate to count where tile is
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile) # convert tile string to int
# create instance of World class
map = World()
# use return from process_data method to get the player instance and health bar
player, health_bar = map.examine_data(world_data)

'''------------------MAIN GAME LOOP------------------'''

# loop for game to continue running unless they quit the game
game = True
while game:

    if start == False: # the game has not started - show main menu
        # create main menu
        screen.fill(BG)
        write_text('Welcome! Please select an option:', font, BLACK, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100)
        # if play button is clicked, start game
        if play_btn.draw_button(screen):
            start = True
        # if exit button is clicked, exit game
        if exit_btn.draw_button(screen):
            game = False

    elif finished == True: # player completed all levels of the game
        screen.fill(BG)
        write_text('CONGRATULATIONS!', font, BLACK, SCREEN_WIDTH // 2 - 90,
                   SCREEN_HEIGHT // 2 - 150)
        write_text('You have completed the game.', font, BLACK, SCREEN_WIDTH // 2 - 175,
                   SCREEN_HEIGHT // 2 - 100)
        # if play button is clicked, start game
        if play_btn.draw_button(screen):
            finished = False
            # if the play button is pressed, reset game
            level = 1
            background_scroll = 0
            world_data = restart_lvl()  # reset world data
            # load in level data and create world (same level)
            with open(f'level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')  # delimiter tells what separates values (comma)
                for x, row in enumerate(reader):  # use enumerate to count where tile is
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)  # convert tile string to int
            # create instance of World class
            map = World()
            # use return from process_data method to get the player instance and health bar
            player, health_bar = map.examine_data(world_data)
        # if exit button is clicked, exit game
        if exit_btn.draw_button(screen):
            game = False

    else: # run game

        clock.tick(FPS) # slows down character movement
        # draw background and map
        draw_bg()
        map.draw_tiles()

        # display player stats on the screen
        write_text(f'AMMO: {player.ammo}', font, WHITE, 10, 35)
        write_text(f'COINS: {player.coins}', font, WHITE, 10, 60)
        health_bar.draw(player.health)

        #update and draw player
        player.update()
        player.draw()

        # iterate through all enemies to give them ai, update, and draw them
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        # update and draw groups
        projectile_group.update()
        projectile_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)
        deco_group.update()
        deco_group.draw(screen)
        water_group.update()
        water_group.draw(screen)
        coin_group.update()
        coin_group.draw(screen)
        exit_group.update()
        exit_group.draw(screen)

        # update player actions (if alive)
        if player.alive:

            if player.in_air: # player is jumping
                player.update_action(2) # index 2 = jump

            elif player_attack: # player is attacking
                player.attack()
                player.update_action(3) # index 3 = attack

            elif move_left or move_right:
                player.update_action(1) # index 1 = run

            else: # player is not running
                player.update_action(0)  # index 0 = idle

            # get the scroll and level passed values
            scroll, lvl_passed = player.move(move_left, move_right) # for map block rectangles
            # for background images
            background_scroll -= scroll

            # if level has been passed, change level
            if lvl_passed:
                level += 1
                background_scroll = 0
                world_data = restart_lvl()  # reset world data
                if level <= MAX_LVLS: # only load in level data if there is a next lvl
                    # load in level data and create world (new level)
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')  # delimiter tells what separates values (comma)
                        for x, row in enumerate(reader):  # use enumerate to count where tile is
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)  # convert tile string to int
                    # create instance of World class
                    map = World()
                    # use return from process_data method to get the player instance and health bar
                    player, health_bar = map.examine_data(world_data)
                elif level > MAX_LVLS: # the player has completed the game by finishing all available levels
                    finished = True

        # player is dead
        else:
            scroll = 0 # stop background from moving
            if try_again_btn.draw_button(screen):
                # if the try again button is pressed, reset level
                background_scroll = 0
                world_data = restart_lvl() # reset world data
                # load in level data and create world (same level)
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')  # delimiter tells what separates values (comma)
                    for x, row in enumerate(reader):  # use enumerate to count where tile is
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)  # convert tile string to int
                # create instance of World class
                map = World()
                # use return from process_data method to get the player instance and health bar
                player, health_bar = map.examine_data(world_data)


    # check for all events that occur (mouse movement, key down, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # set game to false and exit loop
            game = False

        # check keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player_attack == False: # 'a' key means moving left
                move_left = True
            if event.key == pygame.K_d and player_attack == False: # 'd' key means moving right
                move_right = True
            if event.key == pygame.K_w and player_attack == False: # 'w' key means jumping
                player.jump = True
            if event.key == pygame.K_s: # 's' key means attack
                player_attack = True
                # player can't move left or right when attacking
                move_left = False
                move_right = False
            if event.key == pygame.K_ESCAPE:  # the user exits the game
                game = False

        # check keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: # 'a' key release means not moving left anymore
                move_left = False
            if event.key == pygame.K_d: # 'd' key release means not moving right anymore
                move_right = False
            if event.key == pygame.K_s: # 's' key means shooting
                player_attack = False

    pygame.display.update()

pygame.quit()






