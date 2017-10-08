from game import Game
from colony import Colony
from window import Window
import pygame
import time
def startGame():
    window = Window(width=800, height=600)
    clock = pygame.time.Clock()
    while(True):
        game = Game(width=40, height=20)
        while(not game.finished()):
            clock.tick(1)
            game.processTurn()
            window.update(game.board, game.colonies)
        endtime = time.time()
        window.displayGameOver()
        while time.time() < endtime + 5:
            pass

if __name__ == '__main__':
    startGame()