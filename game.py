import pygame
from Constants import *
import numpy as np


# Met à jour et dessine le plateau de jeu sur la fenêtre Pygame.
# Paramètres :
## WIN : la surface Pygame sur laquelle dessiner.
## grid : une matrice représentant l'état actuel du plateau (valeurs : vide, pion noir ou pion blanc).

def update_checkerboard(WIN, grid):
    # Effacer l'écran avec un fond vert.
    WIN.fill(GREEN)
    # Afficher les compteurs de pions noirs et blancs en haut et en bas.
    WIN.blit(BLACK_TOKENS, (200,0))
    WIN.blit(WHITE_TOKENS, (200,500))
    # Dessiner le cadre du plateau ainsi que les cases individuelles.
    pygame.draw.rect(WIN, BLACK, (200, 0, 400, 100), 4)
    pygame.draw.rect(WIN, BLACK, (200, 500, 400, 100), 4)
    pygame.draw.rect(WIN, BLACK, (200, 100, SQUARE_LENGTH*8, SQUARE_LENGTH*8), 2)
    for row in range (ROWS):
        for col in range (COLS):
            pygame.draw.rect(WIN, BLACK, (200+col*SQUARE_LENGTH, 100+row*SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH), 1)
            #  Dessiner un pion noir ou blanc sur chaque case occupée, selon l'état de la grille.
            if (grid[row,col] != EMPTY) :
                if (grid[row,col] == BLACK_TOKEN) :
                    pygame.draw.circle(WIN, BLACK, (200+(col+.5)*SQUARE_LENGTH,100+(row+.5)*SQUARE_LENGTH), 21)
                else :
                    pygame.draw.circle(WIN, WHITE, (200+(col+.5)*SQUARE_LENGTH,100+(row+.5)*SQUARE_LENGTH), 21)


# Initialise le plateau de jeu pour une nouvelle partie de Reversi.
# Retour :
## grid : une matrice NumPy représentant l'état initial du plateau.

def initialise_game() :
    # Crée une grille 8x8 remplie de zéros (cases vides), puis place les 4 pions initiaux au centre
    ## Blanc en (3,3) et (4,4)
    ## Noir en (3,4) et (4,3)
    grid = np.zeros((8,8))
    grid[3,3] = WHITE_TOKEN
    grid[3,4] = BLACK_TOKEN
    grid[4,3] = BLACK_TOKEN
    grid[4,4] = WHITE_TOKEN
    return grid


# Définition des différentes règles du jeu du REVERSI
# grid est la grille du jeu, player est soit le joueur aux jetons Blancs, soit le joueur aux jetons noirs



# Vérifie si une case donnée a au moins un pion voisin (dans les 8 directions autour).
# Cette vérification est utile pour optimiser la détection des coups valides en limitant les zones à tester.
#
# Paramètres :
## grid : matrice représentant le plateau de jeu.
## position : tuple (ligne, colonne) de la case à tester.
#
# Retour :
# - True si au moins une case adjacente contient un pion (noir ou blanc), sinon False.

def has_neighbour_token(grid, position) :
    y, x = position
    for direction in DIRECTIONS:
        dy, dx = direction
        j, i = y+dy, x+dx
        if 0<=j<8 and 0<=i<8 and grid[j][i] != EMPTY :
            return True
    return False




# Détermine les directions valides dans lesquelles un pion peut être retourné si le joueur joue à la position donnée.
# Une direction est considérée valide si elle commence par un pion adverse, suivi d’au moins un pion du joueur sans case vide entre les deux.
# Ne teste que les directions où la case a un voisin, pour optimiser la recherche.
# Paramètres :
## grid : matrice représentant le plateau de jeu.
## player : le joueur courant (BLACK_TOKEN ou WHITE_TOKEN).
## position : tuple (ligne, colonne) représentant la position du coup potentiel.
# Retour :
## Liste des directions (tuples dy, dx) valides dans lesquelles le coup est légal.

def find_valid_directions(grid, player, position) :
    if not has_neighbour_token(grid, position):
        return []
    opponent_player = WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
    y, x = position
    directions = []
    for direction in DIRECTIONS:
        dy, dx = direction
        j, i = y+dy, x+dx
        player_found = False
        if 0<=i<8 and 0<=j<8 and grid[j][i] == opponent_player :
            while 0<=j<8 and 0<=i<8 and grid[j][i]!=EMPTY and not player_found :
                if grid[j][i]==player :
                    player_found = True
                j, i = j+dy, i+dx
            if player_found:
                directions.append(direction)
    return directions




