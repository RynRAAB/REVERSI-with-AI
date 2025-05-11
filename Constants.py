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

# Directions de jeu possibles dans le reversi (haut, bas, gauche, droite, haut-gauche, haut-droite, bas-gauche, bas-droite) 
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
TOP = -1
BOTTOM = +1
LEFT = -1
RIGHT = +1

# table de pondération du reversi
# poids (importance) de chaque case du Reversi (utilisé dans la fonction d'évaluation) pour évaluer un plateau donnée en fonction de l'occupation de la grille
POSITION_WEIGHTS = [
    [100, -25, 10, 5, 5, 10, -25, 100],
    [-25, -50, 1, 1, 1, 1, -50, -25],
    [10, 1, 3, 2, 2, 3, 1, 10],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [10, 1, 3, 2, 2, 3, 1, 10],
    [-25, -50, 1, 1, 1, 1, -50, -25],
    [100, -25, 10, 5, 5, 10, -25, 100]
]

# définir les trois niveaux de difficulté du reversi (Facile, Moyen et Difficile)
# with_pruning pour dire si c'est avec ou sans élagage 
# depth correspond à la profondeur d'anticipation de notre minmax
LEVELS = {
    "Facile" : {"with_pruning":False, "depth":1},
    "Moyen" : {"with_pruning":False, "depth":3},
    "Difficile" : {"with_pruning":True, "depth":4},    
}
