#!/usr/bin/env python3

# empty = 0 (8), black pawn = 1 (9), red pawn = 2 (10), black king = 5 (13), red king = 6 (14)
# king-maker sqaure: +8 ; become a king: +4
# black moves down, red moves up
# U = up, D = down, L = left, R = right (when used as prefixes for search functions)

import math
import re

# BOARD GENERATION FUNCTIONS:

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

def generate_empty_board():
    for i in range(1, 5):
        board_position.append(8)
    for i in range(5, 29):
        board_position.append(0)
    for i in range(29, 33):
        board_position.append(8)

# IMMEDIATE VISION SEARCH FUNCTIONS:

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

# SQUARE LOCATION & IDENTIFICATION FUNCTIONS

def get_square_value(coordinate):
    if coordinate is not None:
        n = coordinate
        value = board_position[n-1]
    else:
        value = None
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

def locate_black_pawns():
    black_pawns = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 1) and not (value & 4):
           black_pawns.append(coordinate)
    return black_pawns

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

def locate_red_pawns():
    red_pawns = []
    for i in range(1, 33):
       coordinate = i
       value = get_square_value(coordinate)
       if (value & 2) and not (value & 4):
           red_pawns.append(coordinate)
    return red_pawns

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

# SIMPLE MOVE SEARCH FUNCTIONS:

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

# JUMP SEARCH FUNCTIONS:

def DL_jump_search(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    if jumper_value is not None:
        jumper_color = jumper_value & 3
        jumpee_coordinate = DL_search(jumper_coordinate)
        jumpee_value = get_square_value(jumpee_coordinate)
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = DL_search(jumpee_coordinate)
            if destination_coordinate not in occupied_squares:
                return (jumper_coordinate, jumpee_coordinate, destination_coordinate)
        
def DR_jump_search(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    if jumper_value is not None:
        jumper_color = jumper_value & 3        
        jumpee_coordinate = DR_search(jumper_coordinate)
        jumpee_value = get_square_value(jumpee_coordinate)
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = DR_search(jumpee_coordinate)
            if destination_coordinate not in occupied_squares:
                return (jumper_coordinate, jumpee_coordinate, destination_coordinate)
        
def UL_jump_search(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    jumper_color = jumper_value & 3
    jumpee_coordinate = UL_search(jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate)
    jumpee_color = jumpee_value & 3
    if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
        destination_coordinate = UL_search(jumpee_coordinate)
        if destination_coordinate not in occupied_squares:
            return (jumper_coordinate, jumpee_coordinate, destination_coordinate)
        
def UR_jump_search(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    jumper_color = jumper_value & 3
    jumpee_coordinate = UR_search(jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate)
    jumpee_color = jumpee_value & 3
    if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
        destination_coordinate = UR_search(jumpee_coordinate)
        if destination_coordinate not in occupied_squares:
            return (jumper_coordinate, jumpee_coordinate, destination_coordinate)



class PawnPath:
    def __init__(self, start_coordinate, end_coordinate):
        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate
        self.captures = []
    
    def record_capture(self, jumpee):
        self.captures.append(jumpee)
    
    def __str__(self):
        return f"{self.start_coordinate}x{self.end_coordinate} {self.captures}"



def find_single_black_pawn_jump_moves(jumper_coordinate):
    DL_jump_info = DL_jump_search(jumper_coordinate)
    DR_jump_info = DR_jump_search(jumper_coordinate)
    input = []
    if DL_jump_info is not None:
        Path_A = PawnPath(DL_jump_info[0], DL_jump_info[2])
        Path_A.captures.append(DL_jump_info[1])
        input.append(Path_A)
    if DR_jump_info is not None:
        Path_B = PawnPath(DR_jump_info[0], DR_jump_info[2])
        Path_B.captures.append(DR_jump_info[1]) 
        input.append(Path_B)
    output = []
    while True:
        for path in input:
            New_Path_1 = path
            if DL_jump_search(path.end_coordinate) is not None:
                New_Path_1.captures.append(DL_jump_search(path.end_coordinate)[1])
                New_Path_1.end_coordinate = DL_jump_search(path.end_coordinate)[2]
                output.append(New_Path_1)
            New_Path_2 = path
            if DR_jump_search(path.end_coordinate) is not None:
                New_Path_2.captures.append(DR_jump_search(path.end_coordinate)[1])
                New_Path_2.end_coordinate = DR_jump_search(path.end_coordinate)[2]
                output.append(New_Path_2)
        if len(output) == 0:
            break    
        input.clear()
        for path in output:
            input.append(path)
        output.clear()
    single_black_pawn_jump_moves = input
    return single_black_pawn_jump_moves
        




generate_starting_position()
board_position[13] = 2
board_position[26] = 0

x = find_single_black_pawn_jump_moves(9)

for jump_move in x:
    print(jump_move)













def find_black_pawn_jump_candidates():
    black_pawn_jump_candidates = []
    black_pawns = locate_black_pawns()
    for pawn in black_pawns:
        DL_jump = DL_jump_search(pawn)
        DR_jump = DR_jump_search(pawn)
        if DL_jump is not None or DR_jump is not None:
            black_pawn_jump_candidates.append(pawn)
    return black_pawn_jump_candidates
        
def find_black_king_jump_candidates():
    black_king_jump_candidates = []
    black_kings = locate_black_kings()
    for king in black_kings:
        DL_jump = DL_jump_search(king)
        DR_jump = DR_jump_search(king)
        UL_jump = UL_jump_search(king)
        UR_jump = UR_jump_search(king)
        if DL_jump is not None or DR_jump is not None or UL_jump is not None or UR_jump is not None:
            black_king_jump_candidates.append(king)
    return black_king_jump_candidates

def find_black_piece_jump_candidates():
    black_piece_jump_candidates = []
    black_pawn_jump_candidates = find_black_pawn_jump_candidates()
    for pawn in black_pawn_jump_candidates:
        black_piece_jump_candidates.append(pawn)
    black_king_jump_candidates = find_black_king_jump_candidates()
    for king in black_king_jump_candidates:
        black_piece_jump_candidates.append(king)
    return black_piece_jump_candidates

def find_red_pawn_jump_candidates():
    red_pawn_jump_candidates = []
    red_pawns = locate_red_pawns()
    for pawn in red_pawns:
        UL_jump = UL_jump_search(pawn)
        UR_jump = UR_jump_search(pawn)
        if UL_jump is not None or UR_jump is not None:
            red_pawn_jump_candidates.append(pawn)
    return red_pawn_jump_candidates
        
def find_red_king_jump_candidates():
    red_king_jump_candidates = []
    red_kings = locate_red_kings()
    for king in red_kings:
        DL_jump = DL_jump_search(king)
        DR_jump = DR_jump_search(king)
        UL_jump = UL_jump_search(king)
        UR_jump = UR_jump_search(king)
        if DL_jump is not None or DR_jump is not None or UL_jump is not None or UR_jump is not None:
            red_king_jump_candidates.append(king)
    return red_king_jump_candidates

def find_red_piece_jump_candidates():
    red_piece_jump_candidates = []
    red_pawn_jump_candidates = find_red_pawn_jump_candidates()
    for pawn in red_pawn_jump_candidates:
        red_piece_jump_candidates.append(pawn)
    red_king_jump_candidates = find_red_king_jump_candidates()
    for king in red_king_jump_candidates:
        red_piece_jump_candidates.append(king)
    return red_piece_jump_candidates












def list_all_black_pawn_jump_moves():
    black_pawn_jump_candidates = find_black_pawn_jump_candidates()
    black_pawn_jump_moves = []
    for pawn in black_pawn_jump_candidates:
        single_black_pawn_jump_moves = find_single_black_pawn_jump_moves(pawn)
        black_pawn_jump_moves.append(single_black_pawn_jump_moves)
    return black_pawn_jump_moves
