# Vérifie si un coup est valide pour le joueur à la position donnée.
# Un coup est valide s’il permet de retourner au moins un pion adverse dans une ou plusieurs directions.
# Paramètres :
## grid : matrice représentant le plateau de jeu.
## player : le joueur courant.
## position : tuple (ligne, colonne) représentant la position du coup.
# Retour :
## True si au moins une direction est valide, sinon False.

def is_valid_shot(grid, player, position):
    directions = find_valid_directions(grid, player, position)
    return len(directions) != 0



# Identifie les pions à retourner si le joueur joue à la position donnée.
# Pour chaque direction valide, la fonction suit la ligne jusqu'à rencontrer un pion du joueur.
# Tous les pions adverses entre le point de départ et ce pion final sont à retourner.
# Paramètres :
## grid : matrice représentant le plateau de jeu.
## player : le joueur courant.
## position : tuple (ligne, colonne) représentant la position du coup.
# Retour :
## Liste des positions (tuples) des pions à retourner, y compris la position jouée si le coup est valide.

def tokens_to_invert(grid, player, position) :
    valid_directions = find_valid_directions(grid=grid, position=position, player=player)
    opponent = BLACK_TOKEN if player==WHITE_TOKEN else WHITE_TOKEN
    y, x = position
    tokens_to_invert = []
    for direction in valid_directions :
        dy, dx = direction
        last_player_token_position = +1
        cpt = 1
        j, i =  y+dy, x+dx 
        while 0<=i<8 and 0<=j<8 and grid[j][i] != EMPTY:
            if grid[j][i]==player:
                last_player_token_position = cpt
            j, i = j+dy, i+dx
            cpt+=1
        j, i =  y+dy, x+dx 
        cpt=1
        while cpt<last_player_token_position:
            if grid[j][i] == opponent:
                tokens_to_invert.append((j,i))
            j, i, cpt = j+dy, i+dx, cpt+1
    if tokens_to_invert!=[]:
        tokens_to_invert.append(position)
    return tokens_to_invert



# CETTE FONCTION Joue un coup sur le plateau pour le joueur donné à la position spécifiée.
# Si le coup est valide on retourne les pions adverses affectés et on place le pion du joueur, on Met ensuite à jour le comptage des pions noirs et blancs sur la grille.
#
# Paramètres :
## grid : matrice représentant le plateau de jeu.
## player : le joueur courant.
## position : tuple (ligne, colonne) où le joueur souhaite jouer.
## number_of_tokens (optionnel) : tuple (black, white) à renvoyer si le coup est invalide (sinon retourne (0, 0) par défaut).
# Retour :
## - Tuple (nb_pions_noirs, nb_pions_blancs) après le coup joué.

def play_a_shot(grid, player, position, number_of_tokens=None):
    tokens = tokens_to_invert(grid, player, position)
    if not tokens:
        return number_of_tokens if number_of_tokens else (0, 0)  # ou None

    for y, x in tokens:
        grid[y][x] = player  # retourne les pions

    y, x = position
    grid[y][x] = player  # place le pion du joueur

    # Recalcul immédiat à partir de la grille
    black = sum(1 for r in range(ROWS) for c in range(COLS) if grid[r, c] == BLACK_TOKEN)
    white = sum(1 for r in range(ROWS) for c in range(COLS) if grid[r, c] == WHITE_TOKEN)

    return(black, white)



# Gère les coordonnées d’un clic utilisateur sur la grille.
# Vérifie si le clic est dans les limites du plateau de jeu, puis convertit les coordonnées en indices de case (ligne, colonne).
# Si le clic est en dehors du plateau, retourne (-1, -1).
#
# Paramètres :
## y : position verticale du clic (en pixels).
## x : position horizontale du clic (en pixels).
#
# Retour :
## Tuple (ligne, colonne) de la case cliquée, ou (-1, -1) si le clic est hors zone.

