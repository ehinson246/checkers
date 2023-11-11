#!/usr/bin/env python3

# empty = 0 (8), black man = 1 (9), red man = 2 (10), black king = 5 (13), red king = 6 (14)
# king-maker sqaure: +8 ; become a king: +4
# black moves down, red moves up
# U = up, D = down, L = left, R = right (when used as prefixes for search functions)

import math

board_position = []

def generate_starting_position():
    for i in range(1, 5):
        board_position.append(9)
    for i in range(5, 13):
        board_position.append(1)
    for i in range(13, 21):
        board_position.append(0)
    for i in range(21, 29):
        board_position.append(2)
    for i in range(29, 33):
        board_position.append(10)

def DL_search(coordinate):
    n = coordinate
    row = math.ceil(n/4)
    if n % 8 == 1 or n % 8 == 2 or n % 8 == 3 or n % 8 == 4:
        new_coordinate = n + 4
    elif n % 8 != 5 and row != 8:
        new_coordinate = n + 3
    else:
        new_coordinate = None
    return new_coordinate

def DR_search(coordinate):
    n = coordinate
    row = math.ceil(n/4)
    if n % 8 == 1 or n % 8 == 2 or n % 8 == 3:
        new_coordinate = n + 5
    elif n % 8 != 4 and row != 8:
        new_coordinate = n + 4
    else:
        new_coordinate = None
    return new_coordinate

def UL_search(coordinate):
    n = coordinate
    row = math.ceil(n/4)
    if n % 8 == 6 or n % 8 == 7 or n % 8 == 0:
        new_coordinate = n - 5
    elif n % 8 != 5 and row != 1:
        new_coordinate = n - 4
    else:
        new_coordinate = None
    return new_coordinate

def UR_search(coordinate):
    n = coordinate
    row = math.ceil(n/4)
    if n % 8 == 5 or n % 8 == 6 or n % 8 == 7 or n % 8 == 0:
        new_coordinate = n - 4
    elif n % 8 != 4 and row != 1:
        new_coordinate = n - 3
    else:
        new_coordinate = None
    return new_coordinate

def get_square_value(coordinate):
    n = coordinate
    value = board_position[n-1]
    return value

def locate_black_pieces():
    black_pieces = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if value & 1:
           black_pieces.append(coordinate)
    return black_pieces

def locate_black_kings():
    black_kings = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 1) and (value & 4):
           black_kings.append(coordinate)
    return black_kings

def locate_black_men():
    black_men = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 1) and not (value & 4):
           black_men.append(coordinate)
    return black_men

def locate_red_pieces():
    red_pieces = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if value & 2:
           red_pieces.append(coordinate)
    return red_pieces

def locate_red_kings():
    red_kings = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 2) and (value & 4):
           red_kings.append(coordinate)
    return red_kings

def locate_red_men():
    red_men = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 2) and not (value & 4):
           red_men.append(coordinate)
    return red_men

def locate_occupied_squares():
    occupied_squares = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 3) | 0:
           occupied_squares.append(coordinate)
    return occupied_squares

def locate_kingmaker_squares():
    kingmaker_squares = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 8):
           kingmaker_squares.append(coordinate)
    return kingmaker_squares

def D_simple_search(coordinate):
    simples = []
    DL_coordinate = DL_search(coordinate)
    DR_coordinate = DR_search(coordinate)
    occupied_squares = locate_occupied_squares()
    if DL_coordinate not in occupied_squares and DL_coordinate is not None:
        simple = str(coordinate) + '-' + str(DL_coordinate)
        simples.append(simple)
    if DR_coordinate not in occupied_squares and DR_coordinate is not None:
        simple = str(coordinate) + '-' + str(DR_coordinate)
        simples.append(simple)
    return simples

def U_simple_search(coordinate):
    simples = []
    UL_coordinate = UL_search(coordinate)
    UR_coordinate = UR_search(coordinate)
    occupied_squares = locate_occupied_squares()
    if UL_coordinate not in occupied_squares and UL_coordinate is not None:
        simple = str(coordinate) + '-' + str(UL_coordinate)
        simples.append(simple)
    if UR_coordinate not in occupied_squares and UR_coordinate is not None:
        simple = str(coordinate) + '-' + str(UR_coordinate)
        simples.append(simple)
    return simples

def find_black_simples():
    black_pieces = locate_black_pieces()
    black_kings = locate_black_kings()
    black_simples = []
    for coordinate in black_pieces:
        D_simples = D_simple_search(coordinate)
        for simple in D_simples:
            black_simples.append(simple)
        if coordinate in black_kings:
            U_simples = U_simple_search(coordinate)
            for simple in U_simples:
                black_simples.append(simple)   
    return black_simples

def find_red_simples():
    red_pieces = locate_red_pieces()
    red_kings = locate_red_kings()
    red_simples = []
    for coordinate in red_pieces:
        U_simples = U_simple_search(coordinate)
        for simple in U_simples:
            red_simples.append(simple)
        if coordinate in red_kings:
            D_simples = D_simple_search(coordinate)
            for simple in D_simples:
                red_simples.append(simple)
    return red_simples













def find_jump_availability(coordinate_list):
    jump_availability = []
    return jump_availability

def find_jumps(jump_availability):
    jumps = []
    return jumps

# def find_moves(coordinate_list):
#     jumpstarts = find_jump_availability()
#     if jumpstarts is None:
#         moves = find_simples()
#         return moves
#     else:
#         moves = find_jumps()
#         return moves