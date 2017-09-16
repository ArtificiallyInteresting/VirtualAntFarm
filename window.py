import pygame
from pygame.locals import *
from game import State
class Window:
    def __init__(self, width=400, height=200):
        self.width = width
        self.height = height
        pygame.init()
        self.display = pygame.display.set_mode((width, height))
        # create a new Surface
        self.surface = pygame.Surface((width, height))

        # change its (background) color
        self.surface.fill((55, 155, 255))

        # blit myNewSurface onto the main screen at the position (0, 0)
        self.display.blit(self.surface, (0, 0))

        # update the sreen to display the changes
        pygame.display.flip()

    def update(self, board):
        pygame.event.get()
        maxX = len(board)
        maxY = len(board[0])
        xSize = self.width/float(maxX)
        ySize = (self.height)/float(maxY)
        for x in range(maxX):
            for y in range(maxY):
                left = x * xSize
                top = self.height - ((y + 1) * ySize)
                pygame.draw.rect(self.surface, self.getColor(board[x][y]), (left, top, xSize, ySize))
        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()

    def getColor(self, s):
        if s == State.DIRT:
            return (139,69,19)
        elif s == State.ANT:
            return 	(255,0,0)
        elif s == State.EMPTY:
            return (0,0,255)
        elif s == State.FOOD:
            return (0,255,0)
        elif s == State.COLONY:
            return (0,255,255)