def handle_click(y, x) :
    if 100<=y<100+HEIGHT and 200<=x<200+WIDTH:
        return ((y-100)//SQUARE_LENGTH , (x-200)//SQUARE_LENGTH)
    else :
        return (-1,-1)
    



def update_timers (WIN, BLACK_TOKEN_TIMER, WHITE_TOKEN_TIMER, player, NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN) :
    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(BACKGROUND, (600,0))
    font = pygame.font.Font(None, 32)  # Police par défaut, taille 36
    black_timer_text = font.render(f"x{NUMBER_OF_BLACK_TOKEN}   {BLACK_TOKEN_TIMER//60:02}:{BLACK_TOKEN_TIMER%60:02}", True, (0, 0, 0))
    white_timer_text = font.render(f"{WHITE_TOKEN_TIMER//60:02}:{WHITE_TOKEN_TIMER%60:02}   x{NUMBER_OF_WHITE_TOKEN}", True, (0, 0, 0))
    WIN.blit(black_timer_text, (38, 50))
    WIN.blit(CHRONOMETER, (150,38))
    pygame.draw.circle(WIN, BLACK, (20,60), 16)
    WIN.blit(white_timer_text, (643, 530))
    WIN.blit(CHRONOMETER, (600,518))
    pygame.draw.circle(WIN, WHITE, (780,540), 16)
    pygame.draw.rect(WIN, BLACK, (1,39, 198, 42), 1, border_radius=15)
    pygame.draw.rect(WIN, BLACK, (601,519, 198, 42), 1, border_radius=15)
    if player==BLACK_TOKEN:
        pygame.draw.rect(WIN, RED, (2,40, 197, 41), 2,  border_radius=15)
    else :
        pygame.draw.rect(WIN, RED, (602,520, 197, 41), 2, border_radius=15)



# Vérifie si la partie est terminée. La partie est considérée comme terminée si aucun coup valide n'est possible pour les deux joueurs.
# Si un joueur a encore des coups valides, la partie continue. Si la grille est pleine ou que les deux joueurs ne peuvent plus jouer, la partie est terminée.
# Paramètres :
## grid : matrice représentant l'état actuel du plateau de jeu.
# Retour :
## Tuple (True/False, nb_pions_noirs, nb_pions_blancs) avec:
### True si la partie est terminée, False sinon.
### Le nombre de pions noirs et blancs sur le plateau si la partie est terminée pour determiner directement le vainqueur

def game_over(grid) :
    black_tokens, white_tokens = 0, 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == EMPTY:
                if (len(tokens_to_invert(grid, WHITE_TOKEN, (row, col))) > 0 or
                    len(tokens_to_invert(grid, BLACK_TOKEN, (row, col))) > 0):
                    return (False, 0, 0)  # Partie non terminée

            elif grid[row][col] == WHITE_TOKEN:
                white_tokens += 1
            elif grid[row][col] == BLACK_TOKEN:
                black_tokens += 1
    return (True, black_tokens, white_tokens)




# Vérifie si le joueur spécifié a gagné la partie, la fonction utilise `game_over` pour vérifier si la partie est terminée.
# Ensuite, elle compare le nombre de pions du joueur avec celui de l'adversaire pour déterminer le vainqueur.
# Paramètres :
## grid : matrice représentant l'état actuel du plateau de jeu.
## player : le joueur courant (BLACK_TOKEN ou WHITE_TOKEN).
# Retour :
## boolean True si le joueur a gagné, False sinon.

def game_won(grid, player):
    gameover, black_tokens, white_tokens = game_over(grid)
    if not gameover :
        return False
    elif player == BLACK_TOKEN:
        return black_tokens > white_tokens
    else:
        return white_tokens > black_tokens




# Récupère tous les coups valides pour le joueur spécifié. Un coup est valide si la case est vide et permet de retourner au moins un pion adverse.
# Paramètres :
## grid : matrice représentant l'état actuel du plateau de jeu.
## player : le joueur courant (BLACK_TOKEN ou WHITE_TOKEN).
# Retour :
## Liste de tuples (y, x, score) où (y, x) est la position du coup et score est le nombre de pions à retourner.

def get_valid_shots(grid, player):
    valid_shots = []
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row][col] == EMPTY:
                score = len(tokens_to_invert(grid,player, (row,col)))
                if score>0:
                    valid_shots.append((row, col, score-1))
    # on retourne valid_shots sous forme d'une liste de tuples (y,x,s) où (y,x) est la position de la case correspondant au coup dans la grille, et s le score de ce coup
    return valid_shots



def log_token_counts(grid):
    black = sum(1 for row in range(ROWS) for col in range(COLS) if grid[row, col] == BLACK_TOKEN)
    white = sum(1 for row in range(ROWS) for col in range(COLS) if grid[row, col] == WHITE_TOKEN)
    print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
