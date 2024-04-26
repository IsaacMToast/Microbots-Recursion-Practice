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
   
class Point:
    def __init__(self, row: int, col: int) -> None:
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))

class Path:
    def __init__(self, start_point:Point, end_point:Point) -> None:
        self.start_point = start_point
        self.end_point = end_point
   
def accessible(point1:'Point', point2:'Point') -> bool:
    cell1 = BOARD[point1.row][point1.col]
    cell2 = BOARD[point2.row][point2.col]
    return cell1.color == cell2.color or cell1.val == cell2.val
   
   
def find_options(point:Point) -> set[Point]:
    accessible_cells = set()
    
    for col in range(BOARD_COLS):
        new_point = Point(point.row, col)
        if col == point.col:
            continue
        if accessible(point, new_point):
            accessible_cells.add(new_point)
   
    for row in range(BOARD_ROWS):
        new_point = Point(row, point.col)
        if row == point.row:
            continue
        if accessible(point, new_point):
            accessible_cells.add(new_point)
            
    return accessible_cells
       
       
least_steps = float('inf')
shortest_path = []
def find_optimal_path(start_point:Point, end_point:Point, steps:int=0, visited:list=[], path:list=[]):
    global least_steps
    global shortest_path
    path.append(start_point)
    if start_point == end_point:
        if steps < least_steps:
            least_steps = steps
            shortest_path = path
        return
            
    visited.append(start_point)
    available_moves = find_options(start_point).difference(visited)
    
    for coord in available_moves:
        find_optimal_path(coord, end_point, steps+1, visited.copy(), path.copy()) 
       


class CoordinateFormatError(Exception):
    pass

def parse_coord(coord_string:str) -> tuple[int]:
    comma_count = 0
    if any(char not in ',0123456789-' for char in coord_string ):
        raise CoordinateFormatError("Unallowed character.")
    
    for char in coord_string:
        if char == ',':
            comma_count += 1
        if comma_count > 1:
            raise CoordinateFormatError('Too many commas!')
        
    try:
        row = int(coord_string[0:coord_string.index(',')])
        col = int(coord_string[coord_string.index(',')+1:])
    except ValueError:
        raise CoordinateFormatError('Invalid row or column number.')
    
    if min(row, col) < 0:
        raise CoordinateFormatError('Negative row or column.')
    
    return row-1, col-1
        
            

def random_row():
    return random.randint(0, BOARD_ROWS-1)

def random_col():
    return random.randint(0, BOARD_COLS-1)

def random_point():
    row = random_row()
    col = random_col()
    return Point(row, col)
       
def clear():
    os.system('cls')
    print(Fore.RESET, end='')
    
     
def menu():
    print("Micro bots! Enter p to play, s to solve, or q to quit.")
    choice = ''
    while True:
        choice = input('>: ')
        if choice not in ['p','s','q']:
            print(Fore.RED + 'ERROR: Invalid choice.' + Fore.RESET)
        else:
            break
    if choice == "p":
        pass
    elif choice == "s":
        solve()
    elif choice == "q":
        quit()



def random_path() -> Path:
    start_point = random_point()
    end_point = start_point

    while (start_point) == (end_point):
        end_point = random_point()
        
    return Path(start_point, end_point)

def play():
    path = random_path()
    start_cell = BOARD[path.start_point.row][path.start_point.col]
    end_cell = BOARD[path.end_point.row][path.end_point.col]

def solve():
    path = random_path()
    start_cell = BOARD[path.start_point.row][path.start_point.col]
    end_cell = BOARD[path.end_point.row][path.end_point.col]
            
    clear()
    print_2d_list(BOARD, 1)
    print(f'Going from {start_cell} to {end_cell}.')
   
    for row in range(BOARD_ROWS):
        temp_list = []
        for col in range(BOARD_COLS):
            temp_list.append(find_options(Point(row, col)))
        movement_board.append(temp_list)

    find_optimal_path(path.start_point, path.end_point, 0)
    for point in shortest_path:
        print(BOARD[point.row][point.col], end=' ')
    print()
    print(f"Steps: {least_steps}")
    print('Press enter to continue . . . ')
    input()
       
def main():
    menu()  
    clear()
       
       
    


if __name__ == '__main__':
    main()