# Dans ce fichier, on implémente l'intelligence artificielle pour le jeu du Reversi

from Constants import *
from game import game_won, game_lose, get_valid_shots


# fonction d'évaluation de chaque état de notre jeu, elle donne estimation sur l'état du jeu
def evaluate_function(grid, player):
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
    
    final_score = (20*token_score) + (60*mobility_score) + (20*corner_score)

    return final_score



# algo minimax
def minimax (grid, player, is_maximizing, depth) :
    # ici on est arrivé au bout de la récursivité de notre minmax
    #  donc on doit faire appel à notre fonction d'évaluation pour retournen le score
    if game_won(grid, player):
        return float("inf")
    elif game_lose(grid, player):
        return float("-inf")
    elif depth==0:
        return evaluate_function(grid, player)
    
    # on vérifie si c est le tour de notre IA (autrement dit si c le tour de max)
    if is_maximizing:
        best_score = float("-inf")
        for move in get_valid_shots(grid, player):
            row, col = move[:2]
            # jouer provisoirement son coup player pour ensuite traiter les combinaisons possibles des coups de l'adversaire
            grid[row,col] = player
            # appeler recursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter le prochain coup)
            score = minimax(grid, player, False, depth-1)
            # supprimer le coup joué provisoirement pour revenir vers l'état de départ
            grid[row, col] = EMPTY
            # mettre à jour le meilleur score
            best_score = max(score ,best_score)
        return best_score
    # dans ce cas c'est le tour du deuxième joueur
    else :
        best_score = float("inf")
        opponent_player = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
        for move in get_valid_shots(grid, opponent_player):
            row, col = move[:2]
            # jouer provisoirement son coup opponent_player pour ensuite traiter les combinaisons possibles des coups de l'adversaire (IA)
            grid[row,col] = opponent_player
            # appeler recursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter le prochain coup)
            score = minimax(grid, player, True, depth-1)
            # supprimer le coup joué provisoirement pour revenir vers l'état de départ
            grid[row, col] = EMPTY
            # mettre à jour le meilleur score
            best_score = min(score, best_score)
        return best_score
    
def get_best_shot(grid, player, depth):
    # afin de trouver le meilleur coup pour une IA minimax
    best_score = float("-inf")
    best_move = None

    for move in get_valid_shots(grid, player):
        row, col = move[:2]
        grid[row, col] = player
        score = minimax(grid, player, False, depth-1)
        grid[row, col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move    
    
    return best_move