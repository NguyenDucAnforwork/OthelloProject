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

# necessary conditions
def stableDisc(grid, player):
    pairDirections = [[[0,1], [0,-1]], [[-1,0], [1,0]], [[1,1], [-1,-1]], [[-1,1], [1,-1]]]
    discCoor = []
    for gridX, row in enumerate(grid):
        for gridY, col in enumerate(row):
            if grid[gridX][gridY] == player:
                discCoor.append([gridX, gridY])
    result = []
    for coor in discCoor:
        X, Y = coor[0], coor[1]
        check = True

        for pair in pairDirections:
            checkLeft = True
            checkRight = True
            left = pair[0]
            right = pair[1]
            leftX, leftY = left[0], left[1]
            rightX, rightY = right[0], right[1]
            while True:
                X, Y = X + leftX, Y + leftY
                if X * (X - 7) > 0 or Y * (Y - 7) > 0:
                    break
                if grid[X][Y] != player:
                    checkLeft = False
                    break
            X, Y = coor[0], coor[1]
            
            while True:
                X, Y = X + rightX, Y + rightY
                if X * (X - 7) > 0 or Y * (Y - 7) > 0:
                    break
                if grid[X][Y] != player:
                    checkRight = False
                    break

            if not checkLeft and not checkRight:
                check = False
        if check:
            result.append(coor)
    return result 
            
def convertReporttoGame():
    pass

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
    unstableCell = []

    for cell in validCells:
        x, y = cell
        if cell in playableCells:
            continue
        swapTiles = swappableTilesGlobal(x, y, grid, currentPlayer)
        if len(swapTiles) > 0:
            playableCells.append(cell)
            for element in swapTiles:
                if element not in unstableCell:
                    unstableCell.append(swapTiles)

    return playableCells, unstableCell


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



