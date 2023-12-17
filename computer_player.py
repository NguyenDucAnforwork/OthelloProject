from utility_functions import *

class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject

    # where we implement our Minimax algorithm | findAvailMoves, evaluateBoard, swappableTiles, computerHard (recursively)
    # what is a grid object? Basically we need to change to evaluateBoard here
    # convention: player = 1 means max player; player = -1 means min player
    # this function returns both the best move and best value
    def computerHard(self, grid, depth, alpha, beta, player, numMove):
        newGrid = copy.deepcopy(grid)
        availMoves = self.grid.findAvailMoves(newGrid, player)

        if depth == 0 or len(availMoves) == 0:
            if(numMove >= 8 and numMove <= 32):
                coef = [2,10]
            elif numMove >32 and numMove <= 56:
                coef = [2,6]
            else:
                coef = [2,2]
            bestMove, Score = None, coef[0] * stability(grid)    # heuristic function
            return bestMove, Score

        if player < 0:   # minimizing player
            bestScore = 64
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)   # update the grid
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                # we need to update the grid before calling recursive function
                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player *-1, numMove+1)

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)    # reset and make a new grid
            return bestMove, bestScore

        if player > 0:    # maximizer
            bestScore = -64 
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player*-1,numMove+1)   # it's the best move of the opponent

                if value > bestScore:
                    bestScore = value
                    bestMove = move
                alpha = max(alpha, bestScore)     # it should be max isn't it?
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)
            return bestMove, bestScore