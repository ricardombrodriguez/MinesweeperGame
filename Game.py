import pygame, sys, random, tkinter
from Const import *
from Cell import Cell
from tkinter import messagebox

class Game:

    # Initial game settings
    def __init__(self):
        pygame.init()
        self.running = True
        self.firstTime = True
        self.canvas = pygame.display.set_mode((WIDTH,HEIGHT))
        self.canvas.fill(DARK_GREY)
        pygame.display.set_caption("Minesweeper")
        pygame.display.flip()
        self.remaining_flags = NUM_BOMBS
        self.remaining_cells = ROW_CELLS*COL_CELLS - NUM_BOMBS
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
        self.surroundingBombsValue()

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
        pygame.draw.rect(self.canvas, DARK_GREY, (GRID_POS[0], GRID_POS[1], GRID_WIDTH, GRID_HEIGHT), 2)
        for x in range(COL_CELLS):
            for y in range(ROW_CELLS):
                square = pygame.draw.rect(self.canvas, WHITE, (GRID_POS[0]+(x*CELL_SIZE), GRID_POS[1]+(y*CELL_SIZE), CELL_SIZE, CELL_SIZE), 2)
                self.squares[y][x] = square
        pygame.display.flip()

    # Returns Cell object + Rectangle object + Grid position
    def getGridPosition(self, mouse_position):
        if GRID_POS[0] <= mouse_position[0] < GRID_POS[0] + GRID_WIDTH and GRID_POS[1] <= mouse_position[1] < GRID_POS[1] + GRID_HEIGHT:
            mouse_pos = (mouse_position[0]-GRID_POS[0],mouse_position[1]-GRID_POS[1])
            grid_position = (mouse_pos[1]//CELL_SIZE, mouse_pos[0]//CELL_SIZE)
            cell = self.grid[grid_position[0]][grid_position[1]]
            square = self.squares[grid_position[0]][grid_position[1]]
            return cell, square, grid_position
        return None, None, None

    # Cell click event
    def click(self, cell, square, grid_position):
        if cell.bomb:
            self.end("L")
        else:
            if not cell.clicked:
                self.remaining_cells -= 1
                cell.clicked = True
                self.updateSquare(cell,square,"CLICK")
                if cell.number == 0:
                    self.findEmptyNeighbours(grid_position[0],grid_position[1])

    # Recursive neighbour empty-cell search
    def findEmptyNeighbours(self, row, column):
        for j in range(-1,2,1):
            for k in range(-1,2,1):
                if row + j < 0 or row + j >= ROW_CELLS or column + k < 0 or column + k >= COL_CELLS or (row + j == row and column + k == column):
                    continue
                else:
                    neighbour_cell = self.grid[row+j][column+k]
                    neighbour_square = self.squares[row+j][column+k]
                    if not neighbour_cell.clicked and not neighbour_cell.bomb:
                        self.click(neighbour_cell,neighbour_square,(row+j,column+k))

    # Cell flag event
    def flag(self, cell, square):
        if not cell.clicked:
            if cell.flag == False and self.remaining_flags > 0:
                cell.flag = True
                self.remaining_flags -= 1
                self.updateSquare(cell,square,"FLAG")
            elif cell.flag == True:
                cell.flag = False
                self.remaining_flags += 1
                self.updateSquare(cell,square,"UNCLICK")

    # Calculate cell surrounding bombs and set number
    def surroundingBombsValue(self):
        for col in range(COL_CELLS):
            for row in range(ROW_CELLS):
                cell = self.grid[row][col]
                surrounding_bombs = 0
                if not cell.bomb:
                    for j in range(-1,2,1):
                        for k in range(-1,2,1):
                            if 0 <= row+j < ROW_CELLS and 0 <= col+k < COL_CELLS:
                                try:
                                    neighbour_cell = self.grid[row+j][col+k]
                                    surrounding_bombs = surrounding_bombs + 1 if neighbour_cell.bomb else surrounding_bombs
                                except IndexError:
                                    continue
                cell.number = surrounding_bombs
        

        # for debugging
        temp = [[self.grid[row][col].number if not self.grid[row][col].bomb else -1 for col in range(COL_CELLS)] for row in range(ROW_CELLS)] 
        print(temp)
                      

    # Gets square + operation (flag, click, unselect...) to fill the square with different colors/images/emojis(?)
    def updateSquare(self,cell,square,operation):
        font = pygame.font.SysFont('Arial', 25)
        if operation == "CLICK":
            self.clickSquare(cell,square)
        elif operation == "FLAG":
            myimage = pygame.image.load("bandeira.png")
            imagerect = myimage.get_rect()
            self.canvas.blit(myimage,(square.left+10, square.top+5))
            pygame.display.flip()
        elif operation == "UNCLICK":
            square = self.overwriteSquare(DARK_GREY,square)
        pygame.display.update()

    #Draw square + number
    def clickSquare(self,cell,square):
        colors = [NUMBER0,NUMBER1,NUMBER2,NUMBER3,NUMBER4,NUMBER5,NUMBER6,NUMBER7,NUMBER8]
        color = colors[cell.number]
        self.overwriteSquare(color,square)
        font = pygame.font.SysFont('Arial', 25)
        if cell.number != 0:
            text = str(cell.number)
            self.canvas.blit(font.render(text, True, BLACK), (square.left+10, square.top+5))
        pygame.display.update()

    # Overwrite the square and fill it with a specified color
    def overwriteSquare(self, color, square):
        square.x += 2
        square.y += 2
        square.width -= 4
        square.height -= 4
        pygame.draw.rect(self.canvas, color, square)
        square.x -= 2
        square.y -= 2
        square.width += 4
        square.height += 4
        return square

    # Check if it's a win
    def checkWin(self):
        if self.remaining_cells + self.remaining_flags != 0:
            return False
        for col in range(COL_CELLS):
            for row in range(ROW_CELLS):
                cell = self.grid[row][col]
                if cell.flag and not cell.bomb:
                    return False
        return True

    # End game -> (W)in / (L)ose
    def end(self,operation):
        self.running = False
        if operation == "L":
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("Minesweeper", "YOU LOST!")
        if operation == "W":
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("Minesweeper!", "YOU WON!\nYou completed the game in " + str(self.time_counter) + " seconds!")

    # Handle events
    def events(self):
        if self.firstTime == False:
            self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT:
                self.timer_surface.fill(DARK_GREY)
                self.canvas.blit(self.timer_surface,(100, 49))
                pygame.display.update()
                font = pygame.font.SysFont('Arial', 25)
                self.time_counter += 1
                self.time_text = ("Timer: " + str(self.time_counter) + "s").rjust(3)
                self.canvas.blit(font.render(self.time_text, True, WHITE), (100, 65))
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.firstTime:
                    self.clock = pygame.time.Clock()
                    self.time_counter = 0
                    self.time_text = '1000000'.rjust(3)
                    self.timer_surface = pygame.Surface((WIDTH, 50))
                    self.timer_surface.fill(DARK_GREY)
                    self.canvas.blit(self.timer_surface, (100, 49))
                    pygame.display.update()
                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                    self.firstTime = False
                mouse_pos = event.pos
                cell,square,grid_position = self.getGridPosition(mouse_pos)
                if cell is None:
                    return
                if event.button == 1:           # mouse left-click event
                    self.click(cell,square,grid_position)
                elif event.button == 3:         # mouse right-click event
                    self.flag(cell,square)
                print("===========")
                print("CELLS: " + str(self.remaining_cells) + " | FLAGS: " + str(self.remaining_flags))
                if self.checkWin():
                    self.end("W")