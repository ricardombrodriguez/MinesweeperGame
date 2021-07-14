from pygame.constants import GL_CONTEXT_FORWARD_COMPATIBLE_FLAG
from Const import *
from Cell import Cell
import pygame, sys, random

class Game:

    # Initial game settings
    def __init__(self):
        pygame.init()
        self.running = True
        self.canvas = pygame.display.set_mode((WIDTH,HEIGHT))
        self.canvas.fill(WHITE)
        pygame.display.set_caption("Minesweeper")
        pygame.display.flip()
        self.createCells()

    # Game start/end
    def run(self):
        while self.running:
            self.events()
        pygame.quit()
        sys.exit(0)

    # Create cells
    def createCells(self):
        self.grid = [[None for col in range(COL_CELLS)] for row in range(ROW_CELLS)]        # Store 'Cell' objects
        self.squares = [[None for col in range(COL_CELLS)] for row in range(ROW_CELLS)]     # Store drawn squares (for future updates)
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

    # Draw canvas/grid
    def drawCanvas(self):
        pygame.draw.rect(self.canvas, BLACK, (GRID_POS[0], GRID_POS[1], GRID_WIDTH, GRID_HEIGHT), 2)
        for x in range(COL_CELLS):
            for y in range(ROW_CELLS):
                square = pygame.draw.rect(self.canvas, BLACK, (GRID_POS[0]+(x*CELL_SIZE), GRID_POS[1]+(y*CELL_SIZE), CELL_SIZE, CELL_SIZE), 1)
                square.fill(GAINSBORO_GREY)
                self.squares[y][x] = square
        pygame.display.flip()

    # Returns Cell object + Rectangle object
    def getCell(self, mouse_position):
        if GRID_POS[0] <= mouse_position[0] < GRID_POS[0] + GRID_WIDTH and GRID_POS[1] <= mouse_position[1] < GRID_POS[1] + GRID_HEIGHT:
            grid_position = (mouse_position[0]-GRID_POS[0],mouse_position[1]-GRID_POS[1])
            cell = self.grid[grid_position[0]//CELL_SIZE][grid_position[1]//CELL_SIZE]
            square = self.squares[grid_position[0]//CELL_SIZE][grid_position[1]//CELL_SIZE]
            return cell, square
        return None

    # Cell click event
    def click(self, cell, square):
        pass

    # Cell flag event
    def flag(self, cell, square):
        pass

    # Calculate cell surrounding bombs and set number
    def surrounding_bombs_value():
        pass

    # Handle events
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                cell, square = self.getCell(mouse_pos)
                print(cell)
                print(square)
                if event.button == 1:           # mouse left-click event
                    self.click(cell,square)
                elif event.button == 3:         # mouse right-click event
                    self.flag(cell,square)