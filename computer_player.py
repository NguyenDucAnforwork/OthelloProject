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

        # if there's no feasible move and we're still not in the leaf node yet
        if numMove == 64 or depth == 0 or len(availMoves) == 0:
            if(numMove >= 8 and numMove <= 32):
                coef = [2,10]
            elif numMove >32 and numMove <= 56:
                coef = [3,9]
            else:
                coef = [8,4]
            bMove, Score = None, coef[0] * coinParty(grid) + coef[1] * mobility(grid)    # heuristic function
            # print(f"NumMove: {numMove}, player: {player}, Best Move: {Score}, Best Score: {bMove}, depth: {depth}")

            return bMove, Score

        if player < 0:   # minimizing player
            bestScore = 100000
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)   # update the grid
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                # we need to update the grid before calling recursive function because we evaluate positions in the future
                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player *-1, numMove+1)

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)    # reset and make a new grid
                # print(f"NumMove: {numMove}, player: {player}, Best Move: {bestMove}, Best Score: {bestScore}, depth: {depth}")
            return bestMove, bestScore

        if player > 0:    # maximizer
            bestScore = -100000 
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
                # print(f"NumMove: {numMove}, player: {player}, Best Move: {bestMove}, Best Score: {bestScore}, depth: {depth}")
            return bestMove, bestScore