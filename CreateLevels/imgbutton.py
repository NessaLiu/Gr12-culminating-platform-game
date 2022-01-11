import pygame
pygame.init()

class ImageButton():
    '''This button class is used to create instances of buttons that can be clicked.'''

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        # scale image
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # create rectangle and its position for the image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False # track button click status

    def draw_button(self, surface):
        '''This function draws a button on the screen for the given image.'''

        # no action to start
        action = False

        # get mouse position
        position = pygame.mouse.get_pos()

        # check mouse position and clicks
        if self.rect.collidepoint(position): # mouse is hovering over button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # left mouse button clicked
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0 :  # the button is not clicked
            self.clicked = False

        # draw button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action