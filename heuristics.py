from utility_functions import * 

def coinParty(grid):
    black_piece = sum([1 if num == -1 else 0 for row in grid for num in row])
    white_piece = sum([1 if num == 1 else 0 for row in grid for num in row]) 
    
    return (white_piece - black_piece) 

# it's actually not the current player but the previous guy
def mobility(grid, currentPlayer):
    # actual/potential mobility: For simplicity I would use the most simple form
    moves = {}
    moves[1] = []
    moves[-1] = []
    moves[1], swappableBlackTiles = findAvailMovesGlobal(grid, 1)
    moves[-1], swappableWhiteTiles = findAvailMovesGlobal(grid, -1)

    # coeffcient:
    corner = 3
    X = -4
    C = -3
    edge = 0.5

    # potential mobility: I would calculate the number of frontier/outside discs
    frontier = {}
    frontier[1] = []
    frontier[-1] = []
    for gridX, row in enumerate(grid):
        for gridY, col in enumerate(row):
            if grid[gridX][gridY] != 0:
                player = grid[gridX][gridY]
                validdirections = []
                if gridX != 0: validdirections.append((gridX-1, gridY))
                if gridX!= 7: validdirections.append((gridX+1, gridY))
                if gridY != 0: validdirections.append((gridX, gridY-1))
                if gridY != 7: validdirections.append((gridX, gridY+1))
                
                for direction in validdirections:
                    if grid[direction[0]][direction[1]]  == 0 and (direction[0], direction[1]) not in frontier[player] and (direction[0], direction[1] not in moves[player * -1]):
                       frontier[player].append((direction[0], direction[1]))
                       break 
    
    # parameters of the corner/X + C squares/remaining edge squares
    corner_square = [(0,0), (0,7), (7,7), (7,0)]
    C_square = [(0,1), (1,0), (0,6), (7,1), (6,0), (7,1), (7,6), (6,7)]
    X_square = [(1,1), (6,6), (6,1), (6,6)]
    edge_square = [(0,2), (0,3), (0,4), (0,5), (7,4), (7,5), (7,2), (7,3), (2,0), (3,0), (4,0), (5,0), (2,7), (3,7), (4,7), (5,7)]
   
    # calculate the total mobility
    whiteMobility = 2/5*len(moves[1]) + 3/5*len(frontier[-1])
    blackMobility = 2/5*len(moves[-1]) + 3/5*len(frontier[1])
    
    # take into account the quality of the move
    # if currentPlayer == 1:
    #     for move in blackMoves:
    #         if move in corner_square:
    #             blackMobility += 6 * corner
    #         if move in X_square:
    #             blackMobility += 6 * X
    #         if move in C_square:
    #             blackMobility += 6*C
    #         if move in edge_square:
    #             blackMobility += 6*edge
    #     for move in frontier[1]:
    #         if move in corner_square:
    #             blackMobility += 4 * corner
    #         if move in X_square:
    #             blackMobility += 4 * X   # not sure about this
    #         if move in C_square:
    #             blackMobility += 4 * C
    #         if move in edge_square:
    #             blackMobility += 4 * edge

        # for move in whiteMoves:
        #     if move in corner_square:
        #         whiteMobility += 6 * corner
        #     if move in X_square:
        #         whiteMobility += 6 * X
        #     if move in C_square:
        #         whiteMobility += 6*C
        #     if move in edge_square:
        #         whiteMobility += 6*edge

        # for move in frontier[-1]:
        #     if move in corner_square:
        #         whiteMobility += 4 * corner
        #     if move in X_square:
        #         whiteMobility += 4 * X
        #     if move in C_square:
        #         whiteMobility += 4 * C 
        #     if move in edge_square:
        #         whiteMobility += 4 * edge
    return whiteMobility, blackMobility, len(frontier[1]), len(frontier[-1])

# stable, semi-stable, unstable. Do we really need the statistic from both sides? 
def stability(grid):
    # 

    # unstable
    whiteMoves, unstableBlackTiles = findAvailMovesGlobal(grid, 1)
    blackMoves, unstableWhiteTiles = findAvailMovesGlobal(grid, -1)

    # semi-stable

    # stable
    whiteStable = stableDisc(grid, 1)
    blackStable = stableDisc(grid, -1)
    return len(whiteStable) - len(blackStable) 

# we definitely need to experiment some pairs of weights
def xSquare(grid):
    coordinates = (
        [1,1], [6,6],
        [6,1], [1,6],
    )

    white_pieces = sum([1 if grid[coor[0]][coor[1]] == 1 else 0 for coor in coordinates])
    black_pieces = sum([1 if grid[coor[0]][coor[1]] == -1 else 0 for coor in coordinates])

    return -5 * white_pieces + 5 * black_pieces

def corner(grid):
    coordinates = (
        [0,0], [0,7],
        [7,0], [7,7],
    )

    white_pieces = sum([1 if grid[coor[0]][coor[1]] == 1 else 0 for coor in coordinates])
    black_pieces = sum([1 if grid[coor[0]][coor[1]] == -1 else 0 for coor in coordinates])

    return 10 * white_pieces - 10 * black_pieces

def corner_occupancy(grid):
    corner = [[0,0], [0,7], [7,0], [7,7]]
    white_corner = sum([1 if grid[cor[0]][cor[1]] == 1 else 0 for cor in corner])
    black_corner = sum([1 if grid[cor[0]][cor[1]] == -1 else 0 for cor in corner])
    return 25 * white_corner - 25 * black_corner

# need to build dynamic weight
def static_weight_beginning(grid):

    weight = [
        [120,-20,40,5,5,40,-20,120],
        [-20,-80,-5,-5,-5,-5,-80,-20],
        [40,-5,25,3,3,25,-5,40],
        [5,-5,3,3,3,3,-5,5],
        [5,-5,3,3,3,3,-5,5],
        [40,-5,25,3,3,25,-5,40],
        [-20,-80,-5,-5,-5,-5,-80,-20],
        [120,-20,40,5,5,40,-20,120],
    ]
    res = (sum([int(grid[i][j])*int(weight[i][j]) for i in range(0,8) for j in range(0,8)]))
    return res/30

def static_weight_ending(grid):
    weight = [
        [120,-20,20,5,5,20,-20,120],
        [-20,-40,0,0,0,0,-40,-20],
        [20,0,0,0,0,0,0,20],
        [5,0,0,0,0,0,0,5],
        [5,0,0,0,0,0,0,5],
        [20,0,0,0,0,0,0,20],
        [-20,-40,0,0,0,0,-40,-20],
        [120,-20,20,5,5,20,-20,120],
    ]
    res = sum([int(grid[i][j])*int(weight[i][j]) for i in range(0,8) for j in range(0,8)])
    return res/20