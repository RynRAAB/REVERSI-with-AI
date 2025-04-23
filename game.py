import pygame
from Constants import *
import numpy as np

def update_checkerboard(WIN, grid):
    WIN.fill(GREEN)
    WIN.blit(BLACK_TOKENS, (200,0))
    WIN.blit(WHITE_TOKENS, (200,500))

    pygame.draw.rect(WIN, BLACK, (200, 0, 400, 100), 4)
    pygame.draw.rect(WIN, BLACK, (200, 500, 400, 100), 4)
    pygame.draw.rect(WIN, BLACK, (200, 100, SQUARE_LENGTH*8, SQUARE_LENGTH*8), 2)
    for row in range (ROWS):
        for col in range (COLS):
            pygame.draw.rect(WIN, BLACK, (200+col*SQUARE_LENGTH, 100+row*SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH), 1)
            if (grid[row,col] != EMPTY) :
                if (grid[row,col] == BLACK_TOKEN) :
                    pygame.draw.circle(WIN, BLACK, (200+(col+.5)*SQUARE_LENGTH,100+(row+.5)*SQUARE_LENGTH), 21)
                else :
                    pygame.draw.circle(WIN, WHITE, (200+(col+.5)*SQUARE_LENGTH,100+(row+.5)*SQUARE_LENGTH), 21)


def initialise_game() :
    grid = np.zeros((8,8))
    grid[3,3] = WHITE_TOKEN
    grid[3,4] = BLACK_TOKEN
    grid[4,3] = BLACK_TOKEN
    grid[4,4] = WHITE_TOKEN
    return grid

# Définition des différentes règles du jeu du REVERSI
# grid est la grille du jeu, player est soit le joueur aux jetons Blancs, soit le joueur aux jetons noirs

# Cette fonction vérifie si à une position (y,x) on retrouve un jeton voisin ou pas
def has_neighbour_token(grid, position) :
    y, x = position
    for direction in DIRECTIONS:
        dy, dx = direction
        j, i = y+dy, x+dx
        if 0<=j<8 and 0<=i<8 and grid[j,i] != EMPTY :
            return True
    return False       


# Retourne les directions possibles...
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
        if 0<=i<8 and 0<=j<8 and grid[j,i] == opponent_player :
            while 0<=j<8 and 0<=i<8 and grid[j,i]!=EMPTY and not player_found :
                if grid[j,i]==player :
                    player_found = True
                j, i = j+dy, i+dx
            if player_found:
                directions.append(direction)
    return directions


# Cette fonction vérifie simplement si un coup est possible ou pas
def is_valid_shot(grid, player, position):
    directions = find_valid_directions(grid, player, position)
    return len(directions) != 0



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
        while 0<=i<8 and 0<=j<8 and grid[j,i] != EMPTY:
            if grid[j,i]==player:
                last_player_token_position = cpt
            j, i = j+dy, i+dx
            cpt+=1
        j, i =  y+dy, x+dx 
        cpt=1
        while cpt<last_player_token_position:
            if grid[j,i] == opponent:
                tokens_to_invert.append((j,i))
            j, i, cpt = j+dy, i+dx, cpt+1
    if tokens_to_invert!=[]:
        tokens_to_invert.append(position)
    return tokens_to_invert

def play_a_shot(grid, player, position, number_of_tokens):
    NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
    tokens = tokens_to_invert(grid, player, position)
    if tokens == [] :
        return number_of_tokens
    for token in tokens :
        y, x = token
        grid[y,x] = BLACK_TOKEN if player==BLACK_TOKEN else WHITE_TOKEN
        if player==BLACK_TOKEN :
            NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = NUMBER_OF_BLACK_TOKEN+1, NUMBER_OF_WHITE_TOKEN-1
        else : 
            NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = NUMBER_OF_BLACK_TOKEN-1, NUMBER_OF_WHITE_TOKEN+1
    if player==BLACK_TOKEN :
        NUMBER_OF_WHITE_TOKEN += 1
    else:
        NUMBER_OF_BLACK_TOKEN += 1    
    return (NUMBER_OF_BLACK_TOKEN,NUMBER_OF_WHITE_TOKEN)

# Cette fonction retourne les coordonnées de la case de la grille correspondante à un clic de souris
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

def game_won(grid, player, number_of_player_tokens, number_of_opponent_player_tokens):
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row, col] == EMPTY :
                if len(tokens_to_invert(grid, player, (row,col))) > 0 :
                    return False
    return number_of_player_tokens > number_of_opponent_player_tokens

def game_lose(grid, player, number_of_player_tokens, number_of_opponent_player_tokens):
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row, col] == EMPTY :
                if len(tokens_to_invert(grid, player, (row,col))) > 0 :
                    return False
    return number_of_player_tokens < number_of_opponent_player_tokens

def get_valid_shots(grid, player):
    valid_shots = []
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row][col] == EMPTY:
                score = len(tokens_to_invert(grid,player, (row,col)))
                if score>0:
                    valid_shots.append((row, col, score-1))
    # on retourne valid_shots  sous forme de tuples (y,x,s) où (y,x) est la position de la case correspondant au coup dans la grille, et s le score de ce coup
    return valid_shots