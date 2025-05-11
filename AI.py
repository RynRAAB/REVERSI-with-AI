# Dans ce fichier, on implémente l'intelligence artificielle pour le jeu du Reversi
from Constants import *
from game import game_over, get_valid_shots, play_a_shot
from evaluation_functions import evaluate_function_v2




# Implémentation pure de l'algorithme Minimax en une fonction récursive ayant 4 paramètres :
# grid: tableau numpy double dimensions où est stocké la grille éffective du jeu 
# player:  stocke le joueur actuel qui fait appel à min ou à max (selon l'appel), le joueur peut être soit BLACK_TOKEN ou WHITE_TOKEN
# is_maximizing: boolean mis à vrai quand c'est le tour de max (celui à la racine de cet appel, celui qui cherche à gagner), et mis à false quand c'est le tour de min (adversaire)  
# depth: stocke la profondeur d'analyse de notre MinMax, dans notre jeu on utilise 3 profondeurs principales (depth=1 pour le niveau facile, depth=3 pour le niveau moyen, et depth=5 pour le niveau difficile)

def minimax(grid, player, is_maximizing, depth) :
    # opponent stocke le joueur adverse
    opponent = WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
    
    # si on atteint la profondeur demandée ou si c'est fin de jeu
    if depth==0 or game_over(grid)[0] :
        # on fait appel à notre fonction d'évaluation pour retourner le score, ce score correspond à une estimation sur l'état actuel de la grille, si c'est plutôt un coup favorisant ou défavorisant pour max
        return evaluate_function_v2(grid, player if is_maximizing else opponent)
    
    # on stocke dans moves tous les coups possibles pour notre joueur actuel sur la grille grid
    moves = get_valid_shots(grid, player)

    # si le joueur actuel n'a aucun coup possible (et que c'est pas fin de jeu)
    if not moves:
        # on passe son tour car il a 0 coup possible
        score = minimax(grid, opponent, not is_maximizing, depth-1)
        return score

    # ici c'est à max de jouer, donc il doit chercher à piocher le meilleur coup où il estime gagner le plus de points parmi les coups possibles
    if is_maximizing:
        #on initialise le best_score à -INF, on traite tous les coups possibles un par un, et on essaie de garder le meilleur coup (celui avec le score le plus haut) 
        best_score = float("-inf")

        # pour chaque coup possible pour max...
        for move in moves:
            # on récupére le move en récupérant ses coordonnées dans la grilee
            row, col = move[:2]
            # on fait une copie de la grille actuelle sur laquelle on va ensuite simuler notre coup (pour éviter de perturber la grille effective du jeu)
            grid_copy = grid.copy()
            # jouer provisoirement son coup max sur la copie de la grille pour ensuite traiter les combinaisons possibles des coups de l'adversaire
            play_a_shot(grid=grid_copy, player=player, position=(row, col), number_of_tokens=[2,2])
            # appeler récursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter les combinaisons possibles sur la prochaine profondeur)
            score = minimax(grid_copy, opponent, False, depth - 1)
            # mettre à jour le meilleur score en gardant le plus grand (max cherche toujours à récupérer le meilleur coup)
            best_score = max(score,best_score)
        # on retourne le meilleur score que max puisse avoir à cette profondeur
        return best_score
    # ici c'est à min de jouer, donc il doit chercher à piocher le meilleur coup pour lui (qui correspond au pire coup de min)
    else :
        #on initialise le best_score à +INF, on traite tous les coups possibles un par un, et on essaie de garder le meilleur coup (celui avec le score le plus bas) 
        best_score = float("inf")

        # pour chaque coup possible pour min...
        for move in moves:
            # on récupére le move en récupérant ses coordonnées dans la grilee
            row, col = move[:2]
            # on fait une copie de la grille actuelle sur laquelle on va ensuite simuler notre coup (pour éviter de perturber la grille effective du jeu)
            grid_copy = grid.copy()
            # jouer provisoirement son coup min sur la copie de la grille pour ensuite traiter les combinaisons des coup possibles pour max
            play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
            # appeler récursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter les combinaisons possibles sur la prochaine profondeur)
            score = minimax(grid_copy, opponent, True, depth - 1)
            # mettre à jour le meilleur score en gardant le plus petit (min cherche à minimiser les coups de max, donc il choisit le coup où max gagne le moins ou du moins le coup ou max perd carrément)
            best_score = min(score, best_score)
        # on retourne le meilleur score que min puisse avoir à cette profondeur
        return best_score
    


