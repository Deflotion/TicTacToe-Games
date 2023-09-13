import sys
import pygame
import numpy as np
import random as rd
import copy
from Constant import *

#$ PYGAME SETUP
pygame.init()
layar = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe UBM')
layar.fill(BG_COLOR)



#$ Class
class Board:
    
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show = False):
        #* Vertical Wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    COLOR = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(layar, COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        #* Horizontal Wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    COLOR = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row  * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(layar, COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        #* Desc Wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    COLOR = CROSS_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH - 20 , HEIGHT - 20)
                    pygame.draw.line(layar, COLOR, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        #* Asc Wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    COLOR = CROSS_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (20, HEIGHT -20)
                    fPos = (WIDTH-20, 20)
                    pygame.draw.line(layar, COLOR, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        #* Draw
        return 0
        
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
        
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0 
    
    def getEmptySquares(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs
    
    def isFull(self):
        return self.marked_sqrs == 9
    
    def isEmpty(self):
        return self.marked_sqrs == 0

class AI:
    
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player
    
    def rnd(self, board):
        empty_sqrs = board.getEmptySquares()
        index = rd.randrange(0, len(empty_sqrs))
        
        return empty_sqrs[index]
    
    def minimax(self, board, maximizing):
        
        #* Basic Case
        case = board.final_state()
        
        #* Player 1 Wins
        if case == 1:
            return 1, None
        
        #* Player 2 Wins / AI
        if case == 2:
            return -1, None
        
        #* Draw
        elif board.isFull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.getEmptySquares()
            
            for (row, col)in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.getEmptySquares()
            
            for (row, col)in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                    
            return min_eval, best_move
    
    def eval(self,main_board):
        if self.level == 0:
            #* Rand Choice
            eval = 'Random'
            move = self.rnd(main_board)
        else:
            #* Minimax Algo
            eval, move = self.minimax(main_board, False)
        
        # print(f"AI Has Choose To Mark The Squares In Position{move} With An Evaluation Of {eval}")
        
        return move
        
class Game:
    
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True 
        self.show_lines()
    
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
    
    def show_lines(self):
        #? Bg
        layar.fill(BG_COLOR)
        
        #? Vertical Line
        pygame.draw.line(layar, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(layar, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        
        #? Horizontal Line
        pygame.draw.line(layar, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(layar, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # Circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(layar, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

        elif self.player == 2:
            # Cross
            #* Desc Line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(layar, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            
            #* Asc Line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE +  OFFSET)
            pygame.draw.line(layar, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
    
    def next_turn(self):
        self.player = self.player % 2+1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isOver(self):
        return self.board.final_state(show=True) != 0 or self.board.isFull()

    def reset(self):
        self.__init__()

def main():
    #$ Object
    game = Game()
    board = game.board
    ai = game.ai
    
    #$ Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                #& g = gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                
                #& r = restart 
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                
                #& 0 = Rand AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                #& 1 = Minimax AI
                if event.key == pygame.K_1:
                    ai.level = 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    
                    if game.isOver():
                        game.running = False
            
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #* Update Screen
            pygame.display.update()
            
            #* AI Methods
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.isOver():
                game.running = False
        
        pygame.display.update()

main()