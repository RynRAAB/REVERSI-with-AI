# Dans ce fichier, on implémente l'intelligence artificielle pour le jeu du Reversi

from Constants import *
from game import game_over, get_valid_shots, play_a_shot

# fonction d'évaluation de chaque état de notre jeu, elle donne estimation sur l'état du jeu
def evaluate_function(grid, player):
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    corners = [(0, 0), (ROWS-1, 0), (0, COLS-1), (ROWS-1, COLS-1)]
    
    empty_cells = 0
    player_tokens, opponent_tokens = 0, 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row, col] == EMPTY:
                empty_cells += 1
            elif grid[row, col] == player:
                player_tokens += 1
            else:
                opponent_tokens += 1

    player_moves_list = get_valid_shots(grid=grid, player=player)
    player_moves = len(player_moves_list)
    opponent_moves = len(get_valid_shots(grid=grid, player=opponent))

    # Coins possédés
    player_corners, opponent_corners = 0, 0
    for y, x in corners:
        if grid[y, x] == player:
            player_corners += 1
        elif grid[y, x] == opponent:
            opponent_corners += 1

    # Bonus si des coups capturent un coin
    coin_move_bonus = 0
    for row, col in [m[:2] for m in player_moves_list]:
        if (row, col) in corners:
            coin_move_bonus += 1

    # Cases dangereuses autour des coins
    dangerous_positions = [
        (0, 1), (1, 0), (1, 1), 
        (0, COLS-2), (1, COLS-1), (1, COLS-2),
        (ROWS-2, 0), (ROWS-1, 1), (ROWS-2, 1),
        (ROWS-2, COLS-1), (ROWS-1, COLS-2), (ROWS-2, COLS-2)
    ]
    dangerous_penalty = 0
    for y, x in dangerous_positions:
        if grid[y, x] == player:
            dangerous_penalty -= 1
        elif grid[y, x] == opponent:
            dangerous_penalty += 1

    # Bonus de capture (pions retournés)
    capture_bonus = 0
    for row, col in [m[:2] for m in player_moves_list]:
        grid_copy = grid.copy()
        play_a_shot(grid=grid_copy, player=player, position=(row, col), number_of_tokens=[2, 2])
        opponent_tokens_after = sum(
            1 for r in range(ROWS) for c in range(COLS)
            if grid_copy[r, c] == opponent
        )
        captured = opponent_tokens - opponent_tokens_after
        capture_bonus += captured 
    if player_moves_list:
        capture_bonus /= len(player_moves_list)

    # Score positionnel
    position_score = 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row, col] == player:
                position_score += POSITION_WEIGHTS[row][col]
            elif grid[row, col] == opponent:
                position_score -= POSITION_WEIGHTS[row][col]

    # Poids dynamiques selon le moment de la partie
    if empty_cells > 10:  # début ou milieu
        token_weight = 20
        mobility_weight = 40
        corner_weight = 40
    else:  # fin de partie
        token_weight = 60
        mobility_weight = 20
        corner_weight = 20

    # Scores relatifs
    token_score = (
        100 * (player_tokens - opponent_tokens) / (player_tokens + opponent_tokens)
        if player_tokens + opponent_tokens != 0 else 0
    )
    mobility_score = (
        100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
        if player_moves + opponent_moves != 0 else 0
    )
    corner_score = (
        100 * (player_corners - opponent_corners) / (player_corners + opponent_corners)
        if player_corners + opponent_corners != 0 else 0
    )

    final_score = (
        token_weight * token_score +
        mobility_weight * mobility_score +
        corner_weight * corner_score +
        coin_move_bonus*20 +
        capture_bonus*10 +
        dangerous_penalty*15 +
        position_score
    )

    return final_score



# algo minimax
def minimax(grid, player, is_maximizing, depth) :
    opponent = WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
    # ici on est arrivé au bout de la récursivité de notre minmax
    # donc on doit faire appel à notre fonction d'évaluation pour retournen le score
    if depth==0 or game_over(grid)[0] :
        return evaluate_function(grid, player)
    
    moves = get_valid_shots(grid, player)
    if not moves:
        score = minimax(grid, opponent, not is_maximizing, depth-1)
        return score

    # on vérifie si c est le tour de notre IA (autrement dit si c le tour de max)
    if is_maximizing:
        best_score = float("-inf")
        for move in moves:
            row, col = move[:2]
            # jouer provisoirement son coup player pour ensuite traiter les combinaisons possibles des coups de l'adversaire
            grid_copy = grid.copy()
            play_a_shot(grid=grid_copy, player=player, position=(row, col), number_of_tokens=[2,2])
            # appeler recursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter le prochain coup)
            score = minimax(grid_copy, opponent, False, depth-1)
            # mettre à jour le meilleur score
            best_score = max(score ,best_score)
        return best_score
    # dans ce cas c'est le tour du deuxième joueur
    else :
        best_score = float("inf")
        for move in moves:
            row, col = move[:2]
            # jouer provisoirement son coup opponent_player pour ensuite traiter les combinaisons possibles des coups de l'adversaire (IA)
            grid_copy = grid.copy()
            play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
            # appeler recursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter le prochain coup)
            score = minimax(grid_copy, opponent, True, depth-1)
            # mettre à jour le meilleur score
            best_score = min(score, best_score)
        return best_score
    
def minimax_with_alpha_beta_pruning (grid, player, is_maximizing, depth, alpha, beta):
    opponent = WHITE_TOKEN if player == BLACK_TOKEN else BLACK_TOKEN
    
    if depth==0 or game_over(grid)[0]:
        return evaluate_function(grid, player)
    
    moves = get_valid_shots(grid, player)
    
    if not moves:
        score = minimax_with_alpha_beta_pruning(grid, opponent,  not is_maximizing, depth-1, alpha, beta)
        if is_maximizing:
            alpha = max(alpha, score) 
        else:
            beta = min(beta, score)
        return score

    if is_maximizing :
        best_score = float("-inf")
        for move in moves :
            row, col = move[:2]
            grid_copy = grid.copy()
            play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
            score = minimax_with_alpha_beta_pruning(grid_copy, opponent, False, depth-1, alpha, beta)
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    
    else:
        best_score = float("inf")
        for move in moves :
            row, col = move[:2]
            grid_copy = grid.copy()
            play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
            score = minimax_with_alpha_beta_pruning(grid_copy, opponent, True, depth-1, alpha, beta)
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score




def get_best_shot(grid, player, depth, with_pruning):
    # afin de trouver le meilleur coup pour une IA minimax
    best_score = float("-inf")
    best_move = None
    opponent = WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
    
    moves = get_valid_shots(grid, player)
    # s'il n y a pas de coups dés le première itération c'est qu'il n y a plus de coups possibles, donc forcément pas de meilleur coup... :)
    if not moves:
        return None

    for move in moves:
        row, col = move[:2]
        grid_copy = grid.copy()
        play_a_shot(grid_copy, player, position=(row,col), number_of_tokens=[2,2])
        if with_pruning:
            score = minimax_with_alpha_beta_pruning(grid_copy, opponent, False, depth-1, float("-inf"), float("+inf"))
        else:
            score = minimax(grid_copy, opponent, False, depth-1)

        if score > best_score:
            best_score = score
            best_move = move 
    
    return best_move