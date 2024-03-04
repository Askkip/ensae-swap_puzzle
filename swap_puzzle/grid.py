"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import random
import numpy as np
import copy
import pygame as pg

BLOCK_SIZE = 200
BLACK = (0,0,0)
WHITE = (255, 255, 255)

def shuffle_along_axis(x,axis):
    idx = np.random.rand(*x.shape).argsort(axis=axis)
    return np.take_along_axis(x,idx,axis=axis)

class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks if the current state of the grid is sorted and returns the answer as a boolean.
        """
        sorted_grid = [list(range(i*self.n+1, (i+1)*self.n+1)) for i in range(self.m)]
        return np.array_equal(sorted_grid,self.state)

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        i1,j1 = cell1
        i2,j2=cell2
        #Check if the swap is permitted
        if not ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)):
            raise ValueError("The swap is not permitted")
        
        tmp = self.state[i1][j1]
        self.state[i1][j1] = self.state[i2][j2]
        self.state[i2][j2] = tmp
        

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for (cell1,cell2) in cell_pair_list:
            self.swap(cell1,cell2)

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid
    
    def hashable_state(self):
        """
        Return a non mutable (hashable) representation of the grid in order to stock it as a node
        """
        return tuple([tuple(inner_list) for inner_list in self.state])
    
    def ui_building(self):
        """
        Create a display of the grid with pygame

        """
        pg.init()
        self.display = pg.display.set_mode((self.n*BLOCK_SIZE,self.m*BLOCK_SIZE))
        self.display.fill(WHITE)
        pg.display.set_caption("Swap Puzzle")
        font = pg.font.Font('arial.ttf', 25)
        for list in self.state:
            for x in list:
                left = self.state.index(list)*BLOCK_SIZE
                top = list.index(x)*BLOCK_SIZE
                pg.draw.rect(self.display,BLACK,pg.Rect(top,left,BLOCK_SIZE,BLOCK_SIZE),5) 
                mid_top = top + (BLOCK_SIZE)/2
                mid_left = left +(BLOCK_SIZE)/2
                text = font.render(str(x),True, BLACK)
                self.display.blit(text,(mid_top,mid_left))
        pg.display.flip()
        while True :
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

    @staticmethod
    def build_controlled_difficulty_grid(m,n,difficulty):
        """
        Input : 
            - m : number of rows
            - n : number of columns
            - difficulty (int) between 1 and 3
        Output : 
            Grid Object
            A Grid Object with an initial state depending the difficulty we want
        """
        g = Grid(m,n)
        if difficulty == 1 : #shuffle only one row
            np.random.shuffle(g.state[random.randint(0,m-1)])
        if difficulty == 2 : #shuffle all rows but not columns
            for i in range(0,m):
                np.random.shuffle(g.state[i])
        if difficulty == 3 : #shuffle all the matrix 
            g.state = shuffle_along_axis(np.array(g.state),0)
            g.state = shuffle_along_axis(np.array(g.state),1)
            g.state = g.state.tolist()
        return g

if __name__ == '__main__':
    g = Grid.build_controlled_difficulty_grid(1,100,3)
    print(g.state)


