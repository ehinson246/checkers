#!/usr/bin/env python3

# black moves down, red moves up
# U = up, D = down, L = left, R = right (when used as prefixes for search functions & variables)

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

# The board position is a list of bitmaps, where each list item corresponds to a coordinate
# on the actual board. Add 1 to the list item index to calculate the corresponding coordinate.

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

def locate_general_board_objects(board_position, board_object_value):
    board_objects = []
    for coordinate in range(1, 33):
       square_value = get_square_value(coordinate, board_position)
       if square_value & board_object_value:
           board_objects.append(coordinate)
    return board_objects

# Note: plugging a piece color constant into the above function will locate both pawns and kings,
# while plugging a piece color constant into the bottom function will locate only pawns.

def locate_specific_board_objects(board_position, board_object_value):
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

# In checkers, a "simple" move occurs when a piece moves from its current position
# to an immediately adjacent empty square without capturing anything.
# Example notation: "1-5" would mean a piece on square 1 moved to the empty square 5.

def simple_search(coordinate, board_position, vertical_search_direction):
    simples = []
    L_coordinate = SEARCHERS[vertical_search_direction][LEFT](coordinate)
    R_coordinate = SEARCHERS[vertical_search_direction][RIGHT](coordinate)
    destination_coordinates = [L_coordinate, R_coordinate]
    occupied_squares = locate_general_board_objects(board_position, IS_OCCUPIED)
    for destination_coordinate in destination_coordinates:
        if destination_coordinate not in occupied_squares and destination_coordinate is not None:
            simple = str(coordinate) + '-' + str(destination_coordinate)
            simples.append(simple)
    return simples

def find_pawn_simples(board_position, piece_color, search_direction):
    pawns = locate_specific_board_objects(board_position, piece_color)
    pawn_simples = []
    for coordinate in pawns:
        pawn_simples.extend(simple_search(coordinate, board_position, search_direction))
    return pawn_simples

def find_king_simples(board_position, piece_color):
    king_piece_value = piece_color + IS_KING
    kings = locate_specific_board_objects(board_position, king_piece_value)
    king_simples = []
    for coordinate in kings:
        D_simples = simple_search(coordinate, board_position, "down")
        U_simples = simple_search(coordinate, board_position, "up")
        king_simples.extend(D_simples + U_simples)
    return king_simples

def find_all_simples(board_position, piece_color, search_direction):
    simples = []
    pawn_simples = find_pawn_simples(board_position, piece_color, search_direction)
    king_simples = find_king_simples(board_position, piece_color)
    simples.extend(pawn_simples + king_simples)
    return simples

# BASIC JUMP SEARCH FUNCTION:

def jump_search(jumper_coordinate, board_position, jumper_color, vertical_search_direction, horizontal_search_direction):
    occupied_squares = locate_general_board_objects(board_position, IS_OCCUPIED)
    jumpee_coordinate = SEARCHERS[vertical_search_direction][horizontal_search_direction](jumper_coordinate)
    if jumpee_coordinate is not None and jumpee_coordinate in occupied_squares:
        jumpee_value = get_square_value(jumpee_coordinate, board_position)
        jumpee_can_be_captured = jumpee_value & ~jumper_color
        if jumpee_can_be_captured:
            destination_coordinate = SEARCHERS[vertical_search_direction][horizontal_search_direction](jumpee_coordinate)
            jump_info = (jumpee_coordinate, destination_coordinate)
            return jump_info

JUMPEE = 0
DESTINATION = 1

# JUMP MOVE INITIALIZATION FUNCTIONS:
        
class Path:
    def __init__(self, start_coordinate, end_coordinate):
        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate
        self.captures = []

    def record_capture(self, jumpee_coordinate):
        if jumpee_coordinate not in self.captures:
            self.captures.append(jumpee_coordinate)
    
    def __str__(self):
        return f"{self.start_coordinate}x{self.end_coordinate} {self.captures}"

def create_initial_path(jumper_coordinate, jump_info, occupied_squares):
    jumpee_coordinate = jump_info[JUMPEE]
    destination_coordinate = jump_info[DESTINATION]
    if destination_coordinate is not None and destination_coordinate not in occupied_squares:
        initial_path = Path(jumper_coordinate, destination_coordinate)
        initial_path.record_capture(jumpee_coordinate)
        return initial_path

