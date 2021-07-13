from Const import WIDTH,HEIGHT
import pygame, sys

class Game:

    def __init__(self):
        pygame.init()

        self.canvas = pygame.display.set_mode((WIDTH,HEIGHT))
        self.canvas.fill((255,255,255))
        pygame.display.set_caption("Minesweeper")
        pygame.display.flip()
        self.running = True

    def run(self):
        while self.running:
            #do stuff
            continue
        pygame.quit()
        sys.exit(0)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False