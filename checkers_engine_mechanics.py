#!/usr/bin/env python3

# black moves down, red moves up
# U = up, D = down, L = left, R = right (when used as prefixes for search functions)

import math
import copy
import re

# PIECE VALUE CONSTANTS:

EMPTY_SQUARE = 0

BLACK_PIECE = 1
RED_PIECE = 2

IS_OCCUPIED = 3

IS_KING = 4

BLACK_KING = BLACK_PIECE + IS_KING
RED_KING = RED_PIECE + IS_KING

ON_BACK_RANK = 8

# BOARD GENERATION FUNCTIONS:

def generate_starting_position():
    board_position = []
    for coordinate in range(1, 5):
        board_position.append(BLACK_PIECE + ON_BACK_RANK)
    for coordinate in range(5, 13):
        board_position.append(BLACK_PIECE)
    for coordinate in range(13, 21):
        board_position.append(EMPTY_SQUARE)
    for coordinate in range(21, 29):
        board_position.append(RED_PIECE)
    for coordinate in range(29, 33):
        board_position.append(RED_PIECE + ON_BACK_RANK)
    return board_position

def generate_empty_board():
    board_position = []
    for coordinate in range(1, 5):
        board_position.append(ON_BACK_RANK + EMPTY_SQUARE)
    for coordinate in range(5, 29):
        board_position.append(EMPTY_SQUARE)
    for coordinate in range(29, 33):
        board_position.append(ON_BACK_RANK + EMPTY_SQUARE)
    return board_position

# BOARD OBJECT LOCATION FUNCTIONS:

def get_square_value(coordinate, board_position):
    if coordinate is not None:
        square_value = board_position[coordinate - 1]
    else:
        square_value = None
    return square_value

def locate_general_board_objects(board_object_value, board_position):
    board_objects = []
    for coordinate in range(1, 33):
       square_value = get_square_value(coordinate, board_position)
       if square_value & board_object_value:
           board_objects.append(coordinate)
    return board_objects

# Note: plugging a piece color constant into the above function will locate both pawns and kings,
# while plugging a piece color constant into the bottom function will locate only pawns.

def locate_specific_board_objects(board_object_value, board_position):
    board_objects = []
    for coordinate in range(1, 33):
       square_value = get_square_value(coordinate, board_position)
       square_value_without_back_rank_info = square_value & ~ON_BACK_RANK
       if board_object_value == square_value_without_back_rank_info:
           board_objects.append(coordinate)
    return board_objects

# IMMEDIATE VISION SEARCH FUNCTIONS (AND CONSTANTS):

# Note: the column numbers are periodic with the first 8 coordinates on the board, which means that
# the 'actual' / 'physical' first column on the board aligns with coordinate 5,
# the 'actual' / 'physical' second column on the board aligns with coordinate 1,
# the 'actual' / 'physical' third column on the board aligns with coordinate 6,
# etc. (However, since the modulo function is used to calculate the column number,
# 0 is used in place of 8.)

# The row number corresponds to the 'actual' / 'physical' board like normal (from top to bottom).

COLUMN_1 = 5
COLUMN_2 = 1
COLUMN_3 = 6
COLUMN_4 = 2
COLUMN_5 = 7
COLUMN_6 = 3
COLUMN_7 = 0
COLUMN_8 = 4

def DL_search(coordinate):
    n = coordinate
    column = n % 8
    row = math.ceil(n/4)
    if column in (COLUMN_2, COLUMN_4, COLUMN_6, COLUMN_8):
        new_coordinate = n + 4
    elif column != COLUMN_1 and row != 8:
        new_coordinate = n + 3
    else:
        new_coordinate = None
    return new_coordinate

def DR_search(coordinate):
    n = coordinate
    column = n % 8
    row = math.ceil(n/4)
    if column in (COLUMN_2, COLUMN_4, COLUMN_6):
        new_coordinate = n + 5
    elif column != COLUMN_8 and row != 8:
        new_coordinate = n + 4
    else:
        new_coordinate = None
    return new_coordinate

