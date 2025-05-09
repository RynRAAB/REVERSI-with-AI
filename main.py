# ce fichier main.py contient la boucle du jeu

import pygame
from Constants import *
from game import *
from AI import *

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Reversi")

running = True
clock = pygame.time.Clock()
grid = initialise_game()
player= WHITE_TOKEN
update_checkerboard(window, grid)

BLACK_TOKEN_TIMER = 0
WHITE_TOKEN_TIMER = 0
NUMBER_OF_BLACK_TOKEN = 2
NUMBER_OF_WHITE_TOKEN = 2
current_time = pygame.time.get_ticks()

while not game_over(grid)[0]:
    # clock.tick(50)
    # if pygame.time.get_ticks()-current_time>1000:
    #     if player == BLACK_TOKEN:
    #         BLACK_TOKEN_TIMER += 1
    #     else:
    #         WHITE_TOKEN_TIMER += 1
    #     current_time = pygame.time.get_ticks()

    # cette partie s'occupe d'afficher le score de chaqu'un des coups possibles
    # mouse_pos = pygame.mouse.get_pos()
    # for row in range(ROWS):
    #     for col in range(COLS):
    #         rect = pygame.Rect(200+col*SQUARE_LENGTH, 100+row*SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH)
    #         # verifie si la souris est au dessus de cette case (autrement dit, si elle est en hover!)
    #         if rect.collidepoint(mouse_pos):
    #             if grid[row,col] == EMPTY: 
    #                 potential_gain = len(tokens_to_invert(grid, player, (row,col)))-1
    #                 if potential_gain!=-1 :
    #                     font = pygame.font.Font(None, 36)
    #                     text_surface= font.render(str(potential_gain), True, BLACK)
    #                     text_rect = text_surface.get_rect(center=rect.center)
    #                     window.blit(text_surface, text_rect)

    # cette partie s'occupe de la boucle de jeu entre les deux joueurs 
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT :
    #         running = False
    #     elif event.type == pygame.MOUSEBUTTONDOWN: # evenement correspondant à un click de souris
    #         if event.button == 1: # click sur bouton gauche
    #             y,x = handle_click(y=event.pos[1], x=event.pos[0])
    #             if (y,x) != (-1,-1) and grid[y,x]==EMPTY:
    #                 number_of_tokens = play_a_shot(grid=grid, player=player, position=(y,x),  number_of_tokens=[NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN])
    #                 if number_of_tokens[0] != NUMBER_OF_BLACK_TOKEN or number_of_tokens[1] != NUMBER_OF_WHITE_TOKEN:
    #                     NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
    #                     player=WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
    #                     update_checkerboard(window, grid)

    if player == BLACK_TOKEN :
        best_move_for_ai = get_best_shot(grid, player, 2, True)
    else :
        best_move_for_ai = get_best_shot(grid, player, 4, True)
    
    if best_move_for_ai :
        best_move_for_ai = best_move_for_ai[:2]
        number_of_tokens = play_a_shot(grid=grid, player=player, position=best_move_for_ai,  number_of_tokens=[NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN])
        if number_of_tokens[0] != NUMBER_OF_BLACK_TOKEN or number_of_tokens[1] != NUMBER_OF_WHITE_TOKEN:
            NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
            player = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
            update_checkerboard(window, grid)
    else:
        player = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
        update_checkerboard(window, grid)

    update_timers(window, BLACK_TOKEN_TIMER, WHITE_TOKEN_TIMER, player, NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN)
    pygame.display.update()


print("BLACK="+str(NUMBER_OF_BLACK_TOKEN))
print("WHITE="+str(NUMBER_OF_WHITE_TOKEN))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Clique sur le bouton "X"
            running = False

pygame.quit()