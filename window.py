import pygame
from pygame.locals import *
from game import State
class Window:
    def __init__(self, width=400, height=200, rows=20, cols=40):
        self.width = width
        self.height = height
        self.infoHeight = .25 * height
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((width, height))
        # create a new Surface
        self.surface = pygame.Surface((width, height))
        self.boardPercentage = .75

        # change its (background) color
        self.surface.fill((55, 155, 255))

        # blit myNewSurface onto the main screen at the position (0, 0)
        self.display.blit(self.surface, (0, 0))

        self.maxX = cols
        self.maxY = rows
        self.xSize = self.width/float(self.maxX)
        self.ySize = ((self.height)/float(self.maxY)) * self.boardPercentage

        # update the sreen to display the changes
        pygame.display.flip()
        self.images = {
            'blueAnt': pygame.image.load('images/blueAnt.png').convert(),
            'redAnt': pygame.image.load('images/redAnt.png').convert(),
            'blueBase': pygame.image.load('images/blueBase.png',).convert(),
            'redBase': pygame.image.load('images/redBase.png').convert(),
            'dirt': pygame.image.load('images/dirt.png').convert(),
            'food': pygame.image.load('images/food.png').convert(),
            'tunnel': pygame.image.load('images/tunnel.png').convert()
        }

    def update(self, board, colonies):
        pygame.event.get()
        for x in range(self.maxX):
            for y in range(self.maxY):
                left = x * self.xSize
                # Maybe use self.boardHeight instead of calculating on height and infoHeight?
                top = (self.height - ((y + 1) * self.ySize)) - self.infoHeight
                self.surface.blit(self.getImage(board[x][y], x, y, colonies), (left, top))
                # pygame.draw.rect(self.surface, self.getColor(board[x][y], x, y, colonies), (left, top, xSize, ySize))
        for ant in colonies[0].ants + colonies[1].ants:
            self.drawName(ant, board)
        self.drawInfo(board, colonies)
        #White visual separator
        pygame.draw.rect(self.surface, (255,255,255), (0, self.height-self.infoHeight-1, self.width, 2))
        self.display.blit(self.surface, (0, 0))
        pygame.display.flip()
    def drawInfo(self, board, colonies):
        pygame.draw.rect(self.surface, (0,0,0),(0, self.height - self.infoHeight, self.width, self.infoHeight))
        antsPerColumn = 3
        i = 0
        for ant in colonies[0].ants:
            self.drawAntStats(ant, 'red', i%antsPerColumn, int(i/antsPerColumn))
            i += 1
        i = 0
        for ant in colonies[1].ants:
            self.drawAntStats(ant, 'blue', i%antsPerColumn, int(i/antsPerColumn))
            i += 1

    def drawAntStats(self, ant, color, numberY, numberX):
        widthOfColumn = 150
        myfont = pygame.font.SysFont('Deja Vu Sans Mono', 10)
        attributes = ['hunger', 'maxHunger', 'health', 'maxHealth']
        antString = ant.name
        textsurface = myfont.render(antString, False, (255, 255, 255))
        x = 0 if color == 'red' else self.width/2
        x += numberX * widthOfColumn
        startingHeight = self.height-self.infoHeight+(10*numberY*(len(attributes)+2))
        self.surface.blit(textsurface, (x, startingHeight))
        i = 1
        for attribute in attributes:
            displayName = self.getDisplayName(attribute)
            textsurface = myfont.render(displayName + ': ' + str(getattr(ant, attribute)), False, (255, 255, 255))
            self.surface.blit(textsurface, (x+10, startingHeight + (10*i)))
            i += 1

    def getDisplayName(self, attribute):
        attributes = {
            'hunger': 'Food',
            'maxHunger': 'Max Food',
            'health': 'Health',
            'maxHealth': 'Max Health'
        }
        if attribute not in attributes.keys():
            return attribute
        return attributes[attribute]

    def drawName(self, ant, board):
        pixelsPerChar = 7
        textWidth = len(ant.name) * pixelsPerChar
        left = ant.x * self.xSize
        midX = left + (self.xSize/2)
        top = (self.height - ((ant.y + 1) * self.ySize)) - self.infoHeight
        myfont = pygame.font.SysFont('Deja Vu Sans Mono', 10)
        #Back surface
        pygame.draw.rect(self.surface, (255,255,255),(midX - textWidth/2, top-10, textWidth, self.ySize/2))
        textsurface = myfont.render(ant.name, False, (0, 0, 0))
        self.surface.blit(textsurface, (midX - textWidth/2, top-10))

    def displayGameOver(self):

        myfont = pygame.font.SysFont('Calibri', 50)
        textsurface = myfont.render('GAME OVER', False, (0, 0, 0))
        self.display.blit(textsurface, (self.width/2 - 100, self.height/2 - 50))
        pygame.display.flip()

    def getImage(self, s, x, y, colonies):
        if s == State.DIRT:
            return self.images['dirt']
        elif s == State.ANT:
            return 	self.getAntImage(x,y,colonies)
        elif s == State.EMPTY:
            return self.images['tunnel']
        elif s == State.FOOD:
            return self.images['food']
        elif s == State.COLONY:
            return self.getColonyImage(x, y, colonies)
    def getAntImage(self, x, y, colonies):
        for ant in colonies[0].ants:
            if (ant.x == x and ant.y == y):
                return self.images['redAnt']
        return self.images['blueAnt']
    def getColonyImage(self, x, y, colonies):
        if (x == colonies[0].x and y == colonies[0].y):
            return self.images['redBase']
        else:
            return self.images['blueBase']

    def getColor(self, s, x, y, colonies):
        if s == State.DIRT:
            return (139,69,19)
        elif s == State.ANT:
            return 	self.getAntColor(x,y,colonies)
        elif s == State.EMPTY:
            return (0,0,255)
        elif s == State.FOOD:
            return (0,255,0)
        elif s == State.COLONY:
            return self.getColonyColor(x, y, colonies)
    def getAntColor(self, x, y, colonies):
        for ant in colonies[0].ants:
            if (ant.x == x and ant.y == y):
                return (255, 0, 0)
        return (255, 0, 255)
    def getColonyColor(self, x, y, colonies):
        if (x == colonies[0].x and y == colonies[0].y):
            return (0,255,255)
        else:
            return (255,255,0)

