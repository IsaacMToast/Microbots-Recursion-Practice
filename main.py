import os
import random
from colorama import Fore
 
class Cell:
    def __init__(self, val:int, color:str) -> None:
        self.val = val
        self.color = color
       
    def __str__(self) -> str:
        return f"{self.color}{self.val}{Fore.RESET}"
       
BOARD = [
    [Cell(5, Fore.LIGHTMAGENTA_EX), Cell(2, Fore.LIGHTMAGENTA_EX), Cell(3, Fore.LIGHTMAGENTA_EX), Cell(2, Fore.YELLOW),          Cell(1, Fore.WHITE),  Cell(1, Fore.BLUE)],
    [Cell(6, Fore.RED),             Cell(4, Fore.RED),             Cell(3, Fore.YELLOW),          Cell(2, Fore.WHITE),           Cell(2, Fore.GREEN),  Cell(2, Fore.RED)],
    [Cell(4, Fore.BLUE),            Cell(5, Fore.GREEN),           Cell(3, Fore.GREEN),           Cell(4, Fore.LIGHTMAGENTA_EX), Cell(6, Fore.GREEN),  Cell(4, Fore.WHITE)],
    [Cell(6, Fore.WHITE),           Cell(6, Fore.BLUE),            Cell(2, Fore.BLUE),            Cell(6, Fore.LIGHTMAGENTA_EX), Cell(5, Fore.YELLOW), Cell(1, Fore.LIGHTMAGENTA_EX)],
    [Cell(3, Fore.RED),             Cell(4, Fore.YELLOW),          Cell(3, Fore.WHITE),           Cell(1, Fore.RED),             Cell(5, Fore.BLUE),   Cell(6, Fore.YELLOW)],
    [Cell(3, Fore.BLUE),            Cell(4, Fore.GREEN),           Cell(5, Fore.WHITE),           Cell(1, Fore.GREEN),           Cell(5, Fore.RED),    Cell(1, Fore.YELLOW)]
]
movement_board = []
BOARD_ROWS = len(BOARD)
BOARD_COLS = len(BOARD[0])
   
   
def print_2d_list(l: list[list], spacing=1) -> None:
    for row in l:
        for col in row:
            print(str(col), end=' ' * spacing)
        print()
   
   
def accessible(row1:int, col1:int, row2:int, col2:int) -> bool:
    cell1 = BOARD[row1][col1]
    cell2 = BOARD[row2][col2]
    return cell1.color == cell2.color or cell1.val == cell2.val
   
   
def find_options(start_row:int, start_col:int) -> set[tuple[int]]:
    accessible_cells = set()
    
    for col in range(BOARD_COLS):
        if col == start_col:
            continue
        if accessible(start_row, start_col, start_row, col):
            accessible_cells.add((start_row, col))
   
    for row in range(BOARD_ROWS):
        if row == start_row:
            continue
        if accessible(start_row, start_col, row, start_col):
            accessible_cells.add((row, start_col))
            
    return accessible_cells
       
       
least_steps = float('inf')
shortest_path = []
def find_optimal_path(start_row:int, start_col:int, end_row:int, end_col:int, steps:int=0, visited:list=[], path:list=[]):
    global least_steps
    global shortest_path
    path.append((start_row, start_col))
    if (start_row, start_col) == (end_row, end_col):
        if steps < least_steps:
            least_steps = steps
            shortest_path = path
        return
            
    visited.append((start_row, start_col))
    available_moves = find_options(start_row, start_col).difference(visited)
    
    for coord in available_moves:
        find_optimal_path(coord[0], coord[1], end_row, end_col, steps+1, visited.copy(), path.copy()) 
       
def random_row():
    return random.randint(0, BOARD_ROWS-1)

def random_col():
    return random.randint(0, BOARD_COLS-1)

class 

def check_coord(coord:str):
    comma_count = 0
    allowed_nums = ',0123456789'
    for char in coord:
        if char not in allowed_nums:
            raise 
        if char == ',':
            


def get_row_col(message:bool = True) -> tuple[int]:
    if message:
        print(f"Please enter coordinates (row,col).")
    while True:
            response = input('>: ')
            try:
                row = int(response[0])
                col = int(response[1])
            except ValueError:
                print(Fore.RED + "Invalid Input. Please enter an integer." + Fore.RESET)
            
            if response < 1 or response > BOARD_ROWS:
                print(Fore.RED + f"Invalid Input. Please choose a valid within the bounds of a ({BOARD_ROWS}/{BOARD_ROWS})." + Fore.RESET)
            else:
                break
    return (row-1, col-1)
       
def main():
    os.system('cls')
    print(Fore.RESET, end='')
   
    print_2d_list(BOARD, 1)
   
    print("What would you like to do?\n   [1.] Manually input start and end locations.\n   [2.] Randomly choose start and end locations.")
    while True:
        try:
            response = int(input('>: '))
            if response not in (1,2):
                print(Fore.RED + "Invalid Input. Please choose either 1 or 2." + Fore.RESET)
            else:
                break
        except ValueError:
            print(Fore.RED + "Invalid Input. Please enter an integer." + Fore.RESET)
            
    if response == 1:
        print("CHOOSING START LOCATION.")
        start = get_row_col()
        start_row = start[0]
        start_col = start[1]
        
        print("CHOOSING END LOCATION.")
        end = get_row_col()
        end_row = end[0]
        end_col = end[1]
        
    elif response == 2:
        start_row = random_row()
        start_col = random_col()
        end_row = start_row
        end_col = start_col
 
        while (start_row, start_col) == (end_row, end_col):
            end_row = random_row()
            end_col = random_col()
       
    start_cell = BOARD[start_row][start_col]
    end_cell = BOARD[end_row][end_col]
       
    os.system('cls')
    print_2d_list(BOARD, 1)
    print(f'Going from {start_cell} to {end_cell}.')
   
    for row in range(BOARD_ROWS):
        temp_list = []
        for col in range(BOARD_COLS):
            temp_list.append(find_options(row, col))
        movement_board.append(temp_list)

    find_optimal_path(start_row, start_col, end_row, end_col, 0)
    for point in shortest_path:
        print(BOARD[point[0]][point[1]], end=' ')
    print()
    print(f"Steps: {least_steps}")


if __name__ == '__main__':
    main()