def process_jump_info(jumper_coordinate, jump_info, board_position):
    occupied_squares = locate_general_board_objects(board_position, IS_OCCUPIED)
    if jump_info is not None:
        destination_coordinate = jump_info[DESTINATION]
        if destination_coordinate is not None and destination_coordinate not in occupied_squares:
            initial_path = create_initial_path(jumper_coordinate, jump_info, occupied_squares)
            return initial_path

def create_initial_pawn_paths(jumper_coordinate, board_position, piece_color, vertical_search_direction):
    initial_pawn_paths = []
    L_jump_info = jump_search(jumper_coordinate, board_position, piece_color, vertical_search_direction, LEFT)
    R_jump_info = jump_search(jumper_coordinate, board_position, piece_color, vertical_search_direction, RIGHT)
    jump_info_for_initial_pawn_paths = [L_jump_info, R_jump_info]
    for jump_info in jump_info_for_initial_pawn_paths:
        initial_path = process_jump_info(jumper_coordinate, jump_info, board_position)
        if initial_path is not None: initial_pawn_paths.append(initial_path)
    return initial_pawn_paths

def create_initial_king_paths(jumper_coordinate, board_position, piece_color):
    initial_king_paths = []
    DL_jump_info = jump_search(jumper_coordinate, board_position, piece_color, "down", LEFT)
    DR_jump_info = jump_search(jumper_coordinate, board_position, piece_color, "down", RIGHT)
    UL_jump_info = jump_search(jumper_coordinate, board_position, piece_color, "up", LEFT)
    UR_jump_info = jump_search(jumper_coordinate, board_position, piece_color, "up", RIGHT)
    jump_info_for_initial_king_paths = [DL_jump_info, DR_jump_info, UL_jump_info, UR_jump_info]
    for jump_info in jump_info_for_initial_king_paths:
        initial_path = process_jump_info(jumper_coordinate, jump_info, board_position)
        if initial_path is not None: initial_king_paths.append(initial_path)
    return initial_king_paths

# JUMP MOVE CALCULATION FUNCTIONS:

def create_pawn_path_jump_branch_info(current_path, board_position, piece_color, vertical_search_direction):
    if current_path is not None:
        L_jump_branch_info = jump_search(current_path.end_coordinate,
                                         board_position, piece_color,
                                         vertical_search_direction, LEFT)
        R_jump_branch_info = jump_search(current_path.end_coordinate,
                                         board_position, piece_color,
                                         vertical_search_direction, RIGHT)
        jump_branch_info = (L_jump_branch_info, R_jump_branch_info)
        return jump_branch_info

def create_king_path_jump_branch_info(current_path, board_position, piece_color):
    if current_path is not None:
        DL_jump_branch_info = jump_search(current_path.end_coordinate,
                                          board_position, piece_color,
                                          "down", LEFT)
        DR_jump_branch_info = jump_search(current_path.end_coordinate,
                                          board_position, piece_color,
                                          "down", RIGHT)
        UL_jump_branch_info = jump_search(current_path.end_coordinate,
                                          board_position, piece_color,
                                          "up", LEFT)
        UR_jump_branch_info = jump_search(current_path.end_coordinate,
                                          board_position, piece_color,
                                          "up", RIGHT)
        jump_branch_info = (DL_jump_branch_info, DR_jump_branch_info,
                            UL_jump_branch_info, UR_jump_branch_info)
        return jump_branch_info

def update_current_pawn_path(current_path, jump_branch_info, occupied_squares):
    new_paths = []
    L_path_jump_info = jump_branch_info[0]
    R_path_jump_info = jump_branch_info[1]
    potential_branches = [L_path_jump_info, R_path_jump_info]
    for jump_branch in potential_branches:
        if jump_branch is not None:
            jumpee_coordinate = jump_branch[JUMPEE]
            destination_coordinate = jump_branch[DESTINATION]
            if destination_coordinate is not None:
                if destination_coordinate not in occupied_squares:
                    new_path = copy.deepcopy(current_path)
                    new_path.record_capture(jumpee_coordinate)
                    new_path.end_coordinate = destination_coordinate
                    new_paths.append(new_path)
    return new_paths

