from utility_functions import *
from heuristics import *
class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject
    # where we implement our Minimax algorithm | findAvailMoves, evaluateBoard, swappableTiles, computerHard (recursively)
    # what is a grid object? Basically we need to change to evaluateBoard here
    # convention: player = 1 means max player; player = -1 means min player
    # this function returns both the best move and best value
    def computerHard(self, grid, depth, alpha, beta, player, numMove, flippedDirection):
        newGrid = copy.deepcopy(grid)
        availMoves = self.grid.findAvailMoves(newGrid, player)
        # if there's no feasible move and we're still not in the leaf node yet
        if numMove == 64 or depth == 0 or len(availMoves) == 0:
            if(numMove >= 8 and numMove <= 32):
                coef = [2,10]
            elif numMove >32 and numMove <= 56:
                coef = [3,9]
            else:
                coef = [8,4]
            bMove = None    
            whiteMobility, blackMobility, fron1, fron2 = mobility(grid, player)
            score = coinParty(grid)
            # coef = [0.35, 0.5]    # I hope this works
            # if numMove < 14:
            #     score = whiteMobility - blackMobility
            # elif numMove >= 14 and numMove <= 40:
            #     score = (whiteMobility - blackMobility) + coef[0] * static_weight_beginning(grid)
            # else:
            #     score = (whiteMobility - blackMobility) + coef[1] * static_weight_ending(grid)
            return bMove, score

        if player < 0:   # minimizing player
            bestScore = 100000000000000
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles, flipped = self.grid.swappableTiles(x, y, newGrid, player)   # update the grid
                newGrid[x][y] = player

                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                # we need to update the grid before calling recursive function because we evaluate positions in the future
                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player *-1, numMove+1, flipped)

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)    # reset and make a new grid
                # print(f"NumMove: {numMove}, player: {player}, Best Move: {bestMove}, Best Score: {bestScore}, depth: {depth}")
            
            # print(str(bestMove) + " | " + str(numMove))
            return bestMove, bestScore 
        
        if player > 0:    # maximizer
            bestScore = -100000000000000
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles, flipped = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player

                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player*-1, numMove+1, flipped)   # it's the best move of the opponent

                if value > bestScore:
                    bestScore = value
                    bestMove = move
                alpha = max(alpha, bestScore)     # it should be max isn't it?
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)
                # print(f"NumMove: {numMove}, player: {player}, Best Move: {bestMove}, Best Score: {bestScore}, depth: {depth}")

            return bestMove, bestScore