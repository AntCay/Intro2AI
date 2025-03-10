from settings import *

def getPixelCoordinates(row, col):
    x = col * CELL_SIZE * 0.6 + 100
    y = row * CELL_SIZE * 1 + 100
    return x, y

def engineToBoard(position):
    x, y = position
    boardPos = None
    if y == 0:
        boardPos = (8+x, 4+x)
    elif y == 1:
        boardPos = (7+x, 5+x)
    elif y == 2:
        boardPos = (6+x, 6+x)
    elif y == 3:
        boardPos = (5+x, 7+x)
    elif y == 4:
        boardPos = (4+x, 8+x)
    elif y == 5:
        boardPos = (3+x, 9+x)
    elif y == 6:
        boardPos = (2+x, 10+x)
    elif y == 7:
        boardPos = (1+x, 11+x)
    elif y == 8:
        boardPos = (0+x, 12+x)
    return boardPos

def boardToEngine(position):
    x, y = position
    enginePos = None
    if y-x == -4:
        enginePos = (x - 8, 0)
    elif y-x == -2:
        enginePos = (x - 7, 1)
    elif y-x == 0:
        enginePos = (x - 6, 2)
    elif y-x == 2:
        enginePos = (x - 5, 3)
    elif y-x == 4:
        enginePos = (x - 4, 4)
    elif y-x == 6:
        enginePos = (x - 3, 5)
    elif y-x == 8:
        enginePos = (x - 2, 6)
    elif y-x == 10:
        enginePos = (x - 1, 7)
    elif y-x == 12:
        enginePos = (x - 0, 8)        
    return enginePos