def UL_search(coordinate):
    n = coordinate
    column = n % 8
    row = math.ceil(n/4)
    if column in (COLUMN_3, COLUMN_5, COLUMN_7):
        new_coordinate = n - 5
    elif column != COLUMN_1 and row != 1:
        new_coordinate = n - 4
    else:
        new_coordinate = None
    return new_coordinate

def UR_search(coordinate):
    n = coordinate
    column = n % 8
    row = math.ceil(n/4)
    if column in (COLUMN_1, COLUMN_3, COLUMN_5, COLUMN_7):
        new_coordinate = n - 4
    elif column != COLUMN_8 and row != 1:
        new_coordinate = n - 3
    else:
        new_coordinate = None
    return new_coordinate

# SEARCH CONSTANTS:

SEARCHERS = {
    "down": (DL_search, DR_search),
    "up": (UL_search, UR_search)
}

LEFT = 0
RIGHT = 1

# SIMPLE MOVE SEARCH FUNCTIONS:

def simple_search(coordinate, board_position, vertical_search_direction):
    simples = []
    L_coordinate = SEARCHERS[vertical_search_direction][LEFT](coordinate)
    R_coordinate = SEARCHERS[vertical_search_direction][RIGHT](coordinate)
    destination_coordinates = [L_coordinate, R_coordinate]
    occupied_squares = locate_general_board_objects(IS_OCCUPIED, board_position)
    for destination_coordinate in destination_coordinates:
        if destination_coordinate not in occupied_squares and destination_coordinate is not None:
            simple = str(coordinate) + '-' + str(destination_coordinate)
            simples.append(simple)
    return simples

def find_pawn_simples(piece_color, board_position, search_direction):
    pawns = locate_specific_board_objects(piece_color, board_position)
    pawn_simples = []
    for coordinate in pawns:
        pawn_simples.extend(simple_search(coordinate, board_position, search_direction))
    return pawn_simples

def find_king_simples(piece_color, board_position):
    king_piece_value = piece_color + IS_KING
    kings = locate_specific_board_objects(king_piece_value, board_position)
    king_simples = []
    for coordinate in kings:
        D_simples = simple_search(coordinate, board_position, "down")
        U_simples = simple_search(coordinate, board_position, "up")
        king_simples.extend(D_simples + U_simples)
    return king_simples

def find_all_simples(piece_color, board_position, search_direction):
    simples = []
    pawn_simples = find_pawn_simples(piece_color, board_position, search_direction)
    king_simples = find_king_simples(piece_color, board_position)
    simples.extend(pawn_simples)
    simples.extend(king_simples)
    return simples

# BASIC JUMP SEARCH FUNCTION:

def jump_search(jumper_coordinate, previous_color, board_position, vertical_search_direction, horizontal_search_direction):
    occupied_squares = locate_general_board_objects(IS_OCCUPIED, board_position)
    jumper_value = get_square_value(jumper_coordinate, board_position)
    if previous_color is None:
        jumper_color = jumper_value & 3
    else:
        jumper_color = previous_color
    jumpee_coordinate = SEARCHERS[vertical_search_direction][horizontal_search_direction](jumper_coordinate)
    jumpee_value = get_square_value(jumpee_coordinate, board_position)
    if jumpee_value is not None:
        jumpee_color = jumpee_value & 3
        if jumpee_coordinate in occupied_squares and not (jumper_color & jumpee_color):
            destination_coordinate = SEARCHERS[vertical_search_direction][horizontal_search_direction](jumpee_coordinate)
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

def create_InitialPath(jumper_coordinate, jump_info, occupied_squares):
    jumpee = jump_info[1]
    destination = jump_info[2]
    if destination is not None and destination not in occupied_squares:
        InitialPath = Path(jumper_coordinate, destination)
        InitialPath.record_capture(jumpee)
        return InitialPath

