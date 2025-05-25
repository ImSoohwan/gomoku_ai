import copy

def create_board(size):
    board = [[' ' for j in range(size)] for i in range(size)]
    return board

def print_board(board, blank_mark="#", number=False, O_mark = "O", X_mark = "X"):
    count = 0
    for rows in board:
        if number: 
            print("\033[33m", end="") #색상 입력 시작
            print(count, end=" ")
            print("\033[0m", end="") #색상 입력 초기화
        for cell in rows:
            print(blank_mark if cell==" " else (O_mark if cell == "O" else (X_mark if cell == "X" else "#")), end=" ")
        print("")
        count += 1

def is_valid_move(board, pos):
    px, py = pos
    size = len(board)
    if px < 0 or py < 0 or px >= size or py >= size:
        return False
    elif board[px][py] != " ":
        return False
    return True

def apply_move(board, pos, player):
    if(is_valid_move(board, pos)):
        px, py = pos
        newBoard = copy.deepcopy(board)
        newBoard[px][py] = player
        return newBoard
    else:
        return False

def is_out_of_board(board, pos):
    px, py = pos
    size = len(board)
    return px < 0 or py < 0 or px >= size or py >= size

def is_five_in_a_row(board, player, pos, dir):
    x_dir, y_dir = dir
    px, py = pos
    for i in range(5):
        if not is_out_of_board(board, (px + i*x_dir, py + i*y_dir)):
            stone = board[px + i*x_dir][py + i*y_dir]
            if stone != player:
                return False
        else:
            return False
    return True

def is_full(board):
    is_full = True
    for row in board:
        for cell in row:
            if cell == " ":
                is_full = False
    return is_full

def check_winner(board):
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    size = len(board)
    for px in range(size):
        for py in range(size):
            current_stone = board[px][py]
            if current_stone == " ": 
                continue
            for dir in directions:
                if (is_five_in_a_row(board, current_stone, (px, py), dir)):
                    return current_stone
    return None


