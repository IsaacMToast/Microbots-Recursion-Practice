import os
import random
from colorama import Fore, Style
 
 
 
class Cell:
    def __init__(self, val:int, color:str) -> None:
        self.val = val
        self.color = color
       
    def __str__(self) -> str:
        return f"{self.color}{self.val}{Fore.RESET}"
       
       
       
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
    
    def __str__(self) -> str:
        return f'Point({self.row}, {self.col})'



class Path:
    def __init__(self, start:Point, end:Point) -> None:
        self.start = start
        self.end = end
        
        
        
BOARD = [
    [Cell(5, Fore.LIGHTMAGENTA_EX), Cell(2, Fore.LIGHTMAGENTA_EX), Cell(3, Fore.LIGHTMAGENTA_EX), Cell(2, Fore.YELLOW),          Cell(1, Fore.WHITE),  Cell(1, Fore.BLUE)],
    [Cell(6, Fore.RED),             Cell(4, Fore.RED),             Cell(3, Fore.YELLOW),          Cell(2, Fore.WHITE),           Cell(2, Fore.GREEN),  Cell(2, Fore.RED)],
    [Cell(4, Fore.BLUE),            Cell(5, Fore.GREEN),           Cell(3, Fore.GREEN),           Cell(4, Fore.LIGHTMAGENTA_EX), Cell(6, Fore.GREEN),  Cell(4, Fore.WHITE)],
    [Cell(6, Fore.WHITE),           Cell(6, Fore.BLUE),            Cell(2, Fore.BLUE),            Cell(6, Fore.LIGHTMAGENTA_EX), Cell(5, Fore.YELLOW), Cell(1, Fore.LIGHTMAGENTA_EX)],
    [Cell(3, Fore.RED),             Cell(4, Fore.YELLOW),          Cell(3, Fore.WHITE),           Cell(1, Fore.RED),             Cell(5, Fore.BLUE),   Cell(6, Fore.YELLOW)],
    [Cell(3, Fore.BLUE),            Cell(4, Fore.GREEN),           Cell(5, Fore.WHITE),           Cell(1, Fore.GREEN),           Cell(5, Fore.RED),    Cell(1, Fore.YELLOW)]
]
COLOR_CODES = {
    "colors":{
        Fore.LIGHTMAGENTA_EX: 'M',
        Fore.GREEN: 'G',
        Fore.YELLOW: 'Y',
        Fore.RED: 'R',
        Fore.BLUE: 'B',
        Fore.WHITE: 'W'
    },
    'letters':{
        'M': Fore.LIGHTMAGENTA_EX,
        'G': Fore.GREEN,
        'Y': Fore.YELLOW,
        'R': Fore.RED,
        'B': Fore.BLUE,
        'W': Fore.WHITE
    }
}
BOARD_CODES = {}
BOARD_ROWS = len(BOARD)
BOARD_COLS = len(BOARD[0])
SHORTEST_PATH = []
MOVEMENT_BOARD = []
   
   
   
def print_board(spacing=1) -> None:
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            print(str(BOARD[row][col]), end=' ' * spacing)
        print()
    print()
   
   
   
def accessible(point1:Point, point2:Point) -> bool:
    cell1 = BOARD[point1.row][point1.col]
    cell2 = BOARD[point2.row][point2.col]
    return (point1.row == point2.row or point1.col == point2.col) and (cell1.color == cell2.color or cell1.val == cell2.val)
   
   
   
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
def find_optimal_path(start_point:Point, end_point:Point, steps:int=0, visited:list=[], path:list=[]):
    global SHORTEST_PATH
    global least_steps
    path.append(start_point)
    if start_point == end_point:
        if steps < least_steps:
            least_steps = steps
            SHORTEST_PATH = path
        return
            
    visited.append(start_point)
    available_moves = find_options(start_point).difference(visited)
    
    for coord in available_moves:
        find_optimal_path(coord, end_point, steps+1, visited.copy(), path.copy()) 
       
       

class CoordinateFormatError(Exception):
    pass



def parse_coord(coord_string:str) -> Path:
    coord_string = coord_string.strip().upper()
        
    try:
        start_space = coord_string[0:coord_string.index(',')].upper()
        start_point = BOARD_CODES[start_space]
        
        end_space = coord_string[coord_string.index(',')+1:].upper()
        end_point = BOARD_CODES[end_space]
    except (KeyError, ValueError):
        raise CoordinateFormatError("Invalid Input.")
        
    return(Path(start_point, end_point))



def random_row():
    return random.randint(0, BOARD_ROWS-1)



def random_col():
    return random.randint(0, BOARD_COLS-1)



def random_point():
    row = random_row()
    col = random_col()
    return Point(row, col)
       
       
       
def random_path() -> Path:
    start_point = random_point()
    end_point = start_point

    while (start_point) == (end_point):
        end_point = random_point()
        
    return Path(start_point, end_point)



def clear():
    os.system('cls')
    print(Fore.RESET, end='')



class PathFormatError(Exception):
    pass



def parse_path(path:str) -> list[Point]:
    points = []
    path = path.strip()
    for i in range(0,len(path), 3):
        color = path[i]
        if color.upper() not in COLOR_CODES['letters'].keys():
            raise PathFormatError(f'Invalid format / Invalid color: {color}')
        try:
            val = int(path[i+1])
            if val < 1 or val > 6:
                raise ValueError
        except ValueError:
            raise PathFormatError(f'Invalid format / Invalid cell value: {val}.')
        if i+3 < len(path):
            comma = path[i+2]
            if comma != ',':
                raise PathFormatError('Invalid format.')
        points.append(BOARD_CODES[f'{color.upper()}{val}'])
    return points



