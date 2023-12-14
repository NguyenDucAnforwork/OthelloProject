import pygame
import random
import copy
from grid import *
from computer_player import *

class Othello:
    # first time in my life I see they pass self as an argument :)) 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Othello')

        self.player1 = 1
        self.player2 = -1

        self.currentPlayer = -1

        self.time = 0

        self.rows = 8
        self.columns = 8

        self.gameOver = True

        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.computerPlayer = ComputerPlayer(self.grid)

        self.RUN = True

    # input, update and draw
    def run(self):
        while self.RUN == True:
            self.input()
            self.update()
            self.draw()

    # update the grid for the human side
    # gameOver | newGame | printGameLogicBoard | findAvailMoves => insertToken => swappableTiles => animateTransition
    def input(self):
        for event in pygame.event.get():   # we can only do it ONE TIME
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1:
                    if self.currentPlayer == 1 and not self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        x, y = (x - 80) // 80, (y - 80) // 80
                        validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
                        if validCells:                            
                            if (y, x) in validCells:
                                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                                swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
                                for tile in swappableTiles:
                                    self.grid.animateTransitions(tile, self.currentPlayer)
                                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                                self.currentPlayer *= -1
                                self.time = pygame.time.get_ticks()
                            else:
                                break
                    if self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.newGame()
                            self.gameOver = False

    # gameOver | findAvailMoves => computerHard => insertToken => swappableTiles => animateTransitions => updateScore
    # we use the algorith to find the best move for black pieces only
    # update score | update cell that is swappable | find the next move for the computer side
    def update(self):
        if self.currentPlayer == -1:
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 100:
                if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                    self.gameOver = True
                    return
                cell, score = self.computerPlayer.computerHard(self.grid.gridLogic, 6, -64, 64, -1)
                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
                swappableTiles = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayer)
                for tile in swappableTiles:
                    self.grid.animateTransitions(tile, self.currentPlayer)
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                if not self.gameOver:
                    self.currentPlayer *= -1

        self.grid.player1Score = self.grid.updateScore(self.player1)
        self.grid.player2Score = self.grid.updateScore(self.player2)
        occupied_cell = sum([1 if self.grid.gridLogic[x][y] != 0 else 0 for x in range(0,8) for y in range(0,8)])
        if occupied_cell == 64:
            self.gameOver = True      # if there's no available move there we simply pass our turn
                                    # there doesn't exist the case when both player couldn't move while the board's still not fulfiled
            return

    # draw grid with the method drawGrid of the class Grid and update
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()