import pygame
import os

# Ici on définit les constantes utilisées dans le jeu

# Taille de ma fenêtre 
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800


# Taille de mon damier
HEIGHT = 400
WIDTH = 400
ROWS = 8
COLS = 8
SQUARE_LENGTH = HEIGHT//ROWS

# Couleurs utilisées dans le damier
GREEN = (5,142,70)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (100,149,237)
GRAY = (200,200,200)

# Images
PATH = ".\imgs"
BLACK_TOKENS = pygame.transform.scale(pygame.image.load(os.path.join(PATH, "jetons_noir.png")),  (WIDTH,100))
WHITE_TOKENS = pygame.transform.scale(pygame.image.load(os.path.join(PATH, "jetons_blanc.png")), (WIDTH,100))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(PATH, "bois.jpg")), (200, WINDOW_HEIGHT))
CHRONOMETER = pygame.transform.scale(pygame.image.load(os.path.join(PATH, "chronometre.png")), (40, 40))

# Constantes utilisées dans la grille de jeu
EMPTY = 0
BLACK_TOKEN = 1
WHITE_TOKEN = 2

# Directions possibles lors du jeu
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
TOP = -1
BOTTOM = +1
LEFT = -1
RIGHT = +1

# poids (importance) de chaque case du Reversi (utilisé dans la fonction d'évaluation)
POSITION_WEIGHTS = [
            [40, 3, 15,  10,  10, 15, 3, 40],
            [3, 0, 9, 12, 12, 9, 0, 3],
            [15,  9,  11, 15, 15, 11,  9, 15],
            [10,   12,  15, 18, 18, 15,  12,  10],
            [10,   12,  15, 18, 18, 15,  12,  10],
            [15,  9,  11, 15, 15, 11,  9,  15],
            [3, 0, 9, 12, 12, 9, 0, 3],
            [40, 3, 15,  10,  10, 15, 3, 40]
        ]

# définir les trois niveaux de difficulté
# with_pruning pour dire si c'est avec élagage ou pas
LEVELS = {
    "Facile" : {"with_pruning":False, "depth":1},
    "Moyen" : {"with_pruning":False, "depth":3},
    "Difficile" : {"with_pruning":True, "depth":5},    
}