from enum import Enum
def log(message):
    print(message)

class AntState:
    GETFOOD = "GETFOOD"
    RETURNTOBASE = "RETURNTOBASE"
    EXPLORE = "EXPLORE"
    FIGHTANT = "FIGHTANT"
    FIGHTCOLONY = "FIGHTCOLONY"

class State(Enum):
    DIRT = 1
    EMPTY = 2
    FOOD = 3
    ANT = 4
    COLONY = 5

def getNewPosition(currentPos, move):
    newx = currentPos[0]
    newy = currentPos[1]
    if move == 'E':
        newx += 1
    elif move == 'W':
        newx -= 1
    elif move == 'N':
        newy += 1
    elif move == 'S':
        newy -= 1
    return [newx, newy]

def removeValuesFromList(theList, val):
   return [value for value in theList if value != val]