# Implémentation de l'algorithme Minimax avec élagage alpha beta en une fonction récursive ayant 6 paramètres :
# grid: tableau numpy double dimensions où est stocké la grille éffective du jeu 
# player:  stocke le joueur actuel qui fait appel à min ou à max (selon l'appel), le joueur peut être soit BLACK_TOKEN ou WHITE_TOKEN
# is_maximizing: boolean mis à vrai quand c'est le tour de max (celui à la racine de cet appel, celui qui cherche à gagner), et mis à false quand c'est le tour de min (adversaire)  
# depth: stocke la profondeur d'analyse de notre MinMax, dans notre jeu on utilise 3 profondeurs principales (depth=1 pour le niveau facile, depth=3 pour le niveau moyen, et depth=5 pour le niveau difficile)
# alpha :  correspond à la meilleure valeur trouvée jusqu’à présent pour le joueur Max ,le joueur qui essaie de maximiser le score
# beta : correspond à la meilleure valeur trouvée jusqu’à présent pour le joueur Min, le joueur qui essaie de minimiser le score

def minimax_with_alpha_beta_pruning (grid, player, is_maximizing, depth, alpha, beta):
    # on stocke le joueur adversaire dans opponent 
    opponent = WHITE_TOKEN if player == BLACK_TOKEN else BLACK_TOKEN
    # si profondeur demandée atteinte ou si finn de jeu
    if depth==0 or game_over(grid)[0]:
        # on appelle notre fonction d'évaluation pour évaluer et donner un score à létat actuel de la grille (tout en prenant en compte que le joueur qui cherche à vaincre est max et non pas min)
        # max correspond à player si is_maximizing==True et à opponent sinon
        return evaluate_function_v2(grid, player if is_maximizing else opponent)
    
    # on stocke dans moves tous les coups possibles pour notre joueur actuel sur la grille grid
    moves = get_valid_shots(grid, player)
    
    # s'il y a 0 coup possible, on passe son tour et on donne la main à l'adversaire de jouer (tout en prenant en compte les MAJ des alpha beta)
    if not moves:
        score = minimax_with_alpha_beta_pruning(grid, opponent,  not is_maximizing, depth-1, alpha, beta)
        # si c'est max qui joue on check s'il y a une MAJ à faire sur alpha
        if is_maximizing:
            alpha = max(alpha, score) 
        # si c'est min qui joue on check s'il y a une MAJ à faire sur beta
        else:
            beta = min(beta, score)
        return score
    
    # dans ce cas c'est max qui analyse
    if is_maximizing :
        #on initialise le best_score à -INF, on traite tous les coups possibles un par un, et on essaie de garder le meilleur coup (celui avec le score le plus haut) 
        best_score = float("-inf")

        # pour chaque coup possible pour max...
        for move in moves :
            # on récupére le move en récupérant ses coordonnées dans la grilee
            row, col = move[:2]
            # on fait une copie de la grille actuelle sur laquelle on va ensuite simuler notre coup (pour éviter de perturber la grille effective du jeu)
            grid_copy = grid.copy()
            # jouer provisoirement son coup max sur la copie de la grille pour ensuite traiter les combinaisons possibles des coups de l'adversaire
            play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
            # appeler récursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter les combinaisons possibles sur la prochaine profondeur)
            score = minimax_with_alpha_beta_pruning(grid_copy, opponent, False, depth-1, alpha, beta)
            # mettre à jour le meilleur score en gardant le plus petit (min cherche à minimiser les coups de max, donc il choisit le coup où max gagne le moins ou du moins le coup ou max perd carrément)
            best_score = max(score, best_score)
            # on met à jour alpha (le meilleur score de max trouvé jusqu'à présent)
            alpha = max(alpha, best_score)
            # si la valeur cet enfant est ≥ beta, on peut arrêter (élaguer) car Min supérieur ne choisira jamais ce chemin
            if beta <= alpha:
                break
        # on retourne le meilleur score que max puisse avoir à cette profondeur
        return best_score
    # dans ce cas c'est min qui analyse
    else:
        #on initialise le best_score à +INF, on traite tous les coups possibles un par un, et on essaie de garder le meilleur coup (celui avec le score le plus bas) 
        best_score = float("inf")

        # pour chaque coup possible pour min...
        for move in moves :
            # on récupére le move en récupérant ses coordonnées dans la grilee
            row, col = move[:2]
            # on fait une copie de la grille actuelle sur laquelle on va ensuite simuler notre coup (pour éviter de perturber la grille effective du jeu)
            grid_copy = grid.copy()
            # jouer provisoirement son coup min sur la copie de la grille pour ensuite traiter les combinaisons des coup possibles pour max
            play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
            # appeler récursivement le minimax sur le prochain coup avec une profondeur en moins (pour traiter les combinaisons possibles sur la prochaine profondeur)           
            score = minimax_with_alpha_beta_pruning(grid_copy, opponent, True, depth-1, alpha, beta)
            # mettre à jour le meilleur score en gardant le plus petit (min cherche à minimiser les coups de max, donc il choisit le coup où max gagne le moins ou du moins le coup ou max perd carrément)
            best_score = min(score, best_score)
            #on met à jour beta (le meilleur score de min trouvé jusqu'à présent)
            beta = min(beta, best_score)
            # si la valeur cet enfant est ≤ alpha, on peut arrêter (élaguer) car Max supérieur ne choisira jamais ce chemin.
            if beta <= alpha:
                break
        # on retourne le meilleur score que min puisse avoir à cette profondeur
        return best_score




