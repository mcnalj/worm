# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US
import random, pygame, sys
from pygame.locals import *

pygame.init()

BOARDWIDTH = 900
BOARDHEIGHT = 600
CELLSIZE = 30

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
FPS = 5
FPSCLOCK = pygame.time.Clock()

HEAD = 0 # syntactic sugar: index of the worm's head
assert BOARDWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert BOARDHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(BOARDWIDTH / CELLSIZE)
CELLHEIGHT = int(BOARDHEIGHT / CELLSIZE)

DISPLAYSURF = pygame.display.set_mode((BOARDWIDTH, BOARDHEIGHT))
DISPLAYSURF.fill(WHITE)

def checkForKeyPress():
     if len(pygame.event.get(QUIT)) > 0:
         sys.exit()
     keyUpEvents = pygame.event.get(KEYUP)
     if len(keyUpEvents) == 0:
         return None
     if keyUpEvents[0].key == K_ESCAPE:
         sys.exit()
     return keyUpEvents[0].key

def drawBoard():
    for x in range(0, BOARDWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, BOARDHEIGHT))
    for y in range(0, BOARDHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (BOARDWIDTH, y))

def getLeftTopPixel(boxX, boxY):
    left = (boxX -1) * CELLSIZE
    top = (boxY -1) * CELLSIZE
    return left, top

def drawHead(left, top):
    head = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, head)
    innerHead = pygame.Rect(left+5, top+5, CELLSIZE-10, CELLSIZE -10)
    pygame.draw.rect(DISPLAYSURF, DARKGREEN, innerHead)

def initialMovement():
    options = ["left", "right", "top", "down"]
    choice = random.randint(0,3)
    return options[choice]

def translateMovment(boxX, boxY, movement):
    if movement == "left":
        boxX = boxX - 1
    elif movement == "right":
        boxX = boxX + 1
    elif movement == "top":
        boxY = boxY - 1
    else:
        boxY = boxY + 1
    return boxX, boxY

def drawWorm(worm_path, worm_length):
    for segment in range(0,worm_length):
        left, top = getLeftTopPixel(worm_path[segment][0],worm_path[segment][1])
        drawHead(left, top)

def getTargetBoxes(boxX, boxY, worm_path):
    xTarget = random.randint(1, CELLWIDTH)
    yTarget = random.randint(1, CELLHEIGHT)
    for cell in worm_path:
        if (xTarget == cell[0] and yTarget == cell[1]) or (xTarget == boxX and yTarget == boxY):
            xTarget, yTarget = getTargetBoxes(boxX, boxY, worm_path)
            return xTarget, yTarget
    return xTarget, yTarget

def drawTargetBox(left, top):
    target = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, target)

def drawTarget(worm_path):
    x, y = getTargetBoxes(worm_path)
    left, top = getLeftTopPixel(x, y)
    drawTargetBox(x, y)

def fillWormPath(worm_path, movement):
    if movement == "right":
        worm_path = [(9, 10), (8, 10), (7, 10)]
    if movement == "left":
        worm_path = [(11, 10), (12, 10), (13, 10)]
    if movement == "top":
        worm_path = [(10, 11), (10, 12), (10, 13)]
    if movement == "down":
        worm_path = [(10, 9), (10, 8), (10, 7)]
    return worm_path

def checkGameOver(boxX, boxY, worm_path):
    running = True
    if (boxX < 1 or boxX > CELLWIDTH) or boxY < 1 or boxY > CELLHEIGHT:
        gameOverMessage()
        pygame.time.wait(4000)
        running = False
    if worm_path:
        for segment in worm_path:
            if boxX == segment[0] and boxY == segment[1]:
                gameOverMessage()
                pygame.time.wait(4000)
                running = False
    return running

def gameOverMessage():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('GAME', True, WHITE)
    overSurf = gameOverFont.render('OVER', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (BOARDWIDTH / 2, 10)
    overRect.midtop = (BOARDWIDTH / 2, gameRect.height + 35)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    pygame.display.flip()

def main(FPS):
    movement = initialMovement()
    boxX = 10
    boxY = 10
    running = True
    worm_length = 0
    worm_path = []
    #worm_path = fillWormPath(worm_path, movement)
    head_tuple = ()
    xTarget = 3
    yTarget = 4
    targetLeft, targetTop = getLeftTopPixel(xTarget, yTarget)
    score = 0

    while running:
        if worm_length > 13:
            FPS = 13
        elif worm_length > 9:
            FPS = 12
        elif worm_length > 6:
            FPS = 11
        elif worm_length > 4:
            FPS = 9
        elif worm_length > 2:
            FPS = 7
        DISPLAYSURF.fill(BGCOLOR)
        head_tuple = (boxX, boxY)
        worm_path.insert(0, head_tuple)
        if len(worm_path) > worm_length:
            worm_path.pop()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_LEFT and movement != "right":
                    movement = "left"
                elif event.key == K_RIGHT and movement != "left":
                    movement = "right"
                elif event.key == K_UP and movement != "down":
                    movement = "top"
                elif event.key == K_DOWN and movement != "top":
                    movement = "down"

        drawBoard()
        boxX, boxY = translateMovment(boxX, boxY, movement)
        left, top = getLeftTopPixel(boxX, boxY)
        drawHead(left, top)
        drawWorm(worm_path, worm_length)
        print(boxX, boxY)
        running = checkGameOver(boxX, boxY, worm_path)
        if boxX == xTarget and boxY == yTarget:
            xTarget, yTarget = getTargetBoxes(boxX, boxY, worm_path)
            targetLeft, targetTop = getLeftTopPixel(xTarget, yTarget)
            worm_length = worm_length + 1
            score = score + 10
        drawTargetBox(targetLeft, targetTop)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)

main(FPS)
sys.exit()
