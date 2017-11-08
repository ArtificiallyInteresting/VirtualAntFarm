import random
import math
import copy
from util import *
class Ant:
    def __init__(self, boardWidth, boardHeight, knowledge, genome, x=2, y=2):
        self.uuid = random.randint(0, 999999999999)
        self.x = x
        self.y = y
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.state = AntState.EXPLORE
        self.knowledge = knowledge
        self.hasFood = False
        self.visitedOnThisTrip = []
        self.goalPoint = []
        self.pathBackToBase = []
        self.maxHealth = genome["startingHealth"]
        self.maxHunger = genome["startingHunger"]
        self.health = self.maxHealth
        self.hunger = self.maxHunger
        self.genome = genome
        self.name = randomName()

    def updateKnowledge(self, selectionArgs):
        antBoard = selectionArgs["board"]
        for key in antBoard.keys():
            if antBoard[key] == State.FOOD and not key.split(',') in self.knowledge["food"]:
                self.knowledge["food"].append([int(k) for k in key.split(',')])
            if antBoard[key] == State.COLONY and self.knowledge["enemyColony"] == [] and self.knowledge["homeColony"] != [int(k) for k in key.split(',')]:
                self.knowledge["enemyColony"] = [int(k) for k in key.split(',')]
        if ([self.x, self.y] in self.knowledge["food"]):
            # self.knowledge["food"].remove([self.x, self.y])
            self.knowledge["food"] = removeValuesFromList(self.knowledge["food"], [self.x, self.y])
    def reorderMoves(self, oldMoves, newMoveOrder):
        newMoves = []
        for move in newMoveOrder:
            if move in oldMoves:
                newMoves.append(move)
        return newMoves
    def sortMoves(self, moves, location, moveAwayFrom):
        vector = [location[0]-moveAwayFrom[0], location[1]-moveAwayFrom[1]]
        moveOrder = []
        if (abs(vector[0]) > abs(vector[1])):
            # East/West is more important than North/South
            if (vector[0] > 0):
                if (vector[1] > 0):
                    moveOrder = ['E', 'N', 'S', 'W']
                else:
                    moveOrder = ['E', 'S', 'N', 'W']
            else:
                if (vector[1] > 0):
                    moveOrder = ['W', 'N', 'S', 'E']
                else:
                    moveOrder = ['W', 'S', 'N', 'E']
        else:
            if (vector[1] > 0):
                if (vector[0] > 0):
                    moveOrder = ['N', 'E', 'W', 'S']
                else:
                    moveOrder = ['N', 'W', 'E', 'S']
            else:
                if (vector[0] > 0):
                    moveOrder = ['S', 'E', 'W', 'N']
                else:
                    moveOrder = ['S', 'W', 'E', 'N']
        return self.reorderMoves(moves, moveOrder)

    def generateGoalPoint(self):
        self.goalPoint = [random.randint(0, self.boardWidth-1), random.randint(0, self.boardHeight-1)]
    def selectAction(self, selectionArgs):
        antBoard = selectionArgs["board"]
        enemyCol = self.knowledge["enemyColony"]
        homeCol = self.knowledge["homeColony"]
        action = ""
        self.transitionStates(antBoard)
        log("My state is " + str(self.state))
        if self.state == AntState.EXPLORE:
            if (self.goalPoint == [] or (self.x == self.goalPoint[0] and self.y == self.goalPoint[1])):
                self.generateGoalPoint()
            log("I'm exploring towards " + str(self.goalPoint) + ". Currently at " + str([self.x, self.y]))
            action = self.moveTowards(self.goalPoint, antBoard, tunnelsOnly=False)
            # # Should this just be random out of just dirt or all?
            # moves = self.getValidMoves()
            # # random.shuffle(moves)
            # moves = self.sortMoves(moves, [self.x, self.y], homeCol)
            # action = random.choice(self.getValidMoves())
            # for move in moves:
            #     pos = getNewPosition([self.x, self.y], move)
            #     strPos = str(pos[0]) + "," + str(pos[1])
            #     if strPos in antBoard: # and antBoard[strPos] == State.DIRT:
            #         action = move
            #         break
        elif self.state == AntState.FIGHTANT:
            action = 'E' #Should be direction of ant
        elif self.state == AntState.FIGHTCOLONY:
            enemyCol = self.knowledge["enemyColony"]
            if enemyCol == []:
                print("I was told to attack the enemy colony, but I don't know where it is")
                action = random.choice(self.getValidMoves())
            else:
                action = self.moveTowards(enemyCol, antBoard, backtrack=False)
        elif self.state == AntState.GETFOOD:
            action = self.moveTowards(self.getClosestFood(), antBoard, tunnelsOnly=False)
        elif self.state == AntState.RETURNTOBASE:
            action = self.pathBackToBase.pop()
            # action = self.moveTowards(homeCol, antBoard, backtrack=False)
            # action = self.moveTowards(homeCol, antBoard, tunnelsOnly=False)
        # Move to function
        if self.state != AntState.RETURNTOBASE:
            if action == 'N':
                actionBack = 'S'
            if action == 'S':
                actionBack = 'N'
            if action == 'W':
                actionBack = 'E'
            if action == 'E':
                actionBack = 'W'
            self.pathBackToBase.append(actionBack)
        # log("My path back is " + str(self.pathBackToBase))
        return action

    def transitionStates(self, antBoard):
        if self.state == AntState.EXPLORE:
            if (len(self.knowledge["food"]) > 0):
                self.state = AntState.GETFOOD
            elif (self.shouldRetreat()):
                self.visitedOnThisTrip = []
                self.state = AntState.RETURNTOBASE
            elif(self.knowledge["enemyColony"] != []):
                self.state = AntState.FIGHTCOLONY
        elif self.state == AntState.FIGHTANT:
            if (self.shouldRetreat()):
                self.visitedOnThisTrip = []
                self.state = AntState.RETURNTOBASE
        elif self.state == AntState.FIGHTCOLONY:
            if (self.shouldRetreat()):
                self.visitedOnThisTrip = []
                self.state = AntState.RETURNTOBASE
        elif self.state == AntState.GETFOOD:
            if (self.hasFood):
                self.visitedOnThisTrip = []
                self.state = AntState.RETURNTOBASE
            elif (len(self.knowledge["food"]) == 0):
                self.state = AntState.EXPLORE
        elif self.state == AntState.RETURNTOBASE:
            if (self.x == self.knowledge['homeColony'][0] and self.y == self.knowledge['homeColony'][1]):
                self.state = AntState.EXPLORE if len(self.knowledge['food']) == 0 else AntState.GETFOOD

    def shouldRetreat(self):
        # Later on, this should involve random mutations. For now, just go back when you should
        # distToCol = (self.x - self.knowledge["homeColony"][0]) + (self.y - self.knowledge["homeColony"][1])
        return self.health < self.maxHealth

    def getClosestFood(self):
        closestFood = []
        closestDist = 999999999999
        for food in self.knowledge["food"]:
            dist = abs(food[0]-self.x) + abs(food[1]-self.y)
            if dist < closestDist:
                closestDist = dist
                closestFood = copy.copy(food)
        return closestFood


    def moveTowards(self, newLocation, antBoard, tunnelsOnly=True, backtrack = True):
        validMoves = self.getValidMoves()
        if 'W' in validMoves and not (newLocation[0] < self.x):
            validMoves.remove('W')
        if 'E' in validMoves and not (newLocation[0] > self.x):
            validMoves.remove('E')
        if 'S' in validMoves and not (newLocation[1] < self.y):
            validMoves.remove('S')
        if 'N' in validMoves and not (newLocation[1] > self.y):
            validMoves.remove('N')
        if len(validMoves) > 0:
            random.shuffle(validMoves)
            for move in validMoves:
                [newx, newy] = getNewPosition([self.x, self.y], move)
                posString = str(newx) + "," + str(newy)
                if posString in antBoard and (antBoard[posString] == State.EMPTY or antBoard[posString] == State.COLONY):
                    if backtrack or posString not in self.visitedOnThisTrip:
                        self.visitedOnThisTrip.append(posString)
                        return move
        if (validMoves == []):
            # There really should be a better solution than juts randomly moving.
            validMoves = self.getValidMoves()
        if (tunnelsOnly):
            #This can get stuck
            #do over, but don't try to go towards the goal at all
            #this code was copied from above (refactor?)
            validMoves = self.getValidMoves()
            random.shuffle(validMoves)
            for move in validMoves:
                [newx, newy] = getNewPosition([self.x, self.y], move)
                posString = str(newx) + "," + str(newy)
                if posString in antBoard and (antBoard[posString] == State.EMPTY or antBoard[posString] == State.COLONY):
                    if backtrack or posString not in self.visitedOnThisTrip:
                        self.visitedOnThisTrip.append(posString)
                        return move

        return random.choice(validMoves)

    def getValidMoves(self):
        moves = []
        if self.x > 0:
            moves.append('W')
        # Am I off by one here?
        if self.x < self.boardWidth:
            moves.append('E')
        if self.y > 0:
            moves.append('S')
        if self.y < self.boardHeight:
            moves.append('N')
        return moves

