from ant import Ant
from util import *
import copy
import random
class Colony:
    def __init__(self, boardWidth, boardHeight, x=5, y=5, numAnts=3):
        self.x = x
        self.y = y
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.ants = []
        self.food = 4
        self.health = 1000
        self.knowledge = {
            "food": [],
            "enemyColony": [],
            "enemyAnts": [],
            "homeColony": [x,y]
        }
        # availableSpawns = [[x-1, y],[x+1,y],[x, y+1],[x, y-1]]
        for ant in range(numAnts):
            self.ants.append(self.generateNeutralAnt())
    def generateNeutralAnt(self):
        return Ant(self.boardWidth, self.boardHeight, copy.deepcopy(self.knowledge), getNeutralAntGenome(), self.x, self.y)
    def generateAntFromGenome(self, genome):
        return Ant(self.boardWidth, self.boardHeight, copy.deepcopy(self.knowledge), genome, self.x, self.y)
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
            # ant.hunger -= 1
        self.useFood()
        return moves
    def useFood(self):
        if self.food >= 5:
            self.generateNewAnt()
            self.food -= 5
    def colonyActions(self):
        return []
    def generateNewAnt(self):
        log("Generating new ant")
        if (len(self.ants) == 0):
            self.ants.append(getNeutralAntGenome())
            log("No ants, generating neutral genome")
        elif (len(self.ants) == 1):
            self.ants.append(self.mutatedAnt(self.ants[0].genome, self.ants[0].genome))
            log("Only one ant, generating off of " + str(self.ants[0].genome))
        else:
            ant1 = random.choice(self.ants)
            ant2 = random.choice(self.ants)
            while(ant1.uuid != ant2.uuid):
                ant2 = random.choice(self.ants)
            log("Generating from two ants: " + str(ant1.genome) + str(ant2.genome))
            self.ants.append(self.mutatedAnt(ant1.genome, ant2.genome))
    def mutatedAnt(self, genome1, genome2):
        newGenome = {}
        for attribute in genome1.keys():
            newGenome[attribute] = (genome1[attribute] + genome2[attribute]) / 2
        mutationAttribute = random.choice(list(genome1.keys()))
        newGenome[mutationAttribute] = newGenome[mutationAttribute] * (random.random() + .5) #.5 could be higher, forces upward trend.
        return self.generateAntFromGenome(newGenome)
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
        log("My hunger is " + str(ant.hunger))
        if (newx != self.x or newy != self.y):
            ant.hunger -= 2
            if (ant.hunger <= 0):
                log("Ant Starved!")
                self.ants.remove(ant)
                return [clearOld]
            setNew = {'x': newx, 'y': newy, 'newSymbol': State.ANT}
            return [clearOld, setNew]
        else:
            #Change to the ants initial hunger.
            ant.hunger = ant.maxHunger
            ant.health = ant.maxHealth
            return [clearOld]