#!/usr/bin/env python3

# empty = 0 (8), black pawn = 1 (9), red pawn = 2 (10), black king = 5 (13), red king = 6 (14)
# king-maker sqaure: +8 ; become a king: +4
# black moves down, red moves up
# U = up, D = down, L = left, R = right (when used as prefixes for search functions)

import math
import copy
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

# BASIC JUMP SEARCH FUNCTIONS:

def DL_jump_search(jumper_coordinate, previous_color):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    if previous_color is None:
        jumper_color = jumper_value & 3
    else:
        jumper_color = previous_color
    jumpee_coordinate = DL_search(jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate)
    if jumpee_value is not None:
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = DL_search(jumpee_coordinate)
            return (jumper_coordinate, jumpee_coordinate, destination_coordinate)
        
def DR_jump_search(jumper_coordinate, previous_color):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    if previous_color is None:
        jumper_color = jumper_value & 3
    else:
        jumper_color = previous_color        
    jumpee_coordinate = DR_search(jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate)
    if jumpee_value is not None:
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = DR_search(jumpee_coordinate)
            return (jumper_coordinate, jumpee_coordinate, destination_coordinate)
        
def UL_jump_search(jumper_coordinate, previous_color):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    if previous_color is None:
        jumper_color = jumper_value & 3
    else:
        jumper_color = previous_color
    jumpee_coordinate = UL_search(jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate)
    if jumpee_value is not None:
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = UL_search(jumpee_coordinate)
            return (jumper_coordinate, jumpee_coordinate, destination_coordinate)
        
def UR_jump_search(jumper_coordinate, previous_color):
    occupied_squares = locate_occupied_squares()
    jumper_value = get_square_value(jumper_coordinate)
    if previous_color is None:
        jumper_color = jumper_value & 3
    else:
        jumper_color = previous_color
    jumpee_coordinate = UR_search(jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate)
    if jumpee_value is not None:
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = UR_search(jumpee_coordinate)
            return (jumper_coordinate, jumpee_coordinate, destination_coordinate)

# JUMP MOVE INITIALIZATION FUNCTIONS:
        
class Path:
    def __init__(self, start_coordinate, end_coordinate):
        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate
        self.captures = []

    def record_capture(self, jumpee):
        if jumpee not in self.captures:
            self.captures.append(jumpee)
    
    def __str__(self):
        return f"{self.start_coordinate}x{self.end_coordinate} {self.captures}"

def create_Path_DL(jumper_coordinate, DL_jump_info, occupied_squares):
    DL_jumpee = DL_jump_info[1]
    DL_destination = DL_jump_info[2]
    if DL_destination is not None:
        if DL_destination not in occupied_squares:
            Path_DL = Path(jumper_coordinate, DL_destination)
            Path_DL.record_capture(DL_jumpee)
            return Path_DL

def create_Path_DR(jumper_coordinate, DR_jump_info, occupied_squares):
    DR_jumpee = DR_jump_info[1]
    DR_destination = DR_jump_info[2]
    if DR_destination is not None:
        if DR_destination not in occupied_squares:
            Path_DR = Path(jumper_coordinate, DR_destination)
            Path_DR.record_capture(DR_jumpee)
            return Path_DR

def create_Path_UL(jumper_coordinate, UL_jump_info, occupied_squares):
    UL_jumpee = UL_jump_info[1]
    UL_destination = UL_jump_info[2]
    if UL_destination is not None:
        if UL_destination not in occupied_squares:
            Path_UL = Path(jumper_coordinate, UL_destination)
            Path_UL.record_capture(UL_jumpee)
            return Path_UL

def create_Path_UR(jumper_coordinate, UR_jump_info, occupied_squares):
    UR_jumpee = UR_jump_info[1]
    UR_destination = UR_jump_info[2]
    if UR_destination is not None:
        if UR_destination not in occupied_squares:
            Path_UR = Path(jumper_coordinate, UR_destination)
            Path_UR.record_capture(UR_jumpee)
            return Path_UR