def create_initial_pawn_paths(jumper_coordinate, board_position, vertical_search_direction):
    occupied_squares = locate_general_board_objects(IS_OCCUPIED, board_position)
    initial_pawn_paths = []
    L_jump_info = jump_search(jumper_coordinate, None, board_position, vertical_search_direction, LEFT)
    R_jump_info = jump_search(jumper_coordinate, None, board_position, vertical_search_direction, RIGHT)
    jump_info_for_initial_pawn_paths = [L_jump_info, R_jump_info]
    for jump_info in jump_info_for_initial_pawn_paths:
        if jump_info is not None:
            initial_pawn_paths.append(create_InitialPath(jumper_coordinate, jump_info, occupied_squares))
    return initial_pawn_paths

def create_initial_king_paths(jumper_coordinate, board_position):
    occupied_squares = locate_general_board_objects(IS_OCCUPIED, board_position)
    initial_king_paths = []
    DL_jump_info = jump_search(jumper_coordinate, None, board_position, "down", LEFT)
    DR_jump_info = jump_search(jumper_coordinate, None, board_position, "down", RIGHT)
    UL_jump_info = jump_search(jumper_coordinate, None, board_position, "up", LEFT)
    UR_jump_info = jump_search(jumper_coordinate, None, board_position, "up", RIGHT)
    jump_info_for_initial_king_paths = [DL_jump_info, DR_jump_info, UL_jump_info, UR_jump_info]
    for jump_info in jump_info_for_initial_king_paths:
        if jump_info is not None:
            initial_king_paths.append(create_InitialPath(jumper_coordinate, jump_info, occupied_squares))
    return initial_king_paths

# JUMP MOVE CALCULATION FUNCTIONS:

def create_pawn_path_calculation_info(path, piece_color, board_position, vertical_search_direction):
    Path_A = copy.deepcopy(path)
    if Path_A is not None:
        Path_A_jump_info = jump_search(Path_A.end_coordinate, piece_color, board_position, vertical_search_direction, LEFT)
    else:
        Path_A_jump_info = None
    Path_B = copy.deepcopy(path)
    if Path_B is not None:
        Path_B_jump_info = jump_search(Path_A.end_coordinate, piece_color, board_position, vertical_search_direction, RIGHT)
    else:
        Path_B_jump_info = None
    return (Path_A, Path_A_jump_info, Path_B, Path_B_jump_info)

def create_king_path_calculation_info(path, piece_color, board_position):
    Path_A = copy.deepcopy(path)
    if Path_A is not None:
        Path_A_jump_info = jump_search(Path_A.end_coordinate, piece_color, board_position, "down", LEFT)
    else:
        Path_A_jump_info = None
    Path_B = copy.deepcopy(path)
    if Path_B is not None:
        Path_B_jump_info = jump_search(Path_A.end_coordinate, piece_color, board_position, "down", RIGHT)
    else:
        Path_B_jump_info = None
    Path_C = copy.deepcopy(path)
    if Path_C is not None:
        Path_C_jump_info = jump_search(Path_A.end_coordinate, piece_color, board_position, "up", LEFT)
    else:
        Path_C_jump_info = None
    Path_D = copy.deepcopy(path)
    if Path_D is not None:
        Path_D_jump_info = jump_search(Path_A.end_coordinate, piece_color, board_position, "up", RIGHT)
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

def calculate_pawn_paths(jumper_coordinate, board_position, piece_color, vertical_search_direction):
    occupied_squares = locate_general_board_objects(IS_OCCUPIED, board_position)
    initial_pawn_paths = create_initial_pawn_paths(jumper_coordinate, board_position, vertical_search_direction)
    processing = []
    finished_paths = []
    for path in initial_pawn_paths:
        processing.append(path)
    while len(processing) > 0:
        for path in processing:
            path_calculation_info = create_pawn_path_calculation_info(path, piece_color, board_position, vertical_search_direction)
            paths_to_process = create_pawn_paths_to_process(path_calculation_info, occupied_squares)
            if len(paths_to_process) == 0:
                finished_paths.append(path)
            else:
                for updated_paths in paths_to_process:
                    processing.append(updated_paths)
            processing.remove(path)
    finished_pawn_paths = finished_paths
    return finished_pawn_paths

