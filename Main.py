import sys
import pygame

from Constant import *

#$ PYGAME SETUP
pygame.init()
layar = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe UBM')
layar.fill(BG_COLOR)

class Game:
    
    def __init__(self):
        pass
    
    def show_lines(self):
        pass

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()



main()