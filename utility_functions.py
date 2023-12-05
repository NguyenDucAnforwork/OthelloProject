import pygame
import random
import copy

def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Check to determine which directions are valid from current cell"""
    validdirections = []
    if x != minX: validdirections.append((x-1, y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))

    if x!= maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))

    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))

    return validdirections

def findValidCellsGlobal(grid, curPlayer):
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in validCellToClick:          # is this necessary?
                        continue

                    validCellToClick.append((gridX, gridY))
        return validCellToClick

def swappableTilesGlobal(x, y, grid, player):
        surroundCells = directions(x, y)
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False     # we search along the same direction and stops when got the same color as (x,y)
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)

        return swappableTiles

def findAvailMovesGlobal(grid, currentPlayer):
        validCells = findValidCellsGlobal(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = swappableTilesGlobal(x, y, grid, currentPlayer)
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells

def loadImages(path, size):
    """Load an image into the game, and scale the image"""
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    """creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img"""
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image

def coin_party(grid):
    black_piece = sum([1 if num == -1 else 0 for row in grid for num in row])
    white_piece = sum([1 if num == 1 else 0 for row in grid for num in row]) 
 
    res = 100 * (white_piece - black_piece) / (white_piece + black_piece)
    return res

def mobility(grid):
    # actual/potential mobility: For simplicity I would use the most simple form
    whiteAvailableMoves = len(findAvailMovesGlobal(grid, 1))
    blackAvailableMoves = len(findAvailMovesGlobal(grid, -1))
    if whiteAvailableMoves + blackAvailableMoves > 0:
        return 100 * (whiteAvailableMoves - blackAvailableMoves) / (whiteAvailableMoves + blackAvailableMoves)
    else:
        return 0

# stable, semi-stable, unstable
def stability(grid):
    # stable

    # semi-stable

    # unstable
    pass

# we definitely need to experiment some pairs of weights
def corner_closeness(grid):
    coordinates = {
        [0,1], [1,0],
        [0,6], [1,7],
        [6,0], [7,1],
        [6,7], [7,6]
    }

    white_pieces = sum([1 if grid[coor[0]][coor[1]] == 1 else 0 for coor in coordinates])
    black_pieces = sum([1 if grid[coor[0]][coor[1]] == -1 else 0 for coor in coordinates])

    return -12.5 * white_pieces + 12.5 * black_pieces

# need to build dynamic weight
def static_weight(grid):
    print(grid)
    weight = [
        [120,-20,20,5,5,20,-20,120],
        [-20,-40,-5,-5,-5,-5,-40,-20],
        [20,-5,15,3,3,15,-5,20],
        [5,-5,3,3,3,3,-5,5],
        [5,-5,3,3,3,3,-5,5],
        [20,-5,15,3,3,15,-5,20],
        [-20,-40,-5,-5,-5,-5,-40,-20],
        [120,-20,20,5,5,20,-20,120],
    ]
    res = print(sum([int(grid[i][j])*int(weight[i][j]) for i in range(0,8) for j in range(0,8)]))
    return res