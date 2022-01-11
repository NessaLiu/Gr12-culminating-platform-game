import pygame
import imgbutton
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 450
LOWER_MARGIN = 200
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16 # rows for gris
MAX_COLS = 150 # columns for grid
TILE_SIZE = SCREEN_HEIGHT // ROWS # size of 1 tile
TILE_TYPES = 29 # number of unique tiles
level = 0 # track game level
current_tile = 0 # track the tile number for tile buttons
scroll_left = False
scroll_right = False
scroll = 0 # for background image location
scroll_speed = 1 # how fast screen scrolls

# load images
trees1_img = pygame.image.load('background/pine1.png').convert_alpha()
trees2_img = pygame.image.load('background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('background/mountain.png').convert_alpha()
sky_img = pygame.image.load('background/sky_cloud.png').convert_alpha()
# store tiles in a list
img_list = []
for x in range(TILE_TYPES): # iterate through all unique tiles and add to list
    img = pygame.image.load(f'tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) # scale
    img_list.append(img)
# save/data load images
save_img = pygame.image.load('saving/save_button.png').convert_alpha()
load_img = pygame.image.load('saving/load_button.png').convert_alpha()


# define colours and font
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
font = pygame.font.SysFont('Futura', 25)

# create empty tile list for the world (list of lists)
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS # each row has 150 columns -- one "r" list is one row
    world_data.append(r)

# create ground (the bottom row will all be ground)
for tile in range(0, MAX_COLS):
    # for each tile in the last row, make it the 5th tile image (ground)
    world_data[ROWS - 1][tile] = 5

def draw_text(text, font, text_colour, x, y):
    '''This function outputs text onto the screen.'''
    # convert text to image and draw it on the screen
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))
# end of draw_text() function

def draw_bg():
    '''This function is used for drawing the background'''
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(6):
        screen.blit(sky_img, ((x * width)- scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width)- scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 180))
        screen.blit(trees1_img, ((x * width)- scroll * 0.7, SCREEN_HEIGHT - trees1_img.get_height() - 100))
        screen.blit(trees2_img, ((x * width)- scroll * 0.8, SCREEN_HEIGHT - trees2_img.get_height()))
# end of draw_bg() function

def draw_grid():
    '''This function draws a grid on the background.'''
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))
# end of draw_grid() function

def draw_world():
    '''This function will draw all the tiles onto the world.'''
    # iterate through rows in the world data (must be enumerated to count where we are in the list)
    for y, row in enumerate(world_data):
        # iterate through each row to get each tile
        for x, tile in enumerate(row):
            if tile >= 0: # value less than 0 (-1) means empty
                #draw the corresponding tile
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
#end of draw_world() function

'''create buttons'''
# for save/load buttons
save_button = imgbutton.ImageButton(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 70, save_img, 0.25)
load_button = imgbutton.ImageButton(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 70, load_img, 0.2)

# for tile buttons
button_list = [] # make a button list
button_col = 0  # button columns
button_row = 0  # button rows
for i in range(len(img_list)): # create instances of buttons for each tile type
    tile_button = imgbutton.ImageButton(SCREEN_WIDTH + (60 * button_col) + 50, 60 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    # after an instance is created, shift over for the next on
    button_col += 1
    if button_col == 4: # if there are 3 buttons in the column already, go to next row
        button_row += 1
        button_col = 0 # reset number of columns


'''~~~~~~~~~MAIN LOOP~~~~~~~~~~'''

run = True
while run:

    clock.tick(FPS)

    # draw background and screen
    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 200)
    draw_text('Press UP or DOWN to change level.', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 150)

    # save and load
    if save_button.draw_button(screen):
        # if save button clicked, save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',') # delimiter tells what to separate values by
            # iterate through each row and add data to file
            for row in world_data:
                writer.writerow(row)

    if load_button.draw_button(screen):
        # if load button is clicked, load in level data
        # reset scroll back to the start of level
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',') # delimiter tells what to separate values by
            # iterate through the rows the csv file
            for x, row in enumerate(reader):
                # iterate through each column in the row to get each individual tile
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile) # convert to int

    '''draw tile panel + tiles'''
    # tile panel
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # iterate through each tile in the list to make a button using the draw_button method
    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list): # use enumerate to track count of buttons
        if i.draw_button(screen):
            current_tile = button_count # store what tile is selected

    # highlight tile button when selected
    pygame.draw.rect(screen, WHITE, button_list[current_tile].rect, 3)

    # scroll map
    if scroll_left == True and scroll > 0: # left limit
        scroll -= 5 * scroll_speed # change by 5 variables (moving left)
    if scroll_right == True and scroll <= (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH : # right limit
        scroll += 5 * scroll_speed

    # add new tiles to screen
    # get mouse position
    position = pygame.mouse.get_pos()
    x = (position[0] + scroll) // TILE_SIZE # figure out what tile we are at on the grid
    y = position[1] // TILE_SIZE

    # check that coordinates are within tile area (not in the margins)
    if position[0] < SCREEN_WIDTH and position[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1: # left mouse button clicked
            # if the tile we are on is not the selected tile, make it the current tile
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        # if right mouse button is clicked, delete the tile
        if pygame.mouse.get_pressed()[2] == 1: # right mouse button clicked
            world_data[y][x] = -1 # empty tile

    # look for events that occur
    for event in pygame.event.get():

       # quit game
        if event.type == pygame.QUIT:
            run = False

        # check keyboard preses
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP: # increase level
                level += 1
            if event.key == pygame.K_DOWN and level > 0: # decrease level
                level -= 1
            if event.key == pygame.K_LEFT: # scroll left
                scroll_left = True
            if event.key == pygame.K_RIGHT: # scroll right
                scroll_right = True
            if event.key == pygame.K_RSHIFT: # scroll faster if shift is pressed
                scroll_speed = 5

        # keyboard release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()