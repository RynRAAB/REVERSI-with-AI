# ce fichier main.py contient la boucle du jeu
import pygame
from Constants import *
from game import *
from AI import *
from menus import main_menu, level_AI_menu

def display_ai_levels(surface, ai1_label, ai2_label):
    font = pygame.font.Font(None, 28) 
    pygame.draw.rect(surface, GRAY, (0, 0, WINDOW_WIDTH, 30))

    label = f" Noire : {ai1_label}    |     Blanche : {ai2_label}"
    text_surface = font.render(label, True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 15))

    surface.blit(text_surface, text_rect)

def display_winner(grid):
    _, black_tokens, white_tokens = game_over(grid)
    font = pygame.font.Font(None, 48)

    if black_tokens > white_tokens:
        message = "Les Noirs ont gagné !"
    elif white_tokens > black_tokens:
        message = "Les Blancs ont gagné !"
    else:
        message = "Match nul !"

    text_surface = font.render(message, True, RED)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(text_surface, text_rect)
    pygame.display.update()


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


clock = pygame.time.Clock()



def human_vs_human():
    grid = initialise_game()
    player= BLACK_TOKEN
    update_checkerboard(window, grid)
    BLACK_TOKEN_TIMER = 0
    WHITE_TOKEN_TIMER = 0
    NUMBER_OF_BLACK_TOKEN = 2
    NUMBER_OF_WHITE_TOKEN = 2
    current_time = pygame.time.get_ticks()
    running=True

    while not game_over(grid)[0]:
        if not get_valid_shots(grid, player):
            player=WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
            
        clock.tick(50)
        if pygame.time.get_ticks()-current_time>1000:
            if player == BLACK_TOKEN:
                BLACK_TOKEN_TIMER += 1
            else:
                WHITE_TOKEN_TIMER += 1
            current_time = pygame.time.get_ticks()

        # cette partie s'occupe d'afficher le score de chaqu'un des coups possibles
        mouse_pos = pygame.mouse.get_pos()
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(200+col*SQUARE_LENGTH, 100+row*SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH)
                # verifie si la souris est au dessus de cette case (autrement dit, si elle est en hover!)
                if rect.collidepoint(mouse_pos):
                    if grid[row,col] == EMPTY: 
                        potential_gain = len(tokens_to_invert(grid, player, (row,col)))-1
                        if potential_gain!=-1 :
                            font = pygame.font.Font(None, 36)
                            text_surface= font.render(str(potential_gain), True, BLACK)
                            text_rect = text_surface.get_rect(center=rect.center)
                            window.blit(text_surface, text_rect)

        # cette partie s'occupe de la boucle de jeu entre les deux joueurs 
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # evenement correspondant à un click de souris
                if event.button == 1: # click sur bouton gauche
                    y,x = handle_click(y=event.pos[1], x=event.pos[0])
                    if (y,x) != (-1,-1) and grid[y,x]==EMPTY:
                        number_of_tokens = play_a_shot(grid=grid, player=player, position=(y,x),  number_of_tokens=[NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN])
                        if number_of_tokens[0] != NUMBER_OF_BLACK_TOKEN or number_of_tokens[1] != NUMBER_OF_WHITE_TOKEN:
                            NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
                            player=WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN
                            update_checkerboard(window, grid)
        update_timers(window, BLACK_TOKEN_TIMER, WHITE_TOKEN_TIMER, player, NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN)
        pygame.display.update()

        if not running:
            # pygame.quit()
            black, white= log_token_counts(grid)
            print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
            return
    
    while running:
        update_checkerboard(window, grid)
        display_winner(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clique sur le bouton "X"
                # pygame.quit()
                black, white= log_token_counts(grid)
                print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
                return


def human_vs_ai(AI_level):
    grid = initialise_game()
    player= BLACK_TOKEN    
    update_checkerboard(window, grid)
    display_ai_levels(window, "Humain", AI_level)
    pygame.display.update()
    BLACK_TOKEN_TIMER = 0
    WHITE_TOKEN_TIMER = 0
    NUMBER_OF_BLACK_TOKEN = 2
    NUMBER_OF_WHITE_TOKEN = 2
    current_time = pygame.time.get_ticks()
    running=True

    while not game_over(grid)[0]:
        if not get_valid_shots(grid, player):
            player=WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN

        clock.tick(50)
        if pygame.time.get_ticks()-current_time>1000:
            if player == BLACK_TOKEN:
                BLACK_TOKEN_TIMER += 1
            else:
                WHITE_TOKEN_TIMER += 1
            current_time = pygame.time.get_ticks()

        # cette partie s'occupe d'afficher le score de chaqu'un des coups possibles
        if player == BLACK_TOKEN:
            mouse_pos = pygame.mouse.get_pos()
            for row in range(ROWS):
                for col in range(COLS):
                    rect = pygame.Rect(200+col*SQUARE_LENGTH, 100+row*SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH)
                    # verifie si la souris est au dessus de cette case (autrement dit, si elle est en hover!)
                    if rect.collidepoint(mouse_pos):
                        if grid[row,col] == EMPTY: 
                            potential_gain = len(tokens_to_invert(grid, player, (row,col)))-1
                            if potential_gain!=-1 :
                                font = pygame.font.Font(None, 36)
                                text_surface= font.render(str(potential_gain), True, BLACK)
                                text_rect = text_surface.get_rect(center=rect.center)
                                window.blit(text_surface, text_rect)

        # cette partie s'occupe de la boucle de jeu entre les deux joueur
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # evenement correspondant à un click de souris
                if event.button == 1 and player == BLACK_TOKEN: # click sur bouton gauche
                    y,x = handle_click(y=event.pos[1], x=event.pos[0])
                    if (y,x) != (-1,-1) and grid[y,x]==EMPTY:
                        number_of_tokens = play_a_shot(grid=grid, player=player, position=(y,x),  number_of_tokens=[NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN])
                        if number_of_tokens[0] != NUMBER_OF_BLACK_TOKEN or number_of_tokens[1] != NUMBER_OF_WHITE_TOKEN:
                            NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
                            player=WHITE_TOKEN 
                            update_checkerboard(window, grid)
                            display_ai_levels(window, "Humain", AI_level)

        update_timers(window, BLACK_TOKEN_TIMER, WHITE_TOKEN_TIMER, player, NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN)
        pygame.display.update()

        if player == WHITE_TOKEN:
            level = LEVELS[AI_level]
            best_move_for_ai = get_best_shot(grid, WHITE_TOKEN, level["depth"], level["with_pruning"])
            if best_move_for_ai :
                best_move_for_ai = best_move_for_ai[:2]
                number_of_tokens = play_a_shot(grid=grid, player=player, position=best_move_for_ai,  number_of_tokens=[NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN])
                if number_of_tokens[0] != NUMBER_OF_BLACK_TOKEN or number_of_tokens[1] != NUMBER_OF_WHITE_TOKEN:
                    NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
                    player = BLACK_TOKEN
                    update_checkerboard(window, grid)
                    display_ai_levels(window, "Humain", AI_level)
                    log_token_counts(grid)

        if not running:
            # pygame.quit()
            black, white= log_token_counts(grid)
            print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
            return
    while running:
        update_checkerboard(window, grid)
        display_winner(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clique sur le bouton "X"
                # pygame.quit()
                black, white= log_token_counts(grid)
                print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
                return

def ai_vs_ai(AI1_level_label, AI2_level_label):
    grid = initialise_game()
    player= BLACK_TOKEN
    update_checkerboard(window, grid)
    BLACK_TOKEN_TIMER = 0
    WHITE_TOKEN_TIMER = 0
    NUMBER_OF_BLACK_TOKEN = 2
    NUMBER_OF_WHITE_TOKEN = 2
    running=True

    while not game_over(grid)[0]:
        if not get_valid_shots(grid, player):
            player=WHITE_TOKEN if player==BLACK_TOKEN else BLACK_TOKEN

        # cette partie s'occupe de la boucle de jeu entre les deux joueur
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                running = False

        if player == BLACK_TOKEN:
            level = LEVELS[AI1_level_label]
        else:
            level = LEVELS[AI2_level_label]
        best_move_for_ai = get_best_shot(grid, player, level["depth"], level["with_pruning"])
        if best_move_for_ai :
            best_move_for_ai = best_move_for_ai[:2]
            number_of_tokens = play_a_shot(grid=grid, player=player, position=best_move_for_ai,  number_of_tokens=[NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN])
            if number_of_tokens[0] != NUMBER_OF_BLACK_TOKEN or number_of_tokens[1] != NUMBER_OF_WHITE_TOKEN:
                NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN = number_of_tokens
                player = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
                update_checkerboard(window, grid)
                display_ai_levels(window, AI1_level_label, AI2_level_label)
                log_token_counts(grid)

            else:
                player = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
                update_checkerboard(window, grid)
                display_ai_levels(window, AI1_level_label, AI2_level_label)
                log_token_counts(grid)

        
        if not running:
            # pygame.quit()
            black, white= log_token_counts(grid)
            print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
            return black, white

        update_timers(window, BLACK_TOKEN_TIMER, WHITE_TOKEN_TIMER, player, NUMBER_OF_BLACK_TOKEN, NUMBER_OF_WHITE_TOKEN)
        pygame.display.update()
    
    while running:
        update_checkerboard(window, grid)
        display_winner(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clique sur le bouton "X"
                # pygame.quit()
                black, white= log_token_counts(grid)
                print(f"[TOKENS] ⚫ Noir : {black}  | ⚪ Blanc : {white}")
                return black, white
    
    
       


if __name__ == "__main__":
    game_mode = main_menu()
    if game_mode == "Humain vs Humain":
        human_vs_human()
    elif game_mode == "Humain vs IA":
        AI_level = level_AI_menu("")
        human_vs_ai(AI_level)
    else:
        AI1_level = level_AI_menu("1")
        AI2_level = level_AI_menu("2")
        ai_vs_ai(AI1_level, AI2_level)