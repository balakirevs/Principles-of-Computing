"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        result = True
        if self.get_number(target_row, target_col) != 0:
            result = False
        width = self.get_width()
        height = self.get_height()
        cur_num = target_row * width + target_col
        for num in range(cur_num + 1, width * height):
            row = num / width
            col = num % width
            if self.get_number(row, col) != num:
                result = False
        return result
    
    def position_tile(self, target_pos, target_tile, move_string):
        """
        Helper function to put target tile to target position when j > 1. 
        And put 0 tile on the left of target tile
        """
        # Move 0 tile up to the same row as target tile
        target_row, target_col = target_pos
        cur_row, cur_col = target_tile
        move_string += "u" * (target_row - cur_row)
        if cur_col < target_col:
            # Move target tile to the same col as target position
            # Then put 0 tile on the top of target tile
            while True:
                if target_col - cur_col == 1:
                    move_string += "l"
                    cur_col += 1
                    break
                else:
                    move_string += "l" * (target_col - cur_col)
                    move_string += "d" if cur_row == 0 else "u"
                    move_string += "r" * (target_col - cur_col)
                    move_string += "u" if cur_row == 0 else "d"
                    cur_col += 1
            # Move 0 tile to the top of target tile
            move_string += "dru" if cur_row == 0 else "ur"
            cur_row += 1 if cur_row == 0 else 0
            
        elif cur_col > target_col:
            # Move target tile to the same col as target position
            # Then put 0 tile on the top of target tile
            while True:
                if cur_col - target_col == 1:
                    move_string += "r"
                    cur_col -= 1
                    break
                else:
                    move_string += "r" * (cur_col - target_col)
                    move_string += "d" if cur_row == 0 else "u"
                    move_string += "l" * (cur_col - target_col)
                    move_string += "u" if cur_row == 0 else "d"
                    cur_col -= 1
            move_string += "dlu" if cur_row == 0 else "ul"
            cur_row += 1 if cur_row == 0 else 0
        elif cur_col == target_col:
            cur_row += 1
        
        # Move target tile down to the target position
        move_string += "lddru" * (target_row - cur_row)
        move_string += "ld"
        
        return move_string
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """ 
        width = self.get_width()
        height = self.get_height()
        move_string = ""

        cur_row = 0
        cur_col = 0
        for row in range(height):
            for col in range(width):
                if self.get_number(row, col) == target_row * width + target_col:
                    cur_row = row
                    cur_col = col
                    break
        
        target_pos = (target_row, target_col)
        target_tile = (cur_row, cur_col)
        move_string = self.position_tile(target_pos, target_tile, move_string)
                
        self.update_puzzle(move_string) # Update
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        # Move 0 tile to (i - 1, 1)
        move_string = "ur"
        new_puzzle = self.clone()
        new_puzzle.update_puzzle(move_string)
        # Find the target tile
        width = self.get_width()
        height = self.get_height()
        target_number = target_row * width
        for row in range(height):
            for col in range(width):
                if new_puzzle.get_number(row, col) == target_number:
                    cur_row = row
                    cur_col = col
                    break
                    
        if cur_row == target_row and cur_col == 0:
            move_string += "r" * (width - 2)
            self.update_puzzle(move_string)
        else:
            target_pos = (target_row - 1, 1)
            target_tile = (cur_row, cur_col)
            move_string = self.position_tile(target_pos, target_tile, move_string)
            move_string += "ruldrdlurdluurddlur" # From homework 9
            move_string += "r" * (width - 2)
            self.update_puzzle(move_string)
            
        assert self.lower_row_invariant(target_row - 1, width - 1)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        result = True
        width = self.get_width()
        height = self.get_height()
        if self.get_number(0, target_col) != 0:
            result = False
        
        for col in range(target_col + 1, width):
            if self.get_number(0, col) != col:
                result = False
        
        number_below = width + target_col
        for num in range(number_below, width * height):
            row = num / width
            col = num % width
            if self.get_number(row, col) != num:
                result = False
        return result

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        result = True
        if not self.lower_row_invariant(1, target_col):
            result = False
        width = self.get_width()
        for col in range(target_col + 1, width):
            if col != self.get_number(0, col):
                result = False
        return result

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_string = "ld"
        new_puzzle = self.clone()
        new_puzzle.update_puzzle(move_string)
        target_num = target_col
        width = self.get_width()
        height = self.get_height()
        for row in range(height):
            for col in range(width):
                if new_puzzle.get_number(row, col) == target_num:
                    cur_row = row
                    cur_col = col
                    break
                    
        if cur_row == 0 and cur_col == target_col:
            self.update_puzzle(move_string)
            return move_string
        else:
            target_pos = (1, target_col - 1)
            target_tile = (cur_row, cur_col)
            move_string = self.position_tile(target_pos, target_tile, move_string)
            move_string += "urdlurrdluldrruld"
            self.update_puzzle(move_string)
            return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        width = self.get_width()
        height = self.get_height()
        
        target_num = width + target_col
        for row in range(height):
            for col in range(width):
                if self.get_number(row, col) == target_num:
                    cur_row = row
                    cur_col = col
                    break
                    
        move_string = ""
        target_pos = (1, target_col)
        target_tile = (cur_row, cur_col)
        move_string = self.position_tile(target_pos, target_tile, move_string)
        
        self.update_puzzle(move_string[:-2])
        return move_string[:-2]

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        width = self.get_width()
        # Three target numbers
        zero_one = 1
        one_zero = width
        one_one = width + 1
        # Three numbers in the positions above now
        pos_one = self.get_number(1, 0)
        pos_two = self.get_number(0, 0)
        pos_three = self.get_number(0, 1)
        num_list = [pos_one, pos_two, pos_three]
        # The three other situation are unsolvable
        if num_list == [one_zero, zero_one, one_one]:
            move_string = "ul"
        elif num_list == [one_one, one_zero, zero_one]:
            move_string = "lu"
        elif num_list == [zero_one, one_one, one_zero]:
            move_string = "lurdlu"
            
        self.update_puzzle(move_string)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        if self.lower_row_invariant(0, 0):
            return ""
        
        move_string = ""
        width = self.get_width()
        height = self.get_height()
        
        # Move 0 tile to the lower right corner
        if self.get_number(height - 1, width - 1) != 0:
            for row in range(height):
                for col in range(width):
                    if self.get_number(row, col) == 0:
                        zero_row = row
                        zero_col = col
                        break
            move_string += "d" * (height - 1 - zero_row)
            move_string += "r" * (width - 1 - zero_col)
            
        self.update_puzzle(move_string)

        for row in range(height - 1, 1, -1):
            for col in range(width - 1, -1, -1):
                move_string += self.solve_col0_tile(row) if col == 0 else self.solve_interior_tile(row, col)
                
        for col in range(width - 1, 1, -1):
            move_string += self.solve_row1_tile(col)
            move_string += self.solve_row0_tile(col)
                
        move_string += self.solve_2x2()
                    
        return move_string

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