def calculate_king_paths(jumper_coordinate, board_position, piece_color):
    occupied_squares = locate_general_board_objects(IS_OCCUPIED, board_position)
    initial_king_paths = create_initial_king_paths(jumper_coordinate, board_position)
    processing = []
    finished_paths = []
    for path in initial_king_paths:
        processing.append(path)
    while len(processing) > 0:
        for path in processing:
            path_calculation_info = create_king_path_calculation_info(path, piece_color, board_position)
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

def list_all_possible_pawn_paths(piece_color, board_position, vertical_search_direction):
    possible_pawn_paths = []
    pawns = locate_specific_board_objects(piece_color, board_position)
    for pawn in pawns:
        pawn_paths = calculate_pawn_paths(pawn, board_position, piece_color, vertical_search_direction)
        if len(pawn_paths) > 0: possible_pawn_paths.extend(pawn_paths)
    return possible_pawn_paths

def list_all_possible_king_paths(piece_color, board_position):
    possible_king_paths = []
    king_value = piece_color + IS_KING
    kings = locate_specific_board_objects(king_value, board_position)
    for king in kings:
        king_paths = calculate_king_paths(king, board_position, piece_color)
        if len(king_paths) > 0: possible_king_paths.extend(king_paths)
    return possible_king_paths

def list_all_jump_moves(board_position, piece_color, vertical_search_direction):
    jump_moves = []
    pawn_paths = list_all_possible_pawn_paths(piece_color, board_position, vertical_search_direction)
    jump_moves.extend(pawn_paths)
    king_paths = list_all_possible_king_paths(piece_color, board_position)
    jump_moves.extend(king_paths)
    return jump_moves

# LIST ALL POSSIBLE MOVES FUNCTIONS:

def list_all_possible_moves(board_position, piece_color, vertical_search_direction):
    all_possible_moves = []
    jump_moves = list_all_jump_moves(board_position, piece_color, vertical_search_direction)
    simples = find_all_simples(piece_color, board_position, vertical_search_direction)
    if len(jump_moves) > 0:
        all_possible_moves.extend(jump_moves)
    else:
        all_possible_moves.extend(simples)
    return all_possible_moves

# USER INTERFACE CODE:

# "o" = black pawn, "O" = black king, "x" = red pawn, "X" = red king, " " = empty square, "=" = non-coordinate square



def translate_position(board_position):
    translated_position = []
    for square_value in board_position:
        match square_value:
            case 0:
                translated_position.append(" ")
            case 1:
                translated_position.append("\033[30;44mo\033[97;44m")
            case 2:
                translated_position.append("\033[31;44mx\033[97;44m")
            case 5:
                translated_position.append("\033[30;44mO\033[97;44m")
            case 6:
                translated_position.append("\033[31;44mX\033[97;44m")
            case 8:
                translated_position.append(" ")
            case 9:
                translated_position.append("\033[30;44mo\033[97;44m")
            case 10:
                translated_position.append("\033[31;44mx\033[97;44m")
            case 13:
                translated_position.append("\033[30;44mO\033[97;44m")
            case 14:
                translated_position.append("\033[31;44mX\033[97;44m")
    return translated_position

# The "T_" prefix indicates that the board position has been translated to a printable format.

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
        print("\033[0;44m" + row + "\033[0m")

def select_move_color(piece_color, board_position):
    if piece_color is BLACK_PIECE:
        moves = list_all_possible_moves(board_position, piece_color, "down")
        print("\nMoves for \033[30;107mblack\033[0m:\n")
    elif piece_color is RED_PIECE:
        moves = list_all_possible_moves(board_position, piece_color, "up")
        print("\nMoves for \033[31;107mred\033[0m:\n")
    return moves