# cette fonction permet d'appeler notre IA (MinMax avec ou sans élagage) pour nous procurer le meilleur coup à jouer, elle a comme paramètre
# grid : correspond à la grille du jeu
# player : correspond au joueur (BLACK_TOKEN | WHITE_TOKEN) cherchant à avoir le meilleur coup
# depth : stocke la profondeur de recherche de notre MinMax, plus elle est haute plus notre IA devient performante, et plus elle prend du temps à répondre
# with_pruning : boolean qui décide si oui ou non on va utiliser l'élagage alpha-beta dans notre recherche (with_pruning==True => minmax_with_pruning sinon => minmax classique)

def get_best_shot(grid, player, depth, with_pruning):
    # le principe de cette fonction est de simuler la première itération (depth=1) en tant que max, afin de garder en mémoire le meilleur coup pour max (en gardant le coup ayant le meilleur score)
    # ici c'est max qui joue, donc on initialise notre meilleur score à -INF (valeur triviale plus petite que tout autre score possible), et on initialise notre meilleur coup à null
    best_score = float("-inf")
    best_move = None
    # on stocke l'adversaire min dans opponent 
    opponent = WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
    # on stocke dans moves tous les coups possibles pour max sur la grille grid
    moves = get_valid_shots(grid, player)
    # s'il n y a pas de coups possible dés la première itération c'est qu'il n y a plus de coups possibles pour max, donc forcément pas de meilleur coup... :)
    if not moves:
        return None
    # pour chaque coup possible pour max...
    for move in moves:
        # on récupère la position du coup (en récupérant ses coordonnées row et col dans la grille)
        row, col = move[:2]
        # on fait une copie de la grille actuelle sur laquelle on va ensuite simuler notre coup (pour éviter de perturber la grille effective du jeu)
        grid_copy = grid.copy()
        # on simule notre coup max sur la copie de la grille pour ensuite traiter les combinaisons des coup possibles pour min
        play_a_shot(grid_copy, player, position=(row,col), number_of_tokens=[2,2])
        # on fait appel à min avec ou sans élagage selon le paramètre with_pruning (tout en réduisant le depth) 
        if with_pruning:
            score = minimax_with_alpha_beta_pruning(grid_copy, opponent, False, depth-1, float("-inf"), float("+inf"))
        else:
            score = minimax(grid_copy, opponent, False, depth-1)
        # une fois l'analyse fait sur le coup courant, on vérifie si c'est un meilleur coup pour max comparé aux coups précédents déjà analysés, si c'est le cas on met à jour les deux vars (best_score et best_move)
        if score > best_score:
            best_score = score
            best_move = move
        # DEBUG
        print(f"[EVAL] move={move[:2]} | score={score:.2f}")
    # DEBUG
    print(f"[CHOIX] Coup {(row, col)} → score = {score:.2f}")
    # on retourne le meilleur coup trouvé par notre IA
    return best_move