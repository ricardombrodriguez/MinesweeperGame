from Const import *
from Cell import Cell
import pygame, sys, random

class Game:

    def __init__(self):
        pygame.init()
        self.running = True
        self.canvas = pygame.display.set_mode((WIDTH,HEIGHT))
        self.canvas.fill(WHITE)
        pygame.display.set_caption("Minesweeper")
        pygame.display.flip()
        self.createCells()

    def run(self):
        while self.running:
            self.events()
        pygame.quit()
        sys.exit(0)

    # Create cells
    def createCells(self):
        self.grid = [[None for col in range(COL_CELLS)] for row in range(ROW_CELLS)] 
        self.createBombs()
        self.createDefault()
        self.drawCanvas()

    # Creating bombs
    def createBombs(self):
        num_cells = ROW_CELLS * COL_CELLS
        num_bombs = NUM_BOMBS
        while num_bombs != 0:
            randnum = random.randint(0,num_cells-1)
            if self.grid[randnum//COL_CELLS][randnum%COL_CELLS] is None:
                cell_bomb = Cell("BOMB")
                self.grid[randnum//COL_CELLS][randnum%COL_CELLS] = cell_bomb
                num_bombs -= 1

    # Creating default/non-bomb cells
    def createDefault(self):
        for row in range(0,ROW_CELLS):
            for column in range(0,COL_CELLS):
                if self.grid[row][column] is None:
                    cell = Cell("DEFAULT")
                    self.grid[row][column] = cell
        print("done create default")

    # Draw canvas/grid
    def drawCanvas(self):
        pygame.draw.rect(self.canvas, BLACK, (GRID_POS[0], GRID_POS[1], GRID_WIDTH, GRID_HEIGHT), 2)
        for x in range(COL_CELLS):
            pygame.draw.line(self.canvas, BLACK, (GRID_POS[0]+(x*CELL_SIZE), GRID_POS[1]), (GRID_POS[0]+(x*CELL_SIZE), GRID_POS[1]+GRID_HEIGHT), 1)
        for y in range(ROW_CELLS):
            pygame.draw.line(self.canvas, BLACK, (GRID_POS[0], GRID_POS[1]+(y*CELL_SIZE)), (GRID_POS[0]+GRID_WIDTH, GRID_POS[1]+(y*CELL_SIZE)), 1)
        pygame.display.flip()
        print("canvas draw done")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False