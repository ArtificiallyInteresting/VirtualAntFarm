from colony import Colony
import random
from util import *
import numpy as np
class Game:
    def __init__(self, width=400, height=200):
        self.initBoard(width, height)
    # Board is 2d array. X,Y with 0,0 being bottom left corner
    # I don't like row/column. Fite me.
    def initBoard(self, width, height):
        self.width = width
        self.colonies = [Colony(40, 20, numAnts=1), Colony(40, 20, x = 35, y = 5,numAnts=1)]
        self.height = height
        self.board = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(State.DIRT)
            self.board.append(row)
        self.addFood(80)
        for colony in self.colonies:
            self.board[colony.x][colony.y] = State.COLONY

    def addFood(self, numFood):
        for food in range(numFood):
            # x = random.randint(0,self.width-1)
            # y = random.randint(0,self.height-1)
            x,y = self.getRandomFoodLocation()
            # Check that this isn't already food.
            self.board[x][y] = State.FOOD
    def getRandomFoodLocation(self):
        x = random.randint(0, self.width - 1)
        y = 99999999
        while (y > self.height):
            y = abs(np.random.normal(0, scale=.5* self.height))
        return int(x),int(self.height - y)



    def processTurn(self):
        moves = []
        for colony in self.colonies:
            moves.extend(colony.processTurn(self.board))
        self.processMoves(moves)
        self.processAntAttacks()

    #Generalize to more than 2 colonies
    def processAntAttacks(self):
       if (len(self.colonies) == 1):
           return
       colony1 = self.colonies[0]
       colony2 = self.colonies[1]
       for ant in colony1.ants:
            for otherant in colony2.ants:
                if (ant.x == otherant.x and ant.y == otherant.y):
                    #Should be based on strength, not just health.
                    if (ant.health > otherant.health):
                        ant.health = ant.health - otherant.health
                        colony2.ants.remove(otherant)
                    else:
                        otherant.health = otherant.health - ant.health
                        colony1.ants.remove(ant)
       for ant in colony1.ants:
           if (ant.x == colony2.x and ant.y == colony2.y):
               colony2.health -= ant.health
       for ant in colony2.ants:
           if (ant.x == colony1.x and ant.y == colony1.y):
               colony1.health -= ant.health

    def finished(self):
        for colony in self.colonies:
            if colony.health <= 0:
                return True
            if len(colony.ants) == 0:
                return True
        return False

    def processMoves(self, moves):
        for move in moves:
                self.processMove(move)

    #This should also be validating moves
    def processMove(self, move):
        if (move['x'] < 0 or move['x'] > self.width-1 or move['y'] < 0 or move['y'] > self.height-1):
            print("Move rejected!")
        else:
            if (self.board[move['x']][move['y']] != State.COLONY):
                self.board[move['x']][move['y']] = move['newSymbol']