def validate_path_moves(path:list[Point]) -> bool:
    if len(path) <= 1:
        return False
    for i in range(len(path)):
        if not accessible(path[i], path[i+1]):
            return False
    return True



def validate_path_completion(path:list[Point], start_cell: Point, end_cell: Point):
    if len(path) <= 1:
        return False
    return path[0] in (start_cell, end_cell) and path[len(path)-1] in (start_cell, end_cell)
        
    

def visualize_text(boolean: bool, true_text: str, false_text: str):
    return Fore.GREEN + true_text + Fore.RESET if boolean else Fore.RED + false_text + Fore.RESET



def pause():
    print('Press ENTER to continue . . . ', end='')
    input()



def get_yn():
    while True:
        response = input('>: ')
        if response in ['y','n']:
            return response
        else:
            print(Fore.RED + 'Invalid response.' + Fore.RESET)



def get_path():
    path = []
    while True:
        path_input = input('>: ')
        try:
            path = parse_path(path_input.strip())
            break
        except PathFormatError as e:
            print(Fore.RED + 'Error: ' + str(e) + Fore.RESET)
    return path
            
            
            
def print_play_instructions(start_cell: Cell, end_cell: Cell):
    print_board()
    print(f'Go from {start_cell} to {end_cell}.')
    print(f'Enter your path comma seperated with the form #C where C is the first letter of the color, and # is the number.\nEg. R6,R4,Y4,Y6')
    print('Colors: M, Y, G, W, B, R')



def print_path(path: list[Point]):
    for point in path:
        print(str(BOARD[point.row][point.col]), end=' ')
    print('')



def play():
    goal_path = random_path()
    start_cell = BOARD[goal_path.start.row][goal_path.start.col]
    end_cell = BOARD[goal_path.end.row][goal_path.end.col]
    path = []
    
    find_optimal_path(goal_path.start, goal_path.end)
    
    while True:
        clear()
        print_play_instructions(start_cell, end_cell)
        path = get_path()
        moves_valid = validate_path_moves(path)
        path_completed = validate_path_completion(path, goal_path.start, goal_path.end)
        
        if moves_valid and path_completed:
            break
        elif not moves_valid:
            print(Fore.RED + 'That path is not valid.' + Fore.RESET)
        elif not path_completed:
            print(Fore.RED + 'That path does not reach the end.' + Fore.RESET)
            
        print('Would you like to try again? (y/n)')
        response = get_yn()
        if response == 'n':
            clear()
            print_board()
            print('Okay! Before you go, this was the shortest path: ')
            print_path(SHORTEST_PATH)
            pause()
            return
    
    print()
    moves = len(path)-1
    optimal_moves = len(SHORTEST_PATH)-1
    
    print('Your path: ', end='')
    print_path(path)
    print()
    print(f'You got it in {moves} move(s).')
    
    print('Here\'s my path: ', end='')
    print_path(SHORTEST_PATH)
    
    if moves == optimal_moves:
        print(f'I got it in {moves} move(s) too.')    
        print(f'You found the shortest path!')
    else:
        print(f'I got it in {optimal_moves} move(s).') 
        print('I won!')
    
    print()
    pause()



def solve():
    clear()
    print_board()
    print()
    print("Enter the start and end spaces seperated by a comma in C# format where C is the first letter of the color, and # is the number.\nEg. Y5,G4")
    while True:
        try:
            path = parse_coord(input('>: '))
            break
        except CoordinateFormatError as e:
            print(Fore.RED + str(e) + Fore.RESET)
            
    start_cell = BOARD[path.start.row][path.start.col]
    end_cell = BOARD[path.end.row][path.end.col]
            
    clear()
    print_board()
    print(f'Going from {start_cell} to {end_cell}.')
    find_optimal_path(path.start, path.end, 0)
    for point in SHORTEST_PATH:
        print(BOARD[point.row][point.col], end=' ')
    print()
    print(f"Steps: {len(SHORTEST_PATH)-1}")
    
    pause()
       
       
       
def load_codes():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            BOARD_CODES[f"{str(COLOR_CODES['colors'][BOARD[row][col].color])}{str(BOARD[row][col].val)}"] = Point(row,col)
       
       
       
def load_moves():
    for row in range(BOARD_ROWS):
        temp_list = []
        for col in range(BOARD_COLS):
            temp_list.append(find_options(Point(row, col)))
        MOVEMENT_BOARD.append(temp_list)
        

     
def menu():
    print("Micro bots! Enter p to play, s to solve, or q to quit.")
    
    global least_steps
    least_steps = float('inf')
    choice = ''
    
    while True:
        choice = input('>: ')
        if choice not in ['p','s','q']:
            print(Fore.RED + 'ERROR: Invalid choice.' + Fore.RESET)
        else:
            break
    if choice == "p":
        play()
    elif choice == "s":
        solve()
    elif choice == "q":
        clear()
        quit()


       
def main():
    clear()
    load_codes()
    load_moves()
    while True:
        menu()  
        clear()
       
    

if __name__ == '__main__':
    main()