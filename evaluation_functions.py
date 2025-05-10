from Constants import *
from game import game_over, get_valid_shots, play_a_shot


def evaluate_function_v1(grid, player):
    # dans cette fonction d'évaluation, on prend en compte trois paramètres principaux, le nombre de pions, la mobilité et les coins
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    corners = [(0,0), (ROWS-1,0), (0,COLS-1), (ROWS-1,COLS-1)]
    
    # nombre de pions
    player_tokens, opponent_tokens = 0, 0
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row,col] != EMPTY:
                if grid[row,col] == player :
                    player_tokens += 1
                else:
                    opponent_tokens += 1

    # mobilité
    player_moves, opponent_moves = 0, 0
    player_moves = len(get_valid_shots(grid=grid, player=player))
    opponent_moves = len(get_valid_shots(grid=grid, player=opponent))

    # coins
    player_corners, opponent_corners = 0, 0
    for y, x in corners :
        if grid[y,x] == player:
            player_corners += 1
        elif grid[y,x] == opponent:
            opponent_corners += 1

    # cacluls des différents scores
    if player_tokens + opponent_tokens != 0:
        token_score = 100 * (player_tokens - opponent_tokens) / (player_tokens + opponent_tokens)
    else :
        token_score = 0
    
    if player_moves + opponent_moves != 0:
        mobility_score = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
    else : 
        mobility_score = 0
    
    if player_corners + opponent_corners != 0:
        corner_score = 100 * (player_corners - opponent_corners) / (player_corners + opponent_corners)
    else:
        corner_score = 0 
    
    final_score = (50*token_score) + (0*mobility_score) + (0*corner_score)

    return final_score



def is_corner(move, board_size):
    return move in [(0, 0), (0, board_size - 1), (board_size - 1, 0), (board_size - 1, board_size - 1)]


def evaluate_function_v2(grid, player):
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    corners = [(0, 0), (ROWS - 1, 0), (0, COLS - 1), (ROWS - 1, COLS - 1)]

    empty_cells = 0
    player_tokens, opponent_tokens = 0, 0

    for row in range(ROWS):
        for col in range(COLS):
            token = grid[row, col]
            if token == EMPTY:
                empty_cells += 1
            elif token == player:
                player_tokens += 1
            elif token == opponent:
                opponent_tokens += 1

    # Valid moves
    player_moves = len(get_valid_shots(grid, player))
    opponent_moves = len(get_valid_shots(grid, opponent))

    # Coin control
    player_corners = sum(1 for y, x in corners if grid[y, x] == player)
    opponent_corners = sum(1 for y, x in corners if grid[y, x] == opponent)

    # Dangerous zones around corners
    dangerous_positions = [
        (0, 1), (1, 0), (1, 1),
        (0, COLS - 2), (1, COLS - 1), (1, COLS - 2),
        (ROWS - 2, 0), (ROWS - 1, 1), (ROWS - 2, 1),
        (ROWS - 2, COLS - 1), (ROWS - 1, COLS - 2), (ROWS - 2, COLS - 2)
    ]

    dangerous_count = sum(1 for y, x in dangerous_positions if grid[y, x] == player)
    dangerous_norm = (dangerous_count / 12) * 100

    # Positional weight
    max_pos_score = sum(max(row) for row in POSITION_WEIGHTS)
    position_score = 0

    for row in range(ROWS):
        for col in range(COLS):
            if grid[row, col] == player:
                position_score += POSITION_WEIGHTS[row][col]
            elif grid[row, col] == opponent:
                position_score -= POSITION_WEIGHTS[row][col]

    position_score_norm = (position_score / max_pos_score) * 100

    # Normalized scores [-100, 100]
    token_score = (
        100 * (player_tokens - opponent_tokens) / (player_tokens + opponent_tokens)
        if (player_tokens + opponent_tokens) != 0 else 0
    )
    mobility_score = (
        100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
        if (player_moves + opponent_moves) != 0 else 0
    )
    corner_score = (
        100 * (player_corners - opponent_corners) / (player_corners + opponent_corners)
        if (player_corners + opponent_corners) != 0 else 0
    )

    # Dynamic weights by phase
    token_weight = 2.0
    mobility_weight = 2.0
    corner_weight = 4.0
    danger_weight = 0.5
    pos_weight = 1.0

    # Bonus explicite si on contrôle un coin
    corner_bonus = 15 * player_corners

    final_score = (
        token_weight * token_score +
        mobility_weight * mobility_score +
        corner_weight * corner_score +
        -danger_weight * dangerous_norm +
        pos_weight * position_score_norm +
        corner_bonus
    )
    

    # Debug
    print(f"[DEBUG] T:{token_score:>6.1f} | M:{mobility_score:>6.1f} | C:{corner_score:>6.1f} | "
          f"Danger:{dangerous_norm:>6.1f} | Pos:{position_score_norm:>6.1f} => Total:{final_score:>7.1f}")

    return final_score
