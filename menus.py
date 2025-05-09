# ce fichier main.py contient la boucle du jeu

import pygame
from Constants import *
from game import *
from AI import *
import sys

# Initialisation du pygame
pygame.init()

# Ajuster la taille de la fenetre
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Police
font = pygame.font.SysFont(None, 40)

# Définition des boutons 
button_width = 300
button_height = 60
button_margin = 80

buttons = [
    {"label" : "Humain vs Humain", "rect": pygame.Rect((WINDOW_WIDTH-button_width)//2, 150, button_width, button_height)}, 
    {"label" : "Humain vs IA", "rect": pygame.Rect((WINDOW_WIDTH-button_width)//2, 150+button_height+button_margin, button_width, button_height)},
    {"label" : "IA vs IA", "rect": pygame.Rect((WINDOW_WIDTH-button_width)//2, 150+2*(button_height+button_margin), button_width, button_height)},
]


# boucle principale du jeu
def main_menu():
    pygame.display.set_caption("Mode de jeu")
    while True:
        window.fill(GRAY)

        # gestion de évenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                sys.exit() 

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        return button["label"] 
        
        # gestion des affichages
        title_font = pygame.font.SysFont(None, 50)
        title_surf = title_font.render("Choisissez un mode de jeu :", True, BLACK)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 80))
        window.blit(title_surf, title_rect)
        for button in buttons:
            pygame.draw.rect(window, GREEN, button["rect"], border_radius=15)
            pygame.draw.rect(window, BLACK, button["rect"], border_radius=15, width=2)
            text_surf = font.render(button["label"], True, WHITE)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            window.blit(text_surf, text_rect)
        
        pygame.display.flip()


levels = [
    {"label" : "Facile", "rect": pygame.Rect((WINDOW_WIDTH-button_width)//2, 150, button_width, button_height)}, 
    {"label" : "Moyen", "rect": pygame.Rect((WINDOW_WIDTH-button_width)//2, 150+button_height+button_margin, button_width, button_height)},
    {"label" : "Difficile", "rect": pygame.Rect((WINDOW_WIDTH-button_width)//2, 150+2*(button_height+button_margin), button_width, button_height)},
]

# boucle principale du jeu
def level_AI_menu():
    pygame.display.set_caption("Niveau de l'IA")
    while True:
        window.fill(GRAY)

        # gestion de évenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                sys.exit() 

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                mouse_pos = pygame.mouse.get_pos()
                for i, level in enumerate(levels):
                    if level["rect"].collidepoint(mouse_pos):
                        return level["label"] 
        
        # gestion des affichages
        title_font = pygame.font.SysFont(None, 50)
        title_surf = title_font.render("Choisissez le niveau de difficulté de l'IA :", True, BLACK)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 80))
        window.blit(title_surf, title_rect)
        for level in levels:
            pygame.draw.rect(window, GREEN, level["rect"], border_radius=15)
            pygame.draw.rect(window, BLACK, level["rect"], border_radius=15, width=2)
            text_surf = font.render(level["label"], True, WHITE)
            text_rect = text_surf.get_rect(center=level["rect"].center)
            window.blit(text_surf, text_rect)
        
        pygame.display.flip()


if __name__ == "__main__":
    choix = level_AI_menu()
    print("Mode choisi :", choix)


    

    

