# PAWN JUMP MOVE FINDERS (taken from main file)

class PawnPath:
    def __init__(self, start_coordinate, end_coordinate):
        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate
        self.captures = []
    
    # def __init__(self, source):
    #     self.start_coordinate = source.start_coordinate
    #     self.end_coordinate = source.end_coordinate
    #     self.captures = source.captures

    def record_capture(self, jumpee):
        self.captures.append(jumpee)
    
    def __str__(self):
        return f"{self.start_coordinate}x{self.end_coordinate} {self.captures}"

def create_down_jump_input(DL_jump_info, DR_jump_info):
    down_jump_input = []
    if DL_jump_info is not None:
        if DL_jump_info[2] is not None:
            Path_A = PawnPath(DL_jump_info[0], DL_jump_info[2])
            Path_A.captures.append(DL_jump_info[1])
            down_jump_input.append(Path_A)
    if DR_jump_info is not None:
        if DR_jump_info[2] is not None:
            Path_B = PawnPath(DR_jump_info[0], DR_jump_info[2])
            Path_B.captures.append(DR_jump_info[1]) 
            down_jump_input.append(Path_B)
    return down_jump_input

def create_down_jump_processing_and_output(input, output):
    down_jump_processing = []
    down_jump_output = []
    for path in input:
        update_detection = 0
        New_Path_1 = PawnPath(path.start_coordinate, path.end_coordinate)
        New_Path_1.captures = path.captures
        print(New_Path_1)
        New_Path_2 = PawnPath(path.start_coordinate, path.end_coordinate)
        New_Path_2.captures = path.captures
        print(New_Path_2)
        if DL_jump_search(New_Path_1.end_coordinate) is not None:
            if DL_jump_search(New_Path_1.end_coordinate)[2] is not None:
                New_Path_1.captures.append(DL_jump_search(New_Path_1.end_coordinate)[1])
                New_Path_1.end_coordinate = DL_jump_search(New_Path_1.end_coordinate)[2]
                down_jump_processing.append(New_Path_1)
                update_detection = update_detection + 1
        if DR_jump_search(New_Path_2.end_coordinate) is not None:
            if DR_jump_search(New_Path_2.end_coordinate)[2] is not None:
                New_Path_2.captures.append(DR_jump_search(New_Path_2.end_coordinate)[1])
                New_Path_2.end_coordinate = DR_jump_search(New_Path_2.end_coordinate)[2]
                down_jump_processing.append(New_Path_2)
                update_detection = update_detection + 1
        if update_detection == 0 and path not in output:
            down_jump_output.append(path)
    return (down_jump_processing, down_jump_output)

def find_single_black_pawn_jump_moves(jumper_coordinate):
    DL_jump_info = DL_jump_search(jumper_coordinate)
    DR_jump_info = DR_jump_search(jumper_coordinate)
    down_jump_input = create_down_jump_input(DL_jump_info, DR_jump_info)
    input = []
    processing = []
    output = []
    for path in down_jump_input:
        input.append(path)
    while True:
        down_jump_processing = create_down_jump_processing_and_output(input, output)[0]
        down_jump_output = create_down_jump_processing_and_output(input, output)[1]
        for path in down_jump_processing:
            processing.append(path)
        for path in down_jump_output:
            output.append(path)
        if len(processing) == 0:
            break    
        input.clear()
        for path in processing:
            input.append(path)
        processing.clear()
    single_black_pawn_jump_moves = output
    return single_black_pawn_jump_moves

































def create_initial_black_pawn_paths(jumper_coordinate):
    initial_black_pawn_paths = []
    DL_jump_possibility = DL_jump_search(jumper_coordinate)
    DR_jump_possibility = DR_jump_search(jumper_coordinate)
    if DL_jump_possibility is not None:
        DL_jumpee = DL_jump_search(jumper_coordinate)[1]
        DL_destination = DL_jump_search(jumper_coordinate)[2]
        if DL_jumpee is not None and DL_destination is not None:
            Path_DL = PawnPath(jumper_coordinate, DL_destination)
            Path_DL.record_capture(DL_jumpee)
            initial_black_pawn_paths.append(Path_DL)
    if DR_jump_possibility is not None:
        DR_jumpee = DR_jump_search(jumper_coordinate)[1]
        DR_destination = DR_jump_search(jumper_coordinate)[2]
        if DR_jumpee is not None and DR_destination is not None:
            Path_DR = PawnPath(jumper_coordinate, DR_destination)
            Path_DR.record_capture(DR_jumpee)
            initial_black_pawn_paths.append(Path_DR)
    return initial_black_pawn_paths

def process_black_pawn_paths(unfinished_black_pawn_paths, completed_black_pawn_paths):
    partially_processed_black_pawn_paths = []
    fully_processed_black_pawn_paths = []
    for path in unfinished_black_pawn_paths:
        update_detection = 0
        end_coordinate = path.end_coordinate
        DL_jump_possibility = DL_jump_search(end_coordinate)
        DR_jump_possibility = DR_jump_search(end_coordinate)
        if DL_jump_possibility is not None:
            DL_jumpee = DL_jump_search(end_coordinate)[1]
            DL_destination = DL_jump_search(end_coordinate)[2]
            if DL_jumpee is not None and DL_destination is not None:
                Path_A = copy.deepcopy(path)
                Path_A.record_capture(DL_jumpee)
                Path_A.end_coordinate = DL_destination
                partially_processed_black_pawn_paths.append(Path_A)
                update_detection = update_detection + 1
        if DR_jump_possibility is not None:
            DR_jumpee = DR_jump_search(end_coordinate)[1]
            DR_destination = DR_jump_search(end_coordinate)[2]
            if DR_jumpee is not None and DR_destination is not None:
                Path_B = copy.deepcopy(path)
                Path_B.record_capture(DL_jumpee)
                Path_B.end_coordinate = DL_destination
                partially_processed_black_pawn_paths.append(Path_B)
                update_detection = update_detection + 1
        if path not in completed_black_pawn_paths:
            fully_processed_black_pawn_paths.append(path)
    return (partially_processed_black_pawn_paths, fully_processed_black_pawn_paths)

def find_jump_moves_for_single_black_pawn(jumper_coordinate):
    completed_black_pawn_paths = []
    unfinished_black_pawn_paths = []
    initial_black_pawn_paths = create_initial_black_pawn_paths(jumper_coordinate)
    if len(initial_black_pawn_paths) != 0:
        partially_processed_black_pawn_paths = process_black_pawn_paths(initial_black_pawn_paths, completed_black_pawn_paths)[0]
        fully_processed_black_pawn_paths = process_black_pawn_paths(initial_black_pawn_paths, completed_black_pawn_paths)[1]
        for path in partially_processed_black_pawn_paths:
            unfinished_black_pawn_paths.append(path)
        for path in fully_processed_black_pawn_paths:
            completed_black_pawn_paths.append(path)
    while True:
        partially_processed_black_pawn_paths = process_black_pawn_paths(unfinished_black_pawn_paths, completed_black_pawn_paths)[0]
        fully_processed_black_pawn_paths = process_black_pawn_paths(unfinished_black_pawn_paths, completed_black_pawn_paths)[1]
        for path in fully_processed_black_pawn_paths:
            completed_black_pawn_paths.append(path)
        if len(partially_processed_black_pawn_paths) == 0:
            break
        unfinished_black_pawn_paths.clear
        for path in partially_processed_black_pawn_paths:
            unfinished_black_pawn_paths.append(path)
    jump_moves = completed_black_pawn_paths
    return jump_moves






































# old jump stuff



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
