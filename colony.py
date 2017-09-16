from ant import Ant
from util import *
import copy
class Colony:
    def __init__(self, boardWidth, boardHeight, x=5, y=5, numAnts=3):
        self.x = x
        self.y = y
        self.ants = []
        self.food = 0
        self.knowledge = {
            "food": [],
            "enemyColony": [],
            "enemyAnts": [],
            "homeColony": [x,y]
        }
        availableSpawns = [[x-1, y],[x+1,y],[x, y+1],[x, y-1]]
        for ant in range(numAnts):
            self.ants.append(Ant(boardWidth, boardHeight, copy.deepcopy(self.knowledge), availableSpawns[ant][0], availableSpawns[ant][1]))
    def getBoardAroundAnt(self, ant, board):
        newBoard = {}
        if ant.y < len(board[0]) - 1:
            newBoard[str(ant.x) + "," + str(ant.y + 1)] = board[ant.x][ant.y+1]
        if ant.y > 0:
            newBoard[str(ant.x) + "," + str(ant.y - 1)] = board[ant.x][ant.y-1]
        if ant.x < len(board) - 1:
            newBoard[str(ant.x + 1) + "," + str(ant.y)] = board[ant.x+1][ant.y]
        if ant.x > 0:
            newBoard[str(ant.x - 1) + "," + str(ant.y)] = board[ant.x-1][ant.y]
        newBoard[str(ant.x) + "," + str(ant.y)] = board[ant.x][ant.y]
        return newBoard
    def processTurn(self, board):
        moves = []
        for ant in self.ants:
            selectionArgs = {"board": self.getBoardAroundAnt(ant, board)}
            ant.updateKnowledge(selectionArgs)
            move = ant.selectAction(selectionArgs)
            moves.extend(self.executeMove(ant, move, board))
            ant.health -= 1
        return moves

    def colonyActions(self):
        return []

    def executeMove(self, ant, move, board):
        clearOld = {'x': ant.x, 'y': ant.y, 'newSymbol': State.EMPTY}
        newx = ant.x
        newy = ant.y
        if move == 'E':
            newx += 1
        elif move == 'W':
            newx -= 1
        elif move == 'N':
            newy += 1
        elif move == 'S':
            newy -= 1
        ant.x = newx
        ant.y = newy
        #Refactor this to game.py
        if (board[newx][newy] == State.FOOD):
            ant.hasFood = True
        if (board[newx][newy] == State.COLONY):
            ant.hasFood = False
            self.food += 1
        if (newx != self.x or newy != self.y):
            ant.hunger -= 2
            setNew = {'x': newx, 'y': newy, 'newSymbol': State.ANT}
            return [clearOld, setNew]
        else:
            ant.hunger = 100
            ant.health = 100
            return [clearOld]