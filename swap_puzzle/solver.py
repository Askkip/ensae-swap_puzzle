from grid import Grid
import copy
import random

UP = (-1,0)
DOWN =(1,0)
RIGHT = (0,1)
LEFT = (0,-1)
directions = [UP,DOWN,RIGHT,LEFT]

class Solver(): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,grid) -> None:
        self.grid = grid


    
    def legal_move(self,x,y):
        i1,j1 = x
        i2,j2 =y
        return 0<=i1<self.grid.m and 0<=j1<self.grid.n and 0<=i2<self.grid.m and 0<=j2<self.grid.n and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1))
    @staticmethod
    def sum_term_tuple(x,y):
        return (x[0]+y[0],x[1]+y[1])

    
    def possible_moves(self,grid):
        """
        Return all possible_moves from a state
        Warning : each move apperas twice
        Output : [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')),.....]
        """
        possible_moves = []
        #n = grid.n
        #m = grid.m
        #we add the four corners
        #possible_moves += [((0,0),(0,1)),((0,0),(1,0)),((0,n-1),(0,n-2)),((0,n-1),(1,n-1)),((m-1,0),(m-1,1)),((m-1,0),(m-2,0)),((m-1,n-1),(m-1,n-2)),((m-1,n-1),(m-2,n-1))]
        
        for i in range(0,self.grid.m):
            for j in range(0,self.grid.n):
                x = (i,j)
                #print(x)
                move_close_to_x = [Solver.sum_term_tuple(x,y) for y in directions]
                #print(move_close_to_x)
                for t in move_close_to_x:
                    if self.legal_move(x,t):
                        #print(f"On append {(x,t)}")
                        possible_moves.append((x,t))
        return possible_moves

    def get_solution_naive_random(self):
        acc =[]
        while not self.grid.is_sorted():
            moves_possible = self.possible_moves()
            rdm = random.randint(0,len(moves_possible)-1)
            self.grid.swap(moves_possible[rdm][0],moves_possible[rdm][1])
            acc.append(moves_possible[rdm])
        return acc



    def get_solution_naive(self):
        """
        We are gonna enumerate all the sequences of possible swaps
        To each state we have (4*2 + 2*(m-2)*3 + 2*(n-2)*3 + 4*(m-2)(n-2))/2 swaps possibles 

        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        def aux(grid,acc,nb_coup): #acc = accumulation of moves do since the beginning
            if grid.is_sorted():
                return acc
            if nb_coup > 100:
                return
            l = self.possible_moves(grid)
            for move in l:
                x,y = move
                new_g = Grid(grid.m,grid.n,copy.deepcopy(grid.state))
                new_g.swap(x,y)
                aux(new_g,acc+[move],nb_coup+1)

        aux(self.grid,[],0)
            



if __name__ == '__main__':
    g = Grid(2,3)
    g.swap((0,0),(0,1))
    g.swap((0,0),(1,0))
    print(g)
    g1 = Grid(2,3)
    g1.swap((0,0),(0,1))
    g1.swap((0,0),(1,0))
    g2 = Grid.grid_from_file("input/grid1.in")
    g3 = Grid.grid_from_file("input/grid2.in")
    solv = Solver(g)
    #l=solv.possible_moves()
    #print(f"moove possible =  {l}")
    #solv2 = Solver(g2)
    #solv3=Solver(g3)
    #l2 = solv2.get_solution_naive_random()
    #l3 = solv3.get_solution_naive_random()
    #res = solv.get_solution_naive_random()
    #print(len(l2),len(l3),len(res))
    #g1.swap_seq(res)
    #print(g1)
    res = solv.get_solution_naive()
    print(res)

        

