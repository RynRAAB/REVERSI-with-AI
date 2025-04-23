# Dans ce fichier, on implémente l'intelligence artificielle pour le jeu du Reversi

from Constants import *
from game import game_won, game_lose, get_valid_shots


# fonction d'évaluation de chaque état de notre jeu, elle donne estimation sur l'état du jeu
def evaluate_function(grid):
    pass


# algo minimax
def minimax (grid, player, is_maximizing, depth, number_of_player_tokens, number_of_opponent_player_tokens) :
    # ici on est arrivé au bout de la récursivité de notre minmax
    #  donc on doit faire appel à notre fonction d'évaluation pour retournen le score
    if game_won(grid, player, number_of_player_tokens, number_of_opponent_player_tokens):
        return 1
    elif game_lose(grid, player, number_of_player_tokens, number_of_opponent_player_tokens):
        return -1
    elif depth==0:
        return evaluate_function(grid)
    
    # on vérifie si c est le tour de notre IA (autrement dit si c le tour de max)
    if is_maximizing:
        best_score = float("-inf")
        for move in get_valid_shots(grid, player):
            row, col, score = move
            # jouer provisoirement son coup player pour ensuite traiter les combinaisons possibles des coups de l'adversaire
            grid[row,col] = player
            # appeler recursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter le prochain coup)
            score = minimax(grid, player, False, depth-1, number_of_player_tokens+score+1, number_of_opponent_player_tokens-score)
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
            row, col, score = move
            # jouer provisoirement son coup opponent_player pour ensuite traiter les combinaisons possibles des coups de l'adversaire (IA)
            grid[row,col] = opponent_player
            # appeler recursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter le prochain coup)
            score = minimax(grid, player, True, depth-1, number_of_player_tokens-score, number_of_opponent_player_tokens+score+1)
            # supprimer le coup joué provisoirement pour revenir vers l'état de départ
            grid[row, col] = EMPTY
            # mettre à jour le meilleur score
            best_score = min(score, best_score)
        return best_score
    
def get_best_shot(grid, player, depth, number_of_player_tokens, number_of_opponent_player_tokens):
    # afin de trouver le meilleur coup pour une IA minimax
    best_score = float("-inf")
    best_move = None

    for move in get_valid_shots(grid, player):
        row, col, score = move
        grid[row, col] = player
        score = minimax(grid, player, False, depth-1, number_of_player_tokens, number_of_opponent_player_tokens)
        grid[row, col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move