def update_current_king_path(current_path, jump_branch_info, occupied_squares):
    new_paths = []
    DL_path_jump_info = jump_branch_info[0]
    DR_path_jump_info = jump_branch_info[1]
    UL_path_jump_info = jump_branch_info[2]
    UR_path_jump_info = jump_branch_info[3]
    potential_branches = [DL_path_jump_info, DR_path_jump_info,
                          UL_path_jump_info, UR_path_jump_info]
    previous_captures = current_path.captures
    for jump_branch in potential_branches:
        if jump_branch is not None:
            jumpee_coordinate = jump_branch[JUMPEE]
            destination_coordinate = jump_branch[DESTINATION]
            if destination_coordinate is not None and \
               jumpee_coordinate not in previous_captures:
                if destination_coordinate not in occupied_squares or \
                   destination_coordinate == current_path.start_coordinate:
                    new_path = copy.deepcopy(current_path)
                    new_path.record_capture(jumpee_coordinate)
                    new_path.end_coordinate = destination_coordinate
                    new_paths.append(new_path)
    return new_paths

def calculate_pawn_paths(jumper_coordinate, board_position, piece_color, vertical_search_direction):
    occupied_squares = locate_general_board_objects(board_position, IS_OCCUPIED)
    processing = create_initial_pawn_paths(jumper_coordinate, board_position, piece_color, vertical_search_direction)
    finished_paths = []
    while len(processing) > 0:
        for current_path in processing:
            jump_branch_info = create_pawn_path_jump_branch_info(current_path,
                                                                 board_position, piece_color,
                                                                 vertical_search_direction)
            paths_to_process = update_current_pawn_path(current_path, jump_branch_info, occupied_squares)
            if len(paths_to_process) == 0:
                finished_paths.append(current_path)
            else:
                processing.extend(paths_to_process)
            processing.remove(current_path)
    finished_pawn_paths = finished_paths
    return finished_pawn_paths

def calculate_king_paths(jumper_coordinate, board_position, piece_color):
    occupied_squares = locate_general_board_objects(board_position, IS_OCCUPIED)
    processing = create_initial_king_paths(jumper_coordinate, board_position, piece_color)
    finished_paths = []
    while len(processing) > 0:
        for path in processing:
            jump_branch_info = create_king_path_jump_branch_info(path, board_position, piece_color)
            paths_to_process = update_current_king_path(path, jump_branch_info, occupied_squares)
            if len(paths_to_process) == 0:
                finished_paths.append(path)
            else:
                processing.extend(paths_to_process)
            processing.remove(path)
    finished_king_paths = finished_paths
    return finished_king_paths

# JUMP MOVE LIST FUNCTIONS:

def list_all_possible_pawn_paths(board_position, piece_color, vertical_search_direction):
    possible_pawn_paths = []
    pawns = locate_specific_board_objects(board_position, piece_color)
    for pawn in pawns:
        pawn_paths = calculate_pawn_paths(pawn, board_position, piece_color, vertical_search_direction)
        if len(pawn_paths) > 0: possible_pawn_paths.extend(pawn_paths)
    return possible_pawn_paths

def list_all_possible_king_paths(board_position, piece_color):
    possible_king_paths = []
    king_piece_value = piece_color + IS_KING
    kings = locate_specific_board_objects(board_position, king_piece_value)
    for king in kings:
        king_paths = calculate_king_paths(king, board_position, piece_color)
        if len(king_paths) > 0: possible_king_paths.extend(king_paths)
    return possible_king_paths

def list_all_jump_moves(board_position, piece_color, vertical_search_direction):
    jump_moves = []
    pawn_paths = list_all_possible_pawn_paths(board_position, piece_color, vertical_search_direction)
    jump_moves.extend(pawn_paths)
    king_paths = list_all_possible_king_paths(board_position, piece_color)
    jump_moves.extend(king_paths)
    return jump_moves

# LIST ALL POSSIBLE MOVES FUNCTIONS:

def list_all_possible_moves(board_position, piece_color, vertical_search_direction):
    all_possible_moves = []
    jump_moves = list_all_jump_moves(board_position, piece_color, vertical_search_direction)
    simples = find_all_simples(board_position, piece_color, vertical_search_direction)
    if len(jump_moves) > 0:
        all_possible_moves.extend(jump_moves)
    else:
        all_possible_moves.extend(simples)
    return all_possible_moves

# USER INTERFACE CODE:

# " " = empty square (0 & 8)
# "o" = black pawn (1 & 9), "O" = black king (5 & 13),
# "x" = red pawn (2 & 6), "X" = red king (10 & 14),

