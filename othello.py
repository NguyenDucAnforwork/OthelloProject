import pygame
import random
import copy
from grid import *
from computer_player import *
import time
import matplotlib.pyplot as plt
import os
class Othello:
    # first time in my life I see they pass self as an argument :)) 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Othello')
        
        self.method = "coin vs static weight | depth = 5"
        self.game_file_path = "./result/games.txt"
        self.player1 = 1
        self.player2 = -1

        self.currentPlayer = 0

        self.time = 0

        self.rows = 8
        self.columns = 8

        self.gameOverForPlayer = True
        self.gameOverForComputer = True
        self.result = []

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
    # def input(self):
    #     for event in pygame.event.get():   # we can only do it ONE TIME
    #         if event.type == pygame.QUIT:
    #             self.RUN = False

    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 3:
    #                 self.grid.printGameLogicBoard()

    #             if event.button == 1:
    #                 if self.gameOverForPlayer and self.gameOverForComputer:                        
    #                     with open(self.game_file_path, "a") as file:
    #                         file.write("\n")
    #                     if len(self.result) > 0:
    #                         plt.plot(self.result)
    #                         plt.xlabel('Move')
    #                         plt.ylabel('Evaluation value')
    #                         plt.title(f'{self.method}')

    #                         # Lưu biểu đồ vào file ảnh trong thư mục "result"
    #                         result_path = os.path.join('result', 'try11.png')
    #                         plt.savefig(result_path)

    #                         # Hiển thị biểu đồ
    #                         plt.show()

    #                     x, y = pygame.mouse.get_pos()
    #                     if x >= 320 and x <= 480 and y >= 400 and y <= 480:
    #                         self.grid.newGame()
    #                         with open(self.game_file_path, "a") as file:
    #                             file.write(f"{self.method}\n")
    #                         self.currentPlayer = -1
    #                         self.result = []
    #                         self.gamePlayed = True
    #                         self.gameOverForPlayer = False
    #                         self.gameOverForComputer = False
                    
    #                 if self.currentPlayer == 1:
    #                     x, y = pygame.mouse.get_pos()
    #                     x, y = (x - 80) // 80, (y - 80) // 80
    #                     with open(self.game_file_path, "a") as file:
    #                         a = x+1
    #                         b = chr(ord('a')+y)
    #                         file.write(f"{b}{a} ")
    #                     validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
    #                     numMove = sum([abs(num) for row in self.grid.gridLogic for num in row])
    #                     # self.gamePlayed = False if numMove == 64 else True
    #                     if validCells:
    #                         self.gameOverForPlayer = False                            
    #                         if (y, x) in validCells:
    #                             self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
    #                             swappableTiles, flippedDirection = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
    #                             for tile in swappableTiles:
    #                                 self.grid.animateTransitions(tile, self.currentPlayer)
    #                                 self.grid.gridLogic[tile[0]][tile[1]] *= -1
    #                             whiteMobility, blackMobility, fron1, fron2 = mobility(self.grid.gridLogic, self.currentPlayer)
                                
    #                             score = (whiteMobility - blackMobility) + static_weight_beginning(self.grid.gridLogic) if numMove >= 30 else whiteMobility - blackMobility

    #                             self.result.append(score)
    #                             print(f"Move: {numMove} | player {self.currentPlayer}, white: Cur - {whiteMobility}, poten - {fron2} || black: Cur - {blackMobility}, poten - {fron1}")                            
    #                             self.currentPlayer *= -1
    #                             self.time = pygame.time.get_ticks()
    #                     else:
    #                         gameOverForPlayer = True   # if we has no valid move
    #                         self.currentPlayer *= -1
    #                         break
    def input(self):
        for event in pygame.event.get():   # we can only do it ONE TIME
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1:
                    if self.gameOverForPlayer and self.gameOverForComputer:                        
                        with open(self.game_file_path, "a") as file:
                            file.write("\n")
                        if len(self.result) > 0:
                            plt.plot(self.result)
                            plt.xlabel('Move')
                            plt.ylabel('Evaluation value')
                            plt.title(f'{self.method}')

                            # Lưu biểu đồ vào file ảnh trong thư mục "result"
                            result_path = os.path.join('result', 'try.png')
                            plt.savefig(result_path)

                            # Hiển thị biểu đồ
                            plt.show()

                        x, y = pygame.mouse.get_pos()
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.newGame()
                            with open(self.game_file_path, "a") as file:
                                file.write(f"{self.method}\n")
                            self.currentPlayer = -1
                            self.result = []
                            self.gameOverForPlayer = False
                            self.gameOverForComputer = False

        if self.currentPlayer == 1:
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 100:   # because of this it would update the score for both side at their timestamp   
                if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                    self.gameOverForPlayer = True
                    self.currentPlayer *= -1
                    return
                
                self.gameOverForPlayer = False
                numMove = sum([abs(num) for row in self.grid.gridLogic for num in row])
                # self.gamePlayed = False if numMove == 63 else True

                start_time = time.time()
                cell, score = self.computerPlayer.computerHard1(self.grid.gridLogic, 5, -64, 64, 1, numMove)
                # print(str(numMove) + " | " + str(cell))
                with open(self.game_file_path, "a") as file:
                    a = cell[0]+1
                    b = chr(ord('a')+cell[1])
                    file.write(f"{b}{a} ")

                # print(cell)
                end_time = time.time()
                # print(f"Thời gian thực hiện nước {numMove} là ", end_time-start_time)
                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
                swappableTiles, flipped = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayer)

                for tile in swappableTiles:
                    self.grid.animateTransitions(tile, self.currentPlayer)
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
            
                self.result.append(coinParty(self.grid.gridLogic))
                self.currentPlayer *= -1   # switch to the opposite side anyways
                
        self.grid.player1Score = self.grid.updateScore(self.player1)
        self.grid.player2Score = self.grid.updateScore(self.player2)
        
        # is this condition necessary? 
        occupied_cell = sum([1 if self.grid.gridLogic[x][y] != 0 else 0 for x in range(0,8) for y in range(0,8)])
        if occupied_cell == 64:
            self.gameOverForComputer = True      # if there's no available move there we simply pass our turn
            self.gameOverForPlayer = True                       # there doesn't exist the case when both player couldn't move while the board's still not fulfiled
            return
            
    # gameOver | findAvailMoves => computerHard1 => insertToken => swappableTiles => animateTransitions => updateScore
    # we use the algorith to find the best move for black pieces only
    # update score | update cell that is swappable | find the next move for the computer side
    def update(self):
        if self.currentPlayer == -1:
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 100:   # because of this it would update the score for both side at their timestamp   
                if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                    self.gameOverForComputer = True
                    self.currentPlayer *= -1
                    return
                
                # for move in self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                #     print(move, end=" ")
                # print()

                self.gameOverForComputer = False
                numMove = sum([abs(num) for row in self.grid.gridLogic for num in row])
                # self.gamePlayed = False if numMove == 63 else True

                start_time = time.time()
                cell, score = self.computerPlayer.computerHard2(self.grid.gridLogic, 4, -64, 64, -1, numMove)
                # print(str(numMove) + " | " + str(cell))
                with open(self.game_file_path, "a") as file:
                    a = cell[0]+1
                    b = chr(ord('a')+cell[1])
                    file.write(f"{b}{a} ")

                # print(cell)
                end_time = time.time()
                # print(f"Thời gian thực hiện nước {numMove} là ", end_time-start_time)
                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
                swappableTiles, flipped = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayer)

                for tile in swappableTiles:
                    self.grid.animateTransitions(tile, self.currentPlayer)
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1

                self.result.append(coinParty(self.grid.gridLogic))

                self.currentPlayer *= -1   # switch to the opposite side anyways
                
        self.grid.player1Score = self.grid.updateScore(self.player1)
        self.grid.player2Score = self.grid.updateScore(self.player2)
        
        # is this condition necessary? 
        occupied_cell = sum([1 if self.grid.gridLogic[x][y] != 0 else 0 for x in range(0,8) for y in range(0,8)])
        if occupied_cell == 64:
            self.gameOverForComputer = True      # if there's no available move there we simply pass our turn
            self.gameOverForPlayer = True                       # there doesn't exist the case when both player couldn't move while the board's still not fulfiled
            return

    # draw grid with the method drawGrid of the class Grid and update
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()