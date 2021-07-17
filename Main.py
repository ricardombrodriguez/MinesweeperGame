from Const import *
from Game import *
import sys
import math

if __name__ == "__main__":
    
    if len(sys.argv) == 4:
        valid = True
        num_rows = int(sys.argv[1])
        num_columns = int(sys.argv[2])
        bomb_percentage= int(sys.argv[3])
        if not (MIN_ROW_CELLS <= num_rows <= MAX_ROW_CELLS):
            print("Invalid number of rows. It must have a value between 8-25 (included)")
            valid = False
        if not (MIN_COL_CELLS <= num_columns <= MAX_COL_CELLS):
            print("Invalid number of columns. It must have a value between 8-45 (included)")
            valid = False
        if not (MIN_BOMB_PERCENTAGE <= bomb_percentage <= MAX_BOMB_PERCENTAGE):
            print("Invalid percentage of bombs. It must have a value between 2-84 (included)")
            valid = False
        if valid == False:
            sys.exit(0)
        bombs = math.floor((num_columns*num_rows*bomb_percentage)/100)
    elif len(sys.argv) == 1:
        num_rows = 16
        num_columns = 30
        bombs = 99
    else:
        print("ERROR: Invalid number of arguments.")
        print("0 arguments -> Creates default 'expert' minesweeper game (16 rows x 30 columns with 99 bombs")
        print("3 arguments -> (number of rows) (number of columns) (bomb percentage)")
        sys.exit(0)
    game = Game(num_rows,num_columns,bombs)
    game.run()