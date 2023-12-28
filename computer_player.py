from utility_functions import *
from heuristics import *
class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject
        self.nodes = 0
        self.maxDepth = 5
        self.lookupTable = {}
        self.result = (0,0)

    # where we implement our Minimax algorithm | findAvailMoves, evaluateBoard, swappableTiles, computerHard (recursively)
    # what is a grid object? Basically we need to change to evaluateBoard here
    # convention: player = 1 means max player; player = -1 means min player
    # this function returns both the best move and best value
    def alphaBetaPruning1(self, grid, depth, alpha, beta, player, maxDepth):
        self.nodes += 1
        newGrid = copy.deepcopy(grid)
        copyGrid = tuple(map(tuple, grid))
        availMoves = self.grid.findAvailMoves(newGrid, player)
        # if copyGrid not in self.lookupTable:
        #     availMoves = self.grid.findAvailMoves(newGrid, player)
        # else:
        #     availMoves = self.lookupTable[copyGrid]
        # moves_value = []

        # if there's no feasible move and we're still not in the leaf node yet
        if depth == maxDepth or len(availMoves) == 0:            
            bMove = None    
            # whiteMobility, blackMobility = mobility(grid, player)
            score = stability(grid)
            return bMove, score

        if player < 0:   # minimizing player
            bestScore = float('inf')
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles, flipped = self.grid.swappableTiles(x, y, newGrid, player)   # update the grid
                newGrid[x][y] = player

                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                # we need to update the grid before calling recursive function because we evaluate positions in the future
                bMove, value = self.alphaBetaPruning1(newGrid, depth+1, alpha, beta, player *-1, maxDepth)
                # moves_value.append((move, value))

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)    # reset to the initial grid to prepare for the next iteration
            # if copyGrid not in self.lookupTable:
            #     # moves_value.sort(key=lambda x: x[1], reverse=True)
            #     self.lookupTable[copyGrid] = []
            
            #     for move, value in moves_value:
            #         self.lookupTable[copyGrid].append(move)

            return bestMove, bestScore 
        
        if player > 0:    # maximizer
            bestScore = float('-inf')
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles, flipped = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player

                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.alphaBetaPruning1(newGrid, depth+1, alpha, beta, player*-1, maxDepth)   # it's the best move of the opponent

                if value > bestScore:
                    bestScore = value
                    bestMove = move
                alpha = max(alpha, bestScore)     # it should be max isn't it?
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)

            # if copyGrid not in self.lookupTable:
            #     moves_value.sort(key=lambda x: x[1], reverse=True)
            #     self.lookupTable[copyGrid] = []
            
            #     for move, value in moves_value:
            #         self.lookupTable[copyGrid].append(move)
            
            return bestMove, bestScore
        
    def alphaBetaPruning2(self, grid, depth, alpha, beta, player, numMove):
        self.nodes += 1
        newGrid = copy.deepcopy(grid)
        availMoves = self.grid.findAvailMoves(newGrid, player)
        # if there's no feasible move and we're still not in the leaf node yet
        if numMove == 64 or depth == self.maxDepth or len(availMoves) == 0:
            if(numMove >= 8 and numMove <= 32):
                coef = [2,10]
            elif numMove >32 and numMove <= 56:
                coef = [3,9]
            else:
                coef = [8,4]
            bMove = None    
            score = stability(grid)
            return bMove, score

        if player < 0:   # minimizing player
            bestScore = float('inf')
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles, flipped = self.grid.swappableTiles(x, y, newGrid, player)   # update the grid
                newGrid[x][y] = player

                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                # we need to update the grid before calling recursive function because we evaluate positions in the future
                bMove, value = self.alphaBetaPruning2(newGrid, depth+1, alpha, beta, player *-1, numMove+1)

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)    # reset and make a new grid
            
            return bestMove, bestScore 
        
        if player > 0:    # maximizer
            bestScore = float('-inf')
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles, flipped = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player

                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.alphaBetaPruning2(newGrid, depth+1, alpha, beta, player*-1, numMove+1)   # it's the best move of the opponent

                if value > bestScore:
                    bestScore = value
                    bestMove = move
                alpha = max(alpha, bestScore)     # it should be max isn't it?
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)

            return bestMove, bestScore
        
    def iterativeDeepning(self, grid, player):
        for depth in range(self.maxDepth):
            cell, value = self.alphaBetaPruning1(grid, 0, -64, 64, player, depth+1)
            print(cell, value)

            for grid in self.lookupTable:
                print("depth = ", depth)
                print(grid)
            #     print(self.lookupTable[grid])
            self.result = cell
        return cell, value