def translate_position(board_position):
    translated_position = []
    for square_value in board_position:
        match square_value:
            case 0:
                translated_position.append(" ")
            case 8:
                translated_position.append(" ")
            case 1:
                translated_position.append("\033[30;44mo\033[97;44m")
            case 9:
                translated_position.append("\033[30;44mo\033[97;44m")
            case 5:
                translated_position.append("\033[30;44mO\033[97;44m")
            case 13:
                translated_position.append("\033[30;44mO\033[97;44m")
            case 2:
                translated_position.append("\033[31;44mx\033[97;44m")
            case 6:
                translated_position.append("\033[31;44mX\033[97;44m")
            case 10:
                translated_position.append("\033[31;44mx\033[97;44m")
            case 14:
                translated_position.append("\033[31;44mX\033[97;44m")
    return translated_position

# The "T_" prefix indicates that the board position has been translated to a printable format.
# "=" = non-coordinate square

def create_board_rows(T_board_position):
    row_1 = f"|=|{T_board_position[0]}|=|{T_board_position[1]}|=|{T_board_position[2]}|=|{T_board_position[3]}|"
    row_2 = f"|{T_board_position[4]}|=|{T_board_position[5]}|=|{T_board_position[6]}|=|{T_board_position[7]}|=|"
    row_3 = f"|=|{T_board_position[8]}|=|{T_board_position[9]}|=|{T_board_position[10]}|=|{T_board_position[11]}|"
    row_4 = f"|{T_board_position[12]}|=|{T_board_position[13]}|=|{T_board_position[14]}|=|{T_board_position[15]}|=|"
    row_5 = f"|=|{T_board_position[16]}|=|{T_board_position[17]}|=|{T_board_position[18]}|=|{T_board_position[19]}|"
    row_6 = f"|{T_board_position[20]}|=|{T_board_position[21]}|=|{T_board_position[22]}|=|{T_board_position[23]}|=|"
    row_7 = f"|=|{T_board_position[24]}|=|{T_board_position[25]}|=|{T_board_position[26]}|=|{T_board_position[27]}|"
    row_8 = f"|{T_board_position[28]}|=|{T_board_position[29]}|=|{T_board_position[30]}|=|{T_board_position[31]}|=|"
    rows = (row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8)
    return rows

def print_current_position(board_position):
    T_board_position = translate_position(board_position)
    rows = create_board_rows(T_board_position)
    for row in rows:
        print("\033[0;44m" + row + "\033[0m")

# MOVE SELECTION FUNCTIONS:

def select_move_color(board_position, piece_color):
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

def select_move(board_position, piece_color):
    moves = select_move_color(board_position, piece_color)
    count = list_countable_moves(moves)
    while True:
        move_selection_number_string = input("\nSelect a move by entering the move number and pressing 'Enter': ")
        if move_selection_number_string == "Q":
            quit()
        elif not move_selection_number_string.isnumeric():
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

# BOARD UPDATE FUNCTIONS:

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

# PLAYABILITY FUNCTIONS:

def play_selected_move(selected_move, board_position):
    if type(selected_move) is str:
        update_board_for_simple_move(selected_move, board_position)
        print(f"\nYou have played the simple move {selected_move}\n")
    elif type(selected_move) is Path:
        update_board_for_jump_move(selected_move, board_position)
        print(f"\nYou have played the jump move {selected_move}\n")

def play_turn(board_position, piece_color):
    move = select_move(board_position, piece_color)
    play_selected_move(move, board_position)

def generate_custom_position():
    custom_board_position = generate_empty_board()
    # custom_board_position[0] = EMPTY_SQUARE
    return custom_board_position 

TURN_TRACKER = {
    0: (RED_PIECE, "up", "[31;107m", "red", "[30;107m", "Black wins!"),
    1: (BLACK_PIECE, "down", "[30;107m", "black", "[31;107m", "Red wins!")
}

# 0 = red's turn, 1 = black's turn

def initiate_two_player_checkers_game():
    board_position = generate_starting_position()
    # board_position = generate_custom_position()
    whose_turn = 1
    while True:
        any_legal_moves = list_all_possible_moves(board_position, TURN_TRACKER[whose_turn][0], TURN_TRACKER[whose_turn][1])
        if any_legal_moves:
            print(f"Turn: \033{TURN_TRACKER[whose_turn][2]}{TURN_TRACKER[whose_turn][3]}\033[0m\n")
            print_current_position(board_position)
            play_turn(board_position, TURN_TRACKER[whose_turn][0])
        else:
            print_current_position(board_position)
            print(f"\nGame over. \033{TURN_TRACKER[whose_turn][4]}{TURN_TRACKER[whose_turn][5]}\033[0m\n")
            break
        whose_turn = (whose_turn + 1) % 2

initiate_two_player_checkers_game()