"""
Mini-project for Principles of Computing Part 1. A clone of "2048" game.
Written on: 14/09/2015
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # Initialize result list
    result_list = [0] * len(line)
    
    # Copy line to temp_list, compacting non-zero elements towards the start of temp_list
    temp_list = [item for item in line if item > 0] 
    temp_list.extend([0]* (len(result_list) - len(temp_list)))

    # Merge two tiles or copy a tile in temp_list; place the result into the next available tile in result_list
    index1 = 0  
    index2 = 0 
    while index1 < len(temp_list):
        if index1 < len(temp_list)-1:
            if temp_list[index1+1] != temp_list[index1]:
                result_list[index2] = temp_list[index1]
                index1 += 1
            else:
                result_list[index2] = temp_list[index1] + temp_list[index1+1]
                index1 += 2
        else:
            # Corner case: if index1 reaches the last element in temp_list, just copy the item
            if index1 == len(line) - 1:
                result_list[index2] = temp_list[index1]
                index1 += 1

        index2 += 1      
        
    return result_list  

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Initialize an instance of TwentyFortyEight and define a dictionary containing the
        lists of indices of initial tiles for the UP, DOWN, LEFT and RIGHT directions
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()

        self._starting_tiles = {UP: [(0, col) for col in range(self._grid_width)], \
                              DOWN: [(self._grid_height-1, col) for col in range(self._grid_width)], \
                              LEFT: [(row, 0) for row in range(self._grid_height)], \
                              RIGHT: [(row, self._grid_width-1) for row in range(self._grid_height)]}
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0] * self._grid_width for dummy_ix in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        text = "["
        for row in range(self._grid_height):
            text = text + "["
            for col in range(self._grid_width):
                text = text + str(self._grid[row][col])
                if col < self._grid_width - 1:
                    text = text + ", "
                 
            text = text + "]"
            if row < self._grid_height - 1:
                text = text +"\n "
                
        text =  text + "]"
        
        return text

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        # Determines how many rows/columns the "sweep" operation is performed
        if direction in [UP,DOWN]:
            num_tiles = self._grid_height
        elif direction in [LEFT,RIGHT]:
            num_tiles = self._grid_width
            
        
        # This block iterates the merge function over each column/row associated with the move direction.
        # line_tiles stores the indices of tiles within a row/column
        # line_vals stores the values of a row/column 
        # Merge line_vals into a new list
        tile_is_changed = False
        for a_tile in self._starting_tiles[direction]:
            line_vals = [0] * num_tiles
            line_tiles = []
            current_tile = [a_tile[0], a_tile[1]]
            for num_iter in range(num_tiles):
                line_tiles.append((current_tile[0], current_tile[1]))
                line_vals[num_iter] = self._grid[current_tile[0]][current_tile[1]]
                current_tile[0] += OFFSETS[direction][0]
                current_tile[1] += OFFSETS[direction][1]

            merged_line = merge(line_vals)
            
            # Copy the merged list back into the grid and check if any tile has changed
            
            for num_iter in range(len(line_tiles)):
                tile = line_tiles[num_iter]
                if self._grid[tile[0]][tile[1]] != merged_line[num_iter]:
                    self._grid[tile[0]][tile[1]] = merged_line[num_iter]
                    tile_is_changed = True
        
        # If there is a change, add a new tile into the grid 
        if tile_is_changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Get the positions of tiles with zeros and choose a position randomly
        tiles_with_zeros = []
        tiles_with_zeros = [(row,col) for row in range(self._grid_height) \
                                     for col in range(self._grid_width) \
                                     if self._grid[row][col] == 0]
        new_pos = random.choice(tiles_with_zeros)
        # Generate a 2 or 4 90% or 10% of the time, respectively, then insert into new_pos
        if random.random() < 0.9:
            self.set_tile(new_pos[0],new_pos[1],2)
        else:
            self.set_tile(new_pos[0],new_pos[1],4)     
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
