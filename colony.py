from ant import Ant
from game import State

class Colony:
    def __init__(self, boardWidth, boardHeight, x=5, y=5, numAnts=3):
        self.x = x
        self.y = y
        self.ants = []
        availableSpawns = [[x-1, y-1],[x+1, y-1],[x-1, y+1],[x+1, y+1],]
        for ant in range(numAnts):
            self.ants.append(Ant(boardWidth, boardHeight, availableSpawns[ant][0], availableSpawns[ant][1]))

    def processTurn(self):
        moves = []
        for ant in self.ants:
            selectionArgs = {}
            move = ant.selectAction(selectionArgs)
            moves.extend(self.executeMove(ant, move))
        return moves

    def colonyActions(self):
        return []

    def executeMove(self, ant, move):
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
        if (newx != self.x or newy != self.y):
            ant.hunger -= 2
            setNew = {'x': newx, 'y': newy, 'newSymbol': State.ANT}
            return [clearOld, setNew]
        else:
            ant.hunger = 100
            ant.health = 100
        return []