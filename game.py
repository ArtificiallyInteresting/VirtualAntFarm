from enum import Enum
class Game:
    def __init__(self, colony, width=400, height=200):
        self.initBoard(width, height)
        self.colony = colony
    # Board is 2d array. X,Y with 0,0 being bottom left corner
    # I don't like row/column. Fite me.
    def initBoard(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(State.DIRT)
            self.board.append(row)

    def processTurn(self):
        moves = self.colony.processTurn()
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
            self.board[move['x']][move['y']] = move['newSymbol']
class State(Enum):
    DIRT = 1
    EMPTY = 2
    FOOD = 3
    ANT = 4