def create_initial_black_pawn_paths(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    initial_black_pawn_paths = []
    DL_jump_info = DL_jump_search(jumper_coordinate, None)
    DR_jump_info = DR_jump_search(jumper_coordinate, None)
    if DL_jump_info is not None:
        Path_DL = create_Path_DL(jumper_coordinate, DL_jump_info, occupied_squares)
        initial_black_pawn_paths.append(Path_DL)
    if DR_jump_info is not None:
        Path_DR = create_Path_DR(jumper_coordinate, DR_jump_info, occupied_squares)
        initial_black_pawn_paths.append(Path_DR)
    return initial_black_pawn_paths

def create_initial_red_pawn_paths(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    initial_red_pawn_paths = []
    UL_jump_info = UL_jump_search(jumper_coordinate, None)
    UR_jump_info = UR_jump_search(jumper_coordinate, None)
    if UL_jump_info is not None:
        Path_UL = create_Path_UL(jumper_coordinate, UL_jump_info, occupied_squares)
        initial_red_pawn_paths.append(Path_UL)
    if UR_jump_info is not None:
        Path_UR = create_Path_UR(jumper_coordinate, UR_jump_info, occupied_squares)
        initial_red_pawn_paths.append(Path_UR)
    return initial_red_pawn_paths

def create_initial_king_paths(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    initial_king_paths = []
    DL_jump_info = DL_jump_search(jumper_coordinate, None)
    DR_jump_info = DR_jump_search(jumper_coordinate, None)
    UL_jump_info = UL_jump_search(jumper_coordinate, None)
    UR_jump_info = UR_jump_search(jumper_coordinate, None)
    if DL_jump_info is not None:
        Path_DL = create_Path_DL(jumper_coordinate, DL_jump_info, occupied_squares)
        initial_king_paths.append(Path_DL)
    if DR_jump_info is not None:
        Path_DR = create_Path_DR(jumper_coordinate, DR_jump_info, occupied_squares)
        initial_king_paths.append(Path_DR)
    if UL_jump_info is not None:
        Path_UL = create_Path_UL(jumper_coordinate, UL_jump_info, occupied_squares)
        initial_king_paths.append(Path_UL)
    if UR_jump_info is not None:
        Path_UR = create_Path_UR(jumper_coordinate, UR_jump_info, occupied_squares)
        initial_king_paths.append(Path_UR)
    return initial_king_paths

# JUMP MOVE CALCULATION FUNCTIONS:

def create_black_pawn_path_calculation_info(path, piece_color):
    Path_A = copy.deepcopy(path)
    if Path_A is not None:
        Path_A_jump_info = DL_jump_search(Path_A.end_coordinate, piece_color)
    else:
        Path_A_jump_info = None
    Path_B = copy.deepcopy(path)
    if Path_B is not None:
        Path_B_jump_info = DR_jump_search(Path_B.end_coordinate, piece_color)
    else:
        Path_B_jump_info = None
    return (Path_A, Path_A_jump_info, Path_B, Path_B_jump_info)

def create_red_pawn_path_calculation_info(path, piece_color):
    Path_A = copy.deepcopy(path)
    if Path_A is not None:
        Path_A_jump_info = UL_jump_search(Path_A.end_coordinate, piece_color)
    else:
        Path_A_jump_info = None
    Path_B = copy.deepcopy(path)
    if Path_B is not None:
        Path_B_jump_info = UR_jump_search(Path_B.end_coordinate, piece_color)
    else:
        Path_B_jump_info = None
    return (Path_A, Path_A_jump_info, Path_B, Path_B_jump_info)

def create_king_path_calculation_info(path, piece_color):
    Path_A = copy.deepcopy(path)
    if Path_A is not None:
        Path_A_jump_info = DL_jump_search(Path_A.end_coordinate, piece_color)
    else:
        Path_A_jump_info = None
    Path_B = copy.deepcopy(path)
    if Path_B is not None:
        Path_B_jump_info = DR_jump_search(Path_B.end_coordinate, piece_color)
    else:
        Path_B_jump_info = None
    Path_C = copy.deepcopy(path)
    if Path_C is not None:
        Path_C_jump_info = UL_jump_search(Path_C.end_coordinate, piece_color)
    else:
        Path_C_jump_info = None
    Path_D = copy.deepcopy(path)
    if Path_D is not None:
        Path_D_jump_info = UR_jump_search(Path_D.end_coordinate, piece_color)
    else:
        Path_D_jump_info = None
    return (Path_A, Path_A_jump_info, Path_B, Path_B_jump_info, Path_C, Path_C_jump_info, Path_D, Path_D_jump_info)

def update_pawn_Path_A(path_calculation_info, occupied_squares):
    Path_A = path_calculation_info[0]
    Path_A_jump_info = path_calculation_info[1]
    Path_A_jumpee = Path_A_jump_info[1]
    Path_A_destination = Path_A_jump_info[2]
    if Path_A_destination is not None:
        if Path_A_destination not in occupied_squares:
            Path_A.record_capture(Path_A_jumpee)
            Path_A.end_coordinate = Path_A_destination
            return Path_A

def update_pawn_Path_B(path_calculation_info, occupied_squares):
    Path_B = path_calculation_info[2]
    Path_B_jump_info = path_calculation_info[3]
    Path_B_jumpee = Path_B_jump_info[1]
    Path_B_destination = Path_B_jump_info[2]
    if Path_B_destination is not None:
        if Path_B_destination not in occupied_squares:
            Path_B.record_capture(Path_B_jumpee)
            Path_B.end_coordinate = Path_B_destination
            return Path_B

def update_king_Path_A(path_calculation_info, occupied_squares):
    Path_A = path_calculation_info[0]
    Path_A_jump_info = path_calculation_info[1]
    Path_A_jumpee = Path_A_jump_info[1]
    Path_A_destination = Path_A_jump_info[2]
    previous_captures = Path_A.captures
    if Path_A_destination is not None and Path_A_jumpee not in previous_captures:
        if Path_A_destination not in occupied_squares or Path_A_destination == Path_A.start_coordinate:
            Path_A.record_capture(Path_A_jumpee)
            Path_A.end_coordinate = Path_A_destination
            return Path_A
            
def update_king_Path_B(path_calculation_info, occupied_squares):
    Path_B = path_calculation_info[2]
    Path_B_jump_info = path_calculation_info[3]
    Path_B_jumpee = Path_B_jump_info[1]
    Path_B_destination = Path_B_jump_info[2]
    previous_captures = Path_B.captures
    if Path_B_destination is not None and Path_B_jumpee not in previous_captures:
        if Path_B_destination not in occupied_squares or Path_B_destination == Path_B.start_coordinate:
            Path_B.record_capture(Path_B_jumpee)
            Path_B.end_coordinate = Path_B_destination
            return Path_B

def update_king_Path_C(path_calculation_info, occupied_squares):
    Path_C = path_calculation_info[4]
    Path_C_jump_info = path_calculation_info[5]
    Path_C_jumpee = Path_C_jump_info[1]
    Path_C_destination = Path_C_jump_info[2]
    previous_captures = Path_C.captures
    if Path_C_destination is not None and Path_C_jumpee not in previous_captures:
        if Path_C_destination not in occupied_squares or Path_C_destination == Path_C.start_coordinate:
            Path_C.record_capture(Path_C_jumpee)
            Path_C.end_coordinate = Path_C_destination
            return Path_C

def update_king_Path_D(path_calculation_info, occupied_squares):
    Path_D = path_calculation_info[6]
    Path_D_jump_info = path_calculation_info[7]
    Path_D_jumpee = Path_D_jump_info[1]
    Path_D_destination = Path_D_jump_info[2]
    previous_captures = Path_D.captures
    if Path_D_destination is not None and Path_D_jumpee not in previous_captures:
        if Path_D_destination not in occupied_squares or Path_D_destination == Path_D.start_coordinate:
            Path_D.record_capture(Path_D_jumpee)
            Path_D.end_coordinate = Path_D_destination
            return Path_D

def create_pawn_paths_to_process(path_calculation_info, occupied_squares):
    paths_to_process = []
    Path_A = path_calculation_info[0]
    Path_A_jump_info = path_calculation_info[1]
    Path_B = path_calculation_info[2]
    Path_B_jump_info = path_calculation_info[3]
    if Path_A_jump_info is not None:
        Path_A = update_pawn_Path_A(path_calculation_info, occupied_squares)
        if Path_A is not None:
            paths_to_process.append(Path_A)
    if Path_B_jump_info is not None:
        Path_B = update_pawn_Path_B(path_calculation_info, occupied_squares)
        if Path_B is not None:
            paths_to_process.append(Path_B)
    return paths_to_process

def create_king_paths_to_process(path_calculation_info, occupied_squares):
    paths_to_process = []
    Path_A = path_calculation_info[0]
    Path_A_jump_info = path_calculation_info[1]
    Path_B = path_calculation_info[2]
    Path_B_jump_info = path_calculation_info[3]
    Path_C = path_calculation_info[4]
    Path_C_jump_info = path_calculation_info[5]
    Path_D = path_calculation_info[6]
    Path_D_jump_info = path_calculation_info[7]
    if Path_A_jump_info is not None:
        Path_A = update_king_Path_A(path_calculation_info, occupied_squares)
        if Path_A is not None:
            paths_to_process.append(Path_A)
    if Path_B_jump_info is not None:
        Path_B = update_king_Path_B(path_calculation_info, occupied_squares)
        if Path_B is not None:
            paths_to_process.append(Path_B)
    if Path_C_jump_info is not None:
        Path_C = update_king_Path_C(path_calculation_info, occupied_squares)
        if Path_C is not None:
            paths_to_process.append(Path_C)
    if Path_D_jump_info is not None:
        Path_D = update_king_Path_D(path_calculation_info, occupied_squares)
        if Path_D is not None:
            paths_to_process.append(Path_D)
    return paths_to_process

def calculate_black_pawn_paths(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    piece_color = get_square_value(jumper_coordinate) & 3
    initial_black_pawn_paths = create_initial_black_pawn_paths(jumper_coordinate)
    processing = []
    finished_paths = []
    for path in initial_black_pawn_paths:
        processing.append(path)
    while len(processing) > 0:
        for path in processing:
            path_calculation_info = create_black_pawn_path_calculation_info(path, piece_color)
            paths_to_process = create_pawn_paths_to_process(path_calculation_info, occupied_squares)
            if len(paths_to_process) == 0:
                finished_paths.append(path)
            else:
                for updated_paths in paths_to_process:
                    processing.append(updated_paths)
            processing.remove(path)
    finished_black_pawn_paths = finished_paths
    return finished_black_pawn_paths

def calculate_red_pawn_paths(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    piece_color = get_square_value(jumper_coordinate) & 3
    initial_red_pawn_paths = create_initial_red_pawn_paths(jumper_coordinate)
    processing = []
    finished_paths = []
    for path in initial_red_pawn_paths:
        processing.append(path)
    while len(processing) > 0:
        for path in processing:
            path_calculation_info = create_red_pawn_path_calculation_info(path, piece_color)
            paths_to_process = create_pawn_paths_to_process(path_calculation_info, occupied_squares)
            if len(paths_to_process) == 0:
                finished_paths.append(path)
            else:
                for updated_paths in paths_to_process:
                    processing.append(updated_paths)
            processing.remove(path)
    finished_red_pawn_paths = finished_paths
    return finished_red_pawn_paths

def calculate_king_paths(jumper_coordinate):
    occupied_squares = locate_occupied_squares()
    piece_color = get_square_value(jumper_coordinate) & 3
    initial_king_paths = create_initial_king_paths(jumper_coordinate)
    processing = []
    finished_paths = []
    for path in initial_king_paths:
        processing.append(path)
    while len(processing) > 0:
        for path in processing:
            path_calculation_info = create_king_path_calculation_info(path, piece_color)
            paths_to_process = create_king_paths_to_process(path_calculation_info, occupied_squares)
            if len(paths_to_process) == 0:
                finished_paths.append(path)
            else:
                for updated_paths in paths_to_process:
                    processing.append(updated_paths)
            processing.remove(path)
    finished_king_paths = finished_paths
    return finished_king_paths

# JUMP MOVE LIST FUNCTIONS:

def list_all_black_jump_moves():
    black_jump_moves = []
    black_pawns = locate_black_pawns()
    black_kings = locate_black_kings()
    for pawn in black_pawns:
        jumper_coordinate = pawn
        paths = calculate_black_pawn_paths(jumper_coordinate)
        for path in paths:
            if path is not None:
                black_jump_moves.append(path)
    for king in black_kings:
        jumper_coordinate = king
        paths = calculate_king_paths(jumper_coordinate)
        for path in paths:
            if path is not None:
                black_jump_moves.append(path)
    return black_jump_moves

def list_all_red_jump_moves():
    red_jump_moves = []
    red_pawns = locate_red_pawns()
    red_kings = locate_red_kings()
    for pawn in red_pawns:
        jumper_coordinate = pawn
        paths = calculate_red_pawn_paths(jumper_coordinate)
        for path in paths:
            if path is not None:
                red_jump_moves.append(path)
    for king in red_kings:
        jumper_coordinate = king
        paths = calculate_king_paths(jumper_coordinate)
        for path in paths:
            if path is not None:
                red_jump_moves.append(path)
    return red_jump_moves

# LIST ALL POSSIBLE MOVES FUNCTIONS:

def list_all_possible_black_moves():
    all_possible_black_moves = []
    black_jump_moves = list_all_black_jump_moves()
    black_simples = find_black_simples()
    if len(black_jump_moves) > 0:
        for jump_move in black_jump_moves:
            all_possible_black_moves.append(jump_move)
    else:
        for simple in black_simples:
            all_possible_black_moves.append(simple)
    return all_possible_black_moves

def list_all_possible_red_moves():
    all_possible_red_moves = []
    red_jump_moves = list_all_red_jump_moves()
    red_simples = find_red_simples()
    if len(red_jump_moves) > 0:
        for jump_move in red_jump_moves:
            all_possible_red_moves.append(jump_move)
    else:
        for simple in red_simples:
            all_possible_red_moves.append(simple)
    return all_possible_red_moves

# USER INTERFACE CODE:

# o = black pawn, O = black king, x = red pawn, X = red king, " " = empty square, "=" = non-coordinate square

# empty board:

# row 1 = "|=| |=| |=| |=| |"
# row 2 = "| |=| |=| |=| |=|"
# row 3 = "|=| |=| |=| |=| |"
# row 4 = "| |=| |=| |=| |=|"
# row 5 = "|=| |=| |=| |=| |"
# row 6 = "| |=| |=| |=| |=|"
# row 7 = "|=| |=| |=| |=| |"
# row 8 = "| |=| |=| |=| |=|"

# starting position:

# row 1 = "|=|o|=|o|=|o|=|o|"
# row 2 = "|o|=|o|=|o|=|o|=|"
# row 3 = "|=|o|=|o|=|o|=|o|"
# row 4 = "| |=| |=| |=| |=|"
# row 5 = "|=| |=| |=| |=| |"
# row 6 = "|x|=|x|=|x|=|x|=|"
# row 7 = "|=|x|=|x|=|x|=|x|"
# row 8 = "|x|=|x|=|x|=|x|=|"

def translate_position(position):
    translated_position = []
    for value in position:
        match value:
            case 0:
                translated_position.append(" ")
            case 8:
                translated_position.append(" ")
            case 1:
                translated_position.append("o")
            case 5:
                translated_position.append("O")
            case 2:
                translated_position.append("x")
            case 6:
                translated_position.append("X")
            case 9:
                translated_position.append("o")
            case 13:
                translated_position.append("O")
            case 10:
                translated_position.append("x")
            case 14:
                translated_position.append("X")
    return translated_position

def create_board_rows(T_board_position):
    row_1 = f"|=|{T_board_position[0]}|=|{T_board_position[1]}|=|{T_board_position[2]}|=|{T_board_position[3]}|"
    row_2 = f"|{T_board_position[4]}|=|{T_board_position[5]}|=|{T_board_position[6]}|=|{T_board_position[7]}|=|"
    row_3 = f"|=|{T_board_position[8]}|=|{T_board_position[9]}|=|{T_board_position[10]}|=|{T_board_position[11]}|"
    row_4 = f"|{T_board_position[12]}|=|{T_board_position[13]}|=|{T_board_position[14]}|=|{T_board_position[15]}|=|"
    row_5 = f"|=|{T_board_position[16]}|=|{T_board_position[17]}|=|{T_board_position[18]}|=|{T_board_position[19]}|"
    row_6 = f"|{T_board_position[20]}|=|{T_board_position[21]}|=|{T_board_position[22]}|=|{T_board_position[23]}|=|"
    row_7 = f"|=|{T_board_position[24]}|=|{T_board_position[25]}|=|{T_board_position[26]}|=|{T_board_position[27]}|"
    row_8 = f"|{T_board_position[28]}|=|{T_board_position[29]}|=|{T_board_position[30]}|=|{T_board_position[31]}|=|"
    rows = [row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8]
    return rows

def print_current_position(board_position):
    T_board_position = translate_position(board_position)
    rows = create_board_rows(T_board_position)
    for row in rows:
        print(row)

def select_black_move():
    moves = list_all_possible_black_moves()
    count = 1
    total_moves = []
    print("\nMoves for black:\n")
    for move in moves:
        move_string = f"{count}: {move}"
        print(move_string)
        total_moves.append(count)
        count += 1
    while True:
        move_selection_number_string = input("\nSelect a move by entering the move number and pressing 'Enter': ")
        if not move_selection_number_string.isnumeric():
            print("\nInvalid move. Please try again.")
            continue
        else:
            move_selection_number_integer = int(move_selection_number_string)
            if move_selection_number_integer not in total_moves:
                print("\nInvalid move. Please try again.")
                continue
            else:
                break
    selected_move = moves[move_selection_number_integer - 1]
    return selected_move

def select_red_move():
    moves = list_all_possible_red_moves()
    count = 1
    total_moves = []
    print("\nMoves for red:\n")
    for move in moves:
        move_string = f"{count}: {move}"
        print(move_string)
        total_moves.append(count)
        count += 1
    while True:
        move_selection_number_string = input("\nSelect a move by entering the move number and pressing 'Enter': ")
        if not move_selection_number_string.isnumeric():
            print("\nInvalid move. Please try again.")
            continue
        else:
            move_selection_number_integer = int(move_selection_number_string)
            if move_selection_number_integer not in total_moves:
                print("\nInvalid move. Please try again.")
                continue
            else:
                break
    selected_move = moves[move_selection_number_integer - 1]
    return selected_move

def update_start_and_end_coordinates(start_coordinate, end_coordinate):
    piece_value = get_square_value(start_coordinate)
    destination_value = get_square_value(end_coordinate)
    if piece_value & 8:
        board_position[start_coordinate - 1] = 8
    else:
        board_position[start_coordinate - 1] = 0
    if destination_value == 8:
        if piece_value & 4:
            board_position[end_coordinate - 1] = piece_value
        else:
            board_position[end_coordinate - 1] = piece_value + 12
    else:
        board_position[end_coordinate - 1] = piece_value

def update_board_position_for_simple_move(selected_move):
    move_coordinates = re.split("[-]", selected_move)
    start_coordinate = int(move_coordinates[0])
    end_coordinate = int(move_coordinates[1])
    update_start_and_end_coordinates(start_coordinate, end_coordinate)
    print(f"\nYou have played the simple move {selected_move}\n")

def update_board_position_for_jump_move(selected_move):
    start_coordinate = selected_move.start_coordinate
    end_coordinate = selected_move.end_coordinate
    captures = selected_move.captures
    update_start_and_end_coordinates(start_coordinate, end_coordinate)
    for capture in captures:
        board_position[capture - 1] = 0
    print(f"You have played the jump move {selected_move}\n")

def play_selected_move(selected_move):
    if type(selected_move) is str:
        update_board_position_for_simple_move(selected_move)
    elif type(selected_move) is Path:
        update_board_position_for_jump_move(selected_move)

# PLAYABILITY:

generate_starting_position()

while True:
    print("Turn: black\n")
    print_current_position(board_position)
    black_move = select_black_move()
    play_selected_move(black_move)
    print("Turn: red\n")
    print_current_position(board_position)
    red_move = select_red_move()
    play_selected_move(red_move)