def list_countable_moves(moves):
    count = 1
    for move in moves:
        move_string = f"{count}: {move}"
        print(move_string)
        count += 1
    return count

def select_move(piece_color, board_position):
    moves = select_move_color(piece_color, board_position)
    count = list_countable_moves(moves)
    while True:
        move_selection_number_string = input("\nSelect a move by entering the move number and pressing 'Enter': ")
        if not move_selection_number_string.isnumeric():
            print("\nInvalid move. Please try again.")
            continue
        else:
            move_selection_number_integer = int(move_selection_number_string)
            if move_selection_number_integer not in range(count) or move_selection_number_integer == 0:
                print("\nInvalid move. Please try again.")
                continue
            else:
                break
    selected_move = moves[move_selection_number_integer - 1]
    return selected_move

def update_start_and_end_coordinate_values(start_coordinate, end_coordinate, board_position):
    piece_value = get_square_value(start_coordinate, board_position)
    destination_value = get_square_value(end_coordinate, board_position)
    piece_on_back_rank = piece_value & ON_BACK_RANK
    piece_going_to_back_rank = destination_value & ON_BACK_RANK
    piece_is_king = piece_value & IS_KING
    if piece_on_back_rank:
        board_position[start_coordinate - 1] = ON_BACK_RANK
    else:
        board_position[start_coordinate - 1] = EMPTY_SQUARE
    if piece_going_to_back_rank:
        if piece_is_king:
            board_position[end_coordinate - 1] = piece_value + ON_BACK_RANK
        else:
            board_position[end_coordinate - 1] = piece_value + IS_KING + ON_BACK_RANK
    else:
        if piece_on_back_rank:
            board_position[end_coordinate - 1] = piece_value - ON_BACK_RANK
        else:
            board_position[end_coordinate - 1] = piece_value

def update_board_for_simple_move(selected_move, board_position):
    move_coordinates = re.split("[-]", selected_move)
    start_coordinate = int(move_coordinates[0])
    end_coordinate = int(move_coordinates[1])
    update_start_and_end_coordinate_values(start_coordinate, end_coordinate, board_position)

def update_board_for_jump_move(selected_move, board_position):
    start_coordinate = selected_move.start_coordinate
    end_coordinate = selected_move.end_coordinate
    captures = selected_move.captures
    update_start_and_end_coordinate_values(start_coordinate, end_coordinate, board_position)
    for capture in captures: board_position[capture - 1] = EMPTY_SQUARE

def play_selected_move(selected_move, board_position):
    if type(selected_move) is str:
        update_board_for_simple_move(selected_move, board_position)
        print(f"\nYou have played the simple move {selected_move}\n")
    elif type(selected_move) is Path:
        update_board_for_jump_move(selected_move, board_position)
        print(f"\nYou have played the jump move {selected_move}\n")

# PLAYABILITY:

def play_black_turn(board_position):
    black_move = select_move(BLACK_PIECE, board_position)
    play_selected_move(black_move, board_position)

def play_red_turn(board_position):
    red_move = select_move(RED_PIECE, board_position)
    play_selected_move(red_move, board_position)

def initiate_two_player_checkers_game():
    board_position = generate_starting_position()
    while True:
        any_legal_black_moves = list_all_possible_moves(board_position, BLACK_PIECE, "down")
        if any_legal_black_moves:
            print("Turn: \033[30;107mblack\033[0m\n")
            print_current_position(board_position)
            play_black_turn(board_position)
        else:
            print_current_position(board_position)
            print("\nGame over. \033[31;107mRed wins!\033[0m\n")
            break
        any_legal_red_moves = list_all_possible_moves(board_position, RED_PIECE, "up")
        if any_legal_red_moves:
            print("Turn: \033[31;107mred\033[0m\n")
            print_current_position(board_position)
            play_red_turn(board_position)
        else:
            print_current_position(board_position)
            print("\nGame over. \033[30;107mBlack wins!\033[0m\n")
            break

initiate_two_player_checkers_game()