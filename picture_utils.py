import numpy as np
import os
from PIL import Image
from pygame.locals import *
import random


def select_picture(path,
                   random_choice = False, 
                   optional_name = None):

    """Selects a picture either randomly or with a given name"""

    if random_choice:
        valid_ending = ['png', 'jpeg', 'jpg']
        pics = [fname for fname in os.listdir(path) if fname.split('.')[-1] in valid_ending]
        pic_file = path + '/' + pics[np.random.randint(len(pics))]
        pic = Image.open(pic_file)
        pic = pic.resize((1280, 800))
        return np.array(pic)

    else:
        try:
            pic_file = path + '/' + optional_name
            pic = Image.open(pic_file)
            pic = pic.resize((1280, 800))
            return np.array(pic)
        except:
            print('No File Given or Found')
            return None


def picture_slice(picture_array, 
                  sides = 2):

    """Cuts the array picture_array into pieces with sides many pieces on each side. More functionality to be added once basic case is tested"""

    WIDTH = int(picture_array.shape[1] / sides)
    LENGTH = int(picture_array.shape[0] / sides)

    piece_list = []
    for ii in range(sides):
        for jj in range(sides):
            piece_array = picture_array[ii*LENGTH: (ii+1)*LENGTH, jj*WIDTH: (jj+1)*WIDTH, :]
            piece_list.append(piece_array)

    return piece_list


def create_borders(piece_list, thickness = 1):

    """Adds borders to the cut up pieces so it's easier to tell what they are. Functionality to add thickness to be added later"""
    new_pieces = []
    for piece in piece_list:
        piece_length, piece_width, _ = piece.shape
        piece_length -= 1
        piece_width -= 1

        piece[ :, 0, :] = 0
        piece[ :, piece_width, :] = 0
        piece[ 0, :, :] = 0
        piece[ piece_length, :, :] = 0
        
        new_pieces.append(piece)

    return new_pieces

def reconstruct_photo(piece_list):

    """Takes a list of pieces and reconstructs them into a complete photo. This includes shuffle and dropping"""

    LENGTH, WIDTH, _ = piece_list[0].shape
    ii = 0
    jj = 0

    # Drop the last piece and shuffle
    del(piece_list[-1])
    random.shuffle(piece_list)

    final_array = np.zeros((800, 1280, 3))
    for piece in piece_list:
        final_array[ii*LENGTH: (ii+1)*LENGTH, jj*WIDTH: (jj+1)*WIDTH, :] = piece

        if (jj+1)*WIDTH == 1280:
            jj = 0
            ii += 1
        else:
            jj += 1

    return final_array


def save_array(picture_list):

    count = 1
    for pic in picture_list:
        Image.fromarray(pic).save(f'tmp_{count}.png')
        count += 1