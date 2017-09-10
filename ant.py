import random
class Ant:
    def __init__(self, boardWidth, boardHeight, x=2, y=2):
        self.x = x
        self.y = y
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.health = 100
        self.hunger = 100
    def selectAction(self, selectionArgs):
        return random.choice(self.getValidMoves())
    def getValidMoves(self):
        moves = []
        if self.x > 0:
            moves.append('W')
        # Am I off by one here?
        if self.x < self.boardWidth:
            moves.append('E')
        if self.y > 0:
            moves.append('N')
        if self.y < self.boardHeight:
            moves.append('S')
        return moves
    def getEmptyInput(self):
        # Some of these should be properties of the ant instead of inputs
        return {
            'Hunger': 1,
            'Depth': 1,
            'DistanceToBase': 1,
            'ClosestEnemy': 1,
            'Health': 1
        }