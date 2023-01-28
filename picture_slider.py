import numpy as np
import pygame
from pygame.locals import *
import sys
import picture_utils as utils

class Picture_Piece(pygame.sprite.Sprite):
    
    def __init__(self, x, y, position, sides):
        super().__init__()
        self.image = pygame.image.load(f'tmp_{position}.png')
        self.rect = self.image.get_rect(center = (x,y))
        self.width = self.rect.width
        self.length = self.rect.height
        self.position = position
        self.sides = sides
        self.true_position = position

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y)) 

    def check_blank(self, direction, sides):
        
        if (self.position - self.sides == blank_position) and (direction == 'up'):
            return True
        
        
        elif (self.position + self.sides == blank_position) and (direction == 'down'):
            return True

        elif (self.position + 1 == blank_position) and (direction == 'right') and (self.position % sides != 0):
            return True
        
        elif (self.position - 1 == blank_position) and (direction == 'left') and (self.position % sides != 1):
            return True        

        else:
            return False

    
    def move_picture(self, direction):
        
        if direction == 'up':
            new_pos = (self.rect.centerx, self.rect.centery - self.length)
            self.position = self.position - self.sides
        elif direction == 'down':
            new_pos = (self.rect.centerx, self.rect.centery + self.length)
            self.position = self.position + self.sides
        elif direction == 'right':
            new_pos = (self.rect.centerx + self.width, self.rect.centery)
            self.position = self.position + 1
        elif direction == 'left':
            new_pos = (self.rect.centerx - self.width, self.rect.centery)  
            self.position = self.position - 1 
        self.rect.center = new_pos     


    def correct_place(self):
        return self.position == self.true_position


def load_pieces(num):

    """Prepare the pieces as picture_piece objects in a list"""
    num = num - 1
    # Get the correct dimensions
    true_num = int(np.sqrt(num + 1))
    WIDTH = int(1280 / true_num)
    LENGTH = int(800 / true_num)
    jj = 0
    
    piece_list = []
    for ii in range(num):
        ij = ii % true_num
        tmp_piece = Picture_Piece(int(WIDTH / 2) + ij*WIDTH, int(LENGTH / 2) + jj*LENGTH ,ii+1, true_num)
        piece_list.append(tmp_piece)

        if (ii+1)%true_num == 0:
            jj += 1

    return piece_list

def check_pieces(piece_list, direction, sides):
    """Runs through a list of pieces and returns the index of the one that can be moved. If none, returns special value"""

    truth_list = [piece.check_blank(direction, sides) for piece in piece_list]

    try:
        ind = truth_list.index(True)
    except:
        ind = 'n'

    return ind

def computer_player(piece_list, sides, blank_position):

    """The computer plays the game to randomize the starting pieces in a configuration that can be solved"""


    # Select a move
    attempted_move = ['up', 'down', 'left', 'right'][np.random.randint(4)]

    if attempted_move == 'up':
        moving = check_pieces(piece_list, 'up', sides)

        if moving != 'n':
            piece_list[moving].move_picture('up')
            blank_position += sides


    elif attempted_move == 'down':
        moving = check_pieces(piece_list, 'down', sides)

        if moving != 'n':
            piece_list[moving].move_picture('down')
            blank_position -= sides


    elif attempted_move == 'right':
        moving = check_pieces(piece_list, 'right', sides)

        if moving != 'n':
            piece_list[moving].move_picture('right')
            blank_position -= 1


    elif attempted_move == 'left':
        moving = check_pieces(piece_list, 'left', sides)

        if moving != 'n':
            piece_list[moving].move_picture('left')
            blank_position += 1

    return piece_list, blank_position
    

# Global varibales
HEIGHT = 800
WIDTH = 1280
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
blank_position = 16
sides = 4
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
tick = 0

# Start up pygame
pygame.init()


# Run all the functions
picture = utils.select_picture('test_photos/', optional_name='test_photo_1.jpg')
piece_list = utils.picture_slice(picture, sides = 4)
piece_list = utils.create_borders(piece_list)
utils.save_array(piece_list)
piece_list = load_pieces(16)


while True:

    displaysurface.fill([255,255,255])

    
    for piece in piece_list:
        piece.render()


    if tick < 100:
        piece_list, blank_position = computer_player(piece_list, 4, blank_position)
        tick += 1

    pygame.display.update()
    FPS_CLOCK.tick(FPS)


    if tick == 100:
        correct_positions = [piece.correct_place() for piece in piece_list]
        if False not in correct_positions:
            print('Correct!')
            final_piece = Picture_Piece(int(WIDTH / (2*sides)) + (sides - 1)*int(WIDTH/sides), int(HEIGHT / (2*sides)) + (sides - 1)*int(HEIGHT/sides) ,16, sides)
            piece_list.append(final_piece)
            tick += 1
            blank_position = 100

    for event in pygame.event.get():

        # Exit event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        # Key press events
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                moving = check_pieces(piece_list, 'up', sides)

                if moving != 'n':
                    piece_list[moving].move_picture('up')
                    blank_position += sides


            if event.key == pygame.K_DOWN:
                moving = check_pieces(piece_list, 'down', sides)

                if moving != 'n':
                    piece_list[moving].move_picture('down')
                    blank_position -= sides


            if event.key == pygame.K_RIGHT:
                moving = check_pieces(piece_list, 'right', sides)

                if moving != 'n':
                    piece_list[moving].move_picture('right')
                    blank_position -= 1


            if event.key == pygame.K_LEFT:
                moving = check_pieces(piece_list, 'left', sides)

                if moving != 'n':
                    piece_list[moving].move_picture('left')
                    blank_position += 1



            if event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()



