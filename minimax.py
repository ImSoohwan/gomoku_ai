from game import *

def any_stone_nearby(board, px, py, search_range=1):
    size = len(board)
    for i in range(px-search_range, px+search_range+1):
        for j in range(py-search_range, py+search_range+1):
            if (not is_valid_move(board, (i, j))) and (not is_out_of_board(board, (i, j))):
                return True
    return False

def get_possible_moves(board, search_range=1):
    size = len(board)
    possible_moves = []
    for px in range(size):
        for py in range(size):
            if any_stone_nearby(board, px, py, search_range) and is_valid_move(board, (px, py)):
                possible_moves.append((px, py))
    return possible_moves


def is_n_in_a_row(board, player, pos, dir, n):
    """
    해당 좌표부터 특정 방향으로 총 n개의 돌이 연속으로 놓여져 있는지 확인

    매개변수:
        board: 현재 보드 상태
        player: 검사할 돌의 종류
        pos: 검사 시작 좌표
        dir: 검사 방향
        n: 검사 개수
    
    반환값:
        True if n개의 돌이 연속되어 놓여져 있으면 else False
    """
    x_dir, y_dir = dir
    px, py = pos
    for i in range(n):
        x_pos, y_pos = (px + i*x_dir, py + i*y_dir)
        if not is_out_of_board(board, (x_pos, y_pos)):
            stone = board[x_pos][y_pos]
            if stone != player:
                return False
        else:
            return False
    return True


def check_both_ends(board, pos, dir, n):
    """
    찾은 연속된 돌 행렬의 양 끝이 열려 있는지 확인

    반환값:
        양 쪽 모두가 열려있으면 2, 하나만 열려있으면 1, 전부 막혀있으면 0 반환환
    """
    px, py = pos
    count = 0
    before_start_pos = (px - dir[0], py - dir[1])
    after_end_pos = (px + dir[0] * n, py + dir[1] * n)
    if is_valid_move(board, before_start_pos):
        count += 1
    if is_valid_move(board, after_end_pos):
        count += 1
    return count


def stones_in_a_row(board, player, num, exception):
    """
    n개의 돌이 연속으로 있는지 검사하는 함수

    매개변수:
        board: 현재 보드 상태
        player: 검사할 돌의 종류
        num: 연속된 몇개의 돌을 검사할 것인지
        exception: 검사에서 제외할 (시작좌표, 방향) 튜플플
    
    반환값:
        다음 튜플의 리스트
        tuple: 연속된 돌을 찾았는지, 열린 방향 수 (0~2)

    """
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    size = len(board)
    found_rows = []
    for px in range(size):
        for py in range(size):
            if board[px][py] == player:
                for dir in directions:
                    if ((px, py), dir) in exception: continue
                    if(is_n_in_a_row(board, player, (px,py), dir, num)):
                        both_ends = check_both_ends(board, (px, py), dir, num)
                        new_exceptions = set()
                        for i in range(num):
                            new_exceptions.add(((px+dir[0]*i, py+dir[1]*i), dir))
                        found_rows.append((True, both_ends, new_exceptions))
    return found_rows

SCORES = {
    "4_in_a_row_2_open": 100000,
    "4_in_a_row_1_open": 1000,
    "3_in_a_row_2_open": 500,
    "3_in_a_row_1_open": 50,
    "2_in_a_row_2_open": 10,
    "2_in_a_row_1_open": 1,
}

def evaluate_board(board, ai):
    score = 0
    exception = set()
    for num in [4,3,2]:
        found_rows = stones_in_a_row(board, ai, num, exception)
        for found in found_rows:
            _, opens, new_exceptions = found
            exception = exception.union(new_exceptions)
            if opens == 2 or opens == 1:
                score += SCORES[f"{num}_in_a_row_{opens}_open"]

    return score


def get_optimal_move(board, ai, opponent, isMaximizing, current_depth, max_depth=3):
    winner = check_winner(board)
    if winner is not None: return 1000000 if winner == ai else -1000000
    elif current_depth >= max_depth: return evaluate_board(board, ai) - evaluate_board(board, opponent)

    possible_moves = get_possible_moves(board, search_range=1)
    score = float("-inf") if isMaximizing else float("inf")
    optimal_move = None 
    for move in possible_moves:
        newboard = apply_move(board, move, ai if isMaximizing else opponent)
        if not newboard: continue

        newScore = get_optimal_move(newboard, ai, opponent, not isMaximizing, current_depth+1, max_depth)
        if (isMaximizing and newScore > score) or (not isMaximizing and newScore < score):
            score = newScore
            optimal_move = move

    if current_depth == 1:
        return (score, optimal_move)
    return score

    





