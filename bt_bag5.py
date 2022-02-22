import itertools as it
import sys
import keyboard
import numpy as np
import math
from PIL import ImageGrab
from utils import *


image = ImageGrab.grab(bbox=(2524, 78, 3263, 883), all_screens=True)

board = np.zeros((20, 10), int) - 1
next_pieces = np.zeros((5,), int) - 1
held_piece = -1
now_piece = -1


def index2name(item):
    return index2piece[item] if isinstance(item, int) else np.vectorize(index2piece.get)(item)


def get_min_dist():
    min_dist = sys.maxsize
    for i, j in it.product(color2index, color2index):
        d = get_color_dist(i, j)
        if d != 0 and d < min_dist:
            min_dist = d
    return min_dist


def get_piece_from_pixel(rgb):
    for idx, color in enumerate(color2index):
        if is_similar_color(color, rgb):
            return idx
    return -1


def get_piece_from_region(left, top, right, bottom, x_step=1, y_step=1):
    # Precondition: there is only one piece in such a region
    if image:
        for y, x in it.product(
                [i for i in range(top, bottom + 1, y_step)],
                [i for i in range(left, right + 1, x_step)]
        ):
            index = get_piece_from_pixel(image.getpixel((x, y)))
            if index != -1:
                return index
    return -1


def get_shape_from_region(left, top, right, bottom, x_step=1, y_step=1):
    if image:
        arr = np.zeros((math.ceil((bottom + 1 - top) / y_step), math.ceil((right + 1 - left) / x_step)), int)
        for y, x in it.product(
                [i for i in range(top, bottom + 1, y_step)],
                [i for i in range(left, right + 1, x_step)]
        ):
            if not is_similar_color((0, 0, 0), image.getpixel((x, y))):
                arr[(y - top) // y_step][(x - left) // x_step] = 1
        for idx, shape in enumerate(shape2index):
            for num_rot in range(4):
                if does_contain_subset(arr, np.rot90(shape, num_rot)):
                    # print(shape)
                    return idx
    return -1


def update_board():
    for y, x in it.product([i for i in range(20)], [i for i in range(10)]):
        new_y = 122 + y * 35
        new_x = 199 + x * 35
        pixel_color = image.getpixel((new_x, new_y))
        board[y][x] = get_piece_from_pixel(pixel_color)


def update_pieces():
    global next_pieces
    global held_piece
    global now_piece
    # Update next_pieces
    for y in range(5):
        next_pieces[y] = get_piece_from_region(643, 183 + 105 * y, 651, 191 + 105 * y)
    # Update held_piece
    held_piece = get_piece_from_region(86, 184, 94, 192)
    # Update now_piece TODO
    now_piece = get_shape_from_region(198, 16, 529, 138, 35, 35)


def update():
    global image
    image = ImageGrab.grab(bbox=(2524, 78, 3263, 883), all_screens=True)
    update_board()
    update_pieces()


def get_board_index():
    new_board = np.where(board >= 0, 1, 0)[-6:, :]
    return binary_search(starting_board_dict, new_board, compare_array, len(starting_board_dict) - 1, 0)
    # for idx, arr in enumerate(starting_board_dict):
    #     if np.array_equal(arr, new_board):
    #         return idx
    # return -1


def save_image(path):
    ImageGrab.grab(bbox=(2524, 78, 3263, 883), all_screens=True).save(path)


if __name__ == '__main__':
    n = 0
    while True:
        keyboard.wait('enter')

        print('\n' * 100)

        update()
        print(index2name(board))
        print('Next:   ', index2name(next_pieces))
        print('Held:   ', index2name(held_piece))
        print('Up:     ', index2name(now_piece))

        idx = get_board_index()
        print(starting_board_dict[idx] if idx != -1 else -1)
        print('Board:  ', idx)

        # save_image('./top_' + str(n) + '.png')
        # n += 1

        # rgb2xyz((100, 0, 0))
