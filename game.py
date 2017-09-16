from colony import Colony
import random
from util import *
class Game:
    def __init__(self, width=400, height=200):
        self.initBoard(width, height)
    # Board is 2d array. X,Y with 0,0 being bottom left corner
    # I don't like row/column. Fite me.
    def initBoard(self, width, height):
        self.width = width
        self.colony = Colony(40, 20, numAnts=1)
        self.height = height
        self.board = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(State.DIRT)
            self.board.append(row)
        self.addFood(80)
        self.board[self.colony.x][self.colony.y] = State.COLONY

    def addFood(self, numFood):
        for food in range(numFood):
            x = random.randint(0,self.width-1)
            y = random.randint(0,self.height-1)
            # Check that this isn't already food.
            self.board[x][y] = State.FOOD


    def processTurn(self):
        moves = self.colony.processTurn(self.board)
        self.processMoves(moves)

    def finished(self):
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




