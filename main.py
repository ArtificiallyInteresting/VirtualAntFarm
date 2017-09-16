from game import Game
from colony import Colony
from window import Window
import pygame
def startGame():
    window = Window(width=800, height=600)
    game = Game(width=40, height=20)
    clock = pygame.time.Clock()
    while(not game.finished()):
        clock.tick(1)
        game.processTurn()
        window.update(game.board)

if __name__ == '__main__':
    startGame()