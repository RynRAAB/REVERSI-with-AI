from Reversi import *
import pygame
import numpy as np


def organize_tournament(IA1_level, IA2_level, rounds=10):
    IA1_wins = 0
    IA2_wins = 0
    start_time = pygame.time.get_ticks()    
    for i in range(rounds):
        black, white = ai_vs_ai(IA1_level, IA2_level)
        if black > white:
            IA1_wins += 1
        elif black < white:
            IA2_wins += 1
        print(f"Round {i+1} : [TOKENS] ⚫ Noir ({IA1_level}) : {black}  | ⚪ Blanc ({IA2_level}) : {white}")
    finishtime = pygame.time.get_ticks()
    total_time = (finishtime - start_time) / 1000
    print(f"\nFinal Results:\n{IA1_level} wins: {IA1_wins}\n{IA2_level} wins: {IA2_wins}")
    print(f"Total time taken: {total_time:.2f} seconds")

if __name__ == "__main__" :
    organize_tournament("Facile", "Moyen", rounds=5)
    organize_tournament("Facile", "Difficile", rounds=5)
    organize_tournament("Moyen", "Facile", rounds=5)
    organize_tournament("Moyen", "Difficile", rounds=5)
    organize_tournament("Difficile", "Facile", rounds=5)
    organize_tournament("Difficile", "Moyen", rounds=5)