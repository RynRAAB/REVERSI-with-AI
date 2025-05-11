from Constants import *
from game import get_valid_shots



# fonction d'évaluation (version initiale) pour le jeu Reversi.
# flle fournit une estimation de la qualité d'une position pour un joueur donné.
# fien que cette version ne soit pas très optimisée, elle constitue une bonne base fonctionnelle.
# Trois critères principaux sont pris en compte dans cette évaluation :
## Différence de pions :
###   Mesure l'écart entre le nombre de pions du joueur et celui de l'adversaire.
###   Ce critère est particulièrement pertinent en fin de partie, car le joueur avec le plus de pions l'emporte.
## Mobilité :
###    Correspond au nombre de coups légaux disponibles pour chaque joueur.
###    Une bonne mobilité permet plus de flexibilité et d'options stratégiques.
###    Ce facteur est crucial surtout en début et milieu de partie.
## Contrôle des coins :
###   Les coins du plateau sont des positions stratégiques très fortes.
###   Un joueur qui contrôle les coins a un net avantage, car ces cases ne peuvent plus être retournées.
# Paramètres :
## grid : représente l'état actuel du plateau de jeu.
## player : le joueur pour lequel on évalue la position 
# Retourne :
##  Une valeur numérique estimant la qualité de la position pour le joueur donné.

def evaluate_function_v1(grid, player):
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    # on définit les coins de notre plateau (4 coins)
    corners = [(0,0), (ROWS-1,0), (0,COLS-1), (ROWS-1,COLS-1)]
    
    # nombre de pions: on compte le nombre de pions pour chaque joueur
    player_tokens, opponent_tokens = 0, 0
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row,col] != EMPTY:
                if grid[row,col] == player :
                    player_tokens += 1
                else:
                    opponent_tokens += 1

    # mobilité.. get_valid_shots est une fonction permettant d'obtenir tous les coups possibles qu'un joueur (player) puisse jouer sur un plateau donné (grid) 
    player_moves, opponent_moves = 0, 0
    player_moves = len(get_valid_shots(grid=grid, player=player))
    opponent_moves = len(get_valid_shots(grid=grid, player=opponent))

    # coins.. on compte le nombre de coins que chaque joueur a en possession
    player_corners, opponent_corners = 0, 0
    for y, x in corners :
        if grid[y,x] == player:
            player_corners += 1
        elif grid[y,x] == opponent:
            opponent_corners += 1

    # Calcul des différents scores (pions, mobilité, coins),
    # avec une normalisation des valeurs sous forme de pourcentages (/100).
    # Cela permet de rendre les différentes composantes comparables et d'appliquer des poids équilibrés à chacun des critères. 
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
    # Le but ensuite est de combiner ces scores de manière pondérée pour obtenir une évaluation globale cohérente de la position.
    # donc on multiplie chaque score par l'effet (l'importance) qu'il puisse avoir sur notre plateau
    # token_score c'est 40%, mobility_score a 20%, et corner_score ayant 40%
    final_score = (40*token_score) + (20*mobility_score) + (40*corner_score)

    # on retourne le score final qui sera compris dans l'intervalle [-10000, 10000]
    return final_score


# cette fonction dit si oui ou non un move donné va prendre un coin
def is_corner(move, board_size):
    return move in [(0, 0), (0, board_size - 1), (board_size - 1, 0), (board_size - 1, board_size - 1)]




# cette fonction d'évaluation correspond à une deuxième version améliorée de la fonction précédente
# afin d'améliorer le rendement de la première heuristique, on a rajouté 3 nouveaux poids à prendre en compte durant l'évaluation, ces poids comprennent :
## les pions dangereux : les pions disent "dangereux" sont près des coins, les avoir est souvent désavantageux, car ça donne plus de chances à l'adversaire de prendre un coin, si un joueur quelconque possède un pion dangereux on doit baisser son score d'une manière considérable ce qui empêcherait le joueur le prendre ce pion
## position_score : un score calculé à travers des valeurs stratégique des positions occupées (via une table de pondération) 
## corner_bonus : on a constaté que dans la plupart des cas, dès qu'un joueur est en possession d'un coin, il lui devient plus facile de mener la partie vers la victoire, donc on a décidé de rajouter un bonus pour un joueur ayant un coin, cela motive notre IA à prendre les coins sans hésitation dès que possible

def evaluate_function_v2(grid, player):
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    corners = [(0, 0), (ROWS - 1, 0), (0, COLS - 1), (ROWS - 1, COLS - 1)]

    # Tokens control 
    player_tokens, opponent_tokens = 0, 0
    for row in range(ROWS):
        for col in range(COLS):
            token = grid[row, col]
            if token == player:
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
    # ce tableau liste toutes les positions dangereuses dans un plateau, ces positions correspondent aux trois cases voisines de chaque case coin
    # exemple :    
    # danger1 danger2
    #  coin3  danger3
    dangerous_positions = [
        (0, 1), (1, 0), (1, 1),
        (0, COLS - 2), (1, COLS - 1), (1, COLS - 2),
        (ROWS - 2, 0), (ROWS - 1, 1), (ROWS - 2, 1),
        (ROWS - 2, COLS - 1), (ROWS - 1, COLS - 2), (ROWS - 2, COLS - 2)
    ]
    dangerous_count = sum(1 for y, x in dangerous_positions if grid[y, x] == player)
    # on normalise en un pourcentage /100
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
    corner_bonus = 100 * player_corners

    # on combine tous nos scores pour avoir un score final
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
