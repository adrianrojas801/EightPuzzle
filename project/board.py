#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Adrian Rojas
# email: rojasa@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        for row in range(3):
            for col in range(3):
                tile_i = 3*row + col
                self.tiles[row][col] = digitstr[tile_i]
                if digitstr[tile_i] == '0':
                    self.blank_c = col
                    self.blank_r = row

    ### Add your other method definitions below. ###
    def __repr__(self):
        """ returns a string representation of a Board object 
            containing each tile represented by the appropriate 
            single-character string followed by a single space, with 
            the blank cell represented by an underscore character
        """
        board = ''
        for row in range(3):
            for col in range(3):
                num = self.tiles[row][col]
                if num == '0':
                    board += '_ '
                else:
                    board += num + ' '
            board += '\n'
        return board
            

    def move_blank(self, direction):
        """ takes as input a string direction that specifies the direction 
            in which the blank should move, and that attempts to modify the 
            contents of the called Board object accordingly
        """
        if direction not in 'leftrightupdown':
            return False
        for row in range(3):
            for col in range(3):
                if self.tiles[row][col] == '0':
                    if direction == 'up':
                        if self.blank_r == 0:
                            return False
                        else:
                            self.tiles[row][col] = self.tiles[row-1][col]
                            self.tiles[row-1][col] = '0'
                            self.blank_r -= 1
                            return True
                    elif direction == 'down':
                        if self.blank_r == 2:
                            return False
                        else:
                            self.tiles[row][col] = self.tiles[row+1][col]
                            self.tiles[row+1][col] = '0'
                            self.blank_r += 1
                            return True
                    elif direction == 'right':
                        if self.blank_c == 2:
                            return False
                        else:
                            self.tiles[row][col] = self.tiles[row][col+1]
                            self.tiles[row][col+1] = '0'
                            self.blank_c += 1
                            return True
                    elif direction == 'left':
                        if self.blank_c == 0:
                            return False
                        else:
                            self.tiles[row][col] = self.tiles[row][col-1]
                            self.tiles[row][col-1] = '0'
                            self.blank_c -= 1
                            return True
                        
                        
    def digit_string(self):
        """ creates and returns a string of digits that corresponds to 
            the current contents of the called Board object’s tiles 
        """
        string = ''
        for row in self.tiles:
            for num in row:
                string += num
        return string
        
        
    def copy(self):
        """ returns a newly-constructed Board object that is a deep copy 
            of the called object
        """
        return Board(self.digit_string())
        
        
    def num_misplaced(self):
        """ counts and returns the number of tiles in the called Board object 
            that are not where they should be in the goal state
        """ 
        count = 0
        for row in range(3):
            for col in range(3):
                if self.tiles[row][col] != '0':
                    if self.tiles[row][col] != GOAL_TILES[row][col]:
                        count +=1
        return count
        
    
    
    def goal_tile_pos(self, tile):
        """ finds and returns the position index of the specified tile on the 
            goal board
        """
        for row in range(3):
            for col in range(3):
                if GOAL_TILES[row][col] == tile:
                    return [row, col]
                
                
    def how_far(self):
        """ determines how far each tile is from the goal state and returns 
            the total distance that the tiles needs to move to be at its goal 
            position
        """
        distance = []
        for row in range(3):
            for col in range(3):
                tile = self.tiles[row][col]
                if tile != '0':
                    pos = self.goal_tile_pos(tile)
                    sideway_d = abs(row - pos[0]) 
                    up_down_d = abs(col - pos[1])
                    distance += [sideway_d + up_down_d]
        return sum(distance)          
        
        
    def __eq__(self, other):
        """ compares two Board objects, returning True if the called object 
            (self) and the argument (other) have the same values for the tiles 
            attribute, and False otherwise
        """
        if self.tiles == other.tiles:
            return True
        return False
 