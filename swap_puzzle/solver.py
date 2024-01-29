from grid import Grid
from graph import Graph
import copy
import random
import sys
import numpy as np

sys.setrecursionlimit(5000)

UP = (-1,0)
DOWN =(1,0)
RIGHT = (0,1)
LEFT = (0,-1)
directions = [UP,DOWN,RIGHT,LEFT]

class Solver(): 
    """
    We decided that each solver has his initial grid 
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

    @staticmethod
    def find_place(mat,elt):
        for i, rows in enumerate(mat):
            if elt in rows:
                return i, rows.index(elt)

        return None
    
    @staticmethod
    def move_needed(state1,state2):
        """
        Giving 2 grid that differs from one swap, find the swap they have in common
        """
        state1l = [list(inner_tuple) for inner_tuple in state1]
        state2l = [list(inner_tuple) for inner_tuple in state2]
        g1 = Grid(len(state1),len(state1[0]),state1l)
        g2 = Grid(len(state2),len(state2[0]),state2l)
        solv = Solver(g1)
        possible_moves = solv.possible_moves()
        for cell1,cell2 in possible_moves:
            g1.swap(cell1,cell2)
            if np.array_equal(g1.state,g2.state):
                return (cell1,cell2)
            g1.swap(cell1,cell2)
        raise Exception(f"The 2 grids differs from more than 1 swap {state1} and {state2}")

    
    def possible_moves(self):
        """
        Return all possible_moves from a state
        
        To each state we have (4*2 + 2*(m-2)*3 + 2*(n-2)*3 + 4*(m-2)(n-2))/2 swaps possibles 
        Output : [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')),.....]
        """
        possible_moves = []
        
        for i in range(0,self.grid.m):
            for j in range(0,self.grid.n):
                x = (i,j)
                #print(x)
                move_close_to_x = [Solver.sum_term_tuple(x,y) for y in directions]
                #print(move_close_to_x)
                for t in move_close_to_x:
                    if self.legal_move(x,t) and (t,x) not in possible_moves:
                        #print(f"On append {(x,t)}")
                        possible_moves.append((x,t))
        return possible_moves

    def get_solution_naive_random(self):
        """
        Using a randomize method 
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 

        """
        acc =[]
        while not self.grid.is_sorted():
            moves_possible = self.possible_moves()
            rdm = random.randint(0,len(moves_possible)-1)
            self.grid.swap(moves_possible[rdm][0],moves_possible[rdm][1])
            acc.append(moves_possible[rdm])
        return acc


    def place(self,x):
        """
        Place x to his right position without moving the element 1,2....x-1
        that are supposed to be in their final place
        Side effect : order the grid associate to the Solver
        Output : moves that have been made  [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        grid_ordered = Grid(self.grid.m,self.grid.n)
        right_place = Solver.find_place(grid_ordered.state,x)
        actual_place = Solver.find_place(self.grid.state,x)
        moves_done =[]
        i_a,j_a = actual_place
        i_r,j_r = right_place
        moves_to_do =[]
        if i_a>i_r:
            moves_to_do.append(UP)
        if i_a<i_r:
            moves_to_do.append(DOWN)
        if j_a<j_r:
            moves_to_do.append(RIGHT)
        if j_a>j_r:
            moves_to_do.append(LEFT)

        
        while actual_place != right_place :
            idx = 0 #keep it between 0 and len(moves_to_do)
            next_place = Solver.sum_term_tuple(actual_place,moves_to_do[idx])
            i,j = next_place
            if self.grid.state[i][j] < x : #if in the emplacement there is an already placed numbers, use an other direction
                idx = (idx +1)%len(moves_to_do)
                next_place = Solver.sum_term_tuple(actual_place,moves_to_do[idx])
                i,j = next_place

            self.grid.swap(actual_place,next_place)
            moves_done.append((actual_place,next_place))
            actual_place = next_place

        return moves_done
    #Complexité de cette fonction en O(mn) car au pire des cas mn opérations en 0(1) même si en pratique c'est beaucoup moins ça serait plus max(n,m) opérations en moyenne

            
    def get_solution_naive(self):
        """
        Move each number in its right place by treating them in ascending order

        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        moves =[]
        max_number = self.grid.n*self.grid.m
        for i in range(1,max_number+1):
            #print(f"on move {i} à sa bonne place ")
            moves = moves + self.place(i)
        return moves
    #Complexité en O(mn^2) et en moyenne en O(mn*max(n,m))

    def build_graph(self):
        """
        Build a graph where each node is a state of the grid and there is an edge between 2 nodes
        if and only if u can go from a state to another with a legal swap
        Output : Graph object
        """
        g = Graph()
        possibles_moves = self.possible_moves()
        memory = copy.deepcopy(self.grid.state) #Remember the state for putting back the state of the grid at the end of the function

        for swap1,swap2 in possibles_moves :
            non_mutable_state = self.grid.hashable_state()
            for cell1,cell2 in possibles_moves:
                self.grid.swap(cell1,cell2)
                non_mutable_new_state = self.grid.hashable_state()
                if (non_mutable_state,non_mutable_new_state) not in g.edges or (non_mutable_new_state,non_mutable_state) not in g.edges: 
                        g.add_edge(non_mutable_state,non_mutable_new_state)
                self.grid.swap(cell1,cell2) #put back the changement

            self.grid.swap(swap1,swap2)
            non_mutable_state = self.grid.hashable_state()
        
        self.grid.state = memory
        return g 

    def get_solution_graphe(self):
        """
        Find the shortest path in the state graph built previously
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        #print(self.grid)
        g = self.build_graph()
        src = self.grid.hashable_state()
        #print(src)
        goal = Grid(self.grid.m,self.grid.n)
        dst = goal.hashable_state()
        state_path = g.bfs(src,dst)
        #print(f"state_path = {state_path}") 
        if state_path == None :
            return None
        #we have the list of the different state we need to follow to order the grid
        #but we want the sequence of swaps, so we are gonna extrat the list of the swap neccessary
        path = []
        for i in range(0,len(state_path)-1):
            state1,state2 = state_path[i],state_path[i+1]
            move_needed = Solver.move_needed(state1,state2)
            path.append(move_needed)
        return path



if __name__ == '__main__':
    g = Grid(2,3)
    g.swap((0,0),(0,1))
    g.swap((0,0),(1,0))
    print(g)
    #print(g.hashable_state())
    # g1 = Grid(2,3)
    # g1.swap((0,0),(0,1))
    # g1.swap((0,0),(1,0))
    # g2 = Grid.grid_from_file("input/grid1.in")
    # g3 = Grid.grid_from_file("input/grid2.in")
    solv = Solver(g)
    #graph = solv.build_graph()
    #print(graph.edges)
    print(solv.get_solution_graphe())
    # l=solv.possible_moves()
    # print(f"moove possible =  {l}")
    # #solv2 = Solver(g2)
    # #solv3=Solver(g3)
    # #l2 = solv2.get_solution_naive_random()
    # #l3 = solv3.get_solution_naive_random()
    # #res = solv.get_solution_naive_random()
    # #print(len(l2),len(l3),len(res))
    # #g1.swap_seq(res)
    # #print(g1)
    # #res = solv.get_solution_naive()
    # #print(res)
    # res1 = solv.get_solution_naive()
    # print(res1)
    # g1.swap_seq(res1)
    # print(g1)
    # grid1 = Grid.grid_from_file("input/grid1.in")
    # grid2= Grid.grid_from_file("input/grid2.in")
    # grid3= Grid.grid_from_file("input/grid3.in")
    # solv1= Solver(grid1)
    # solv2 = Solver(grid2)
    # solv3=Solver(grid3)
    # res1= solv1.get_solution_naive()
    # res2= solv2.get_solution_naive()
    # res3= solv3.get_solution_naive()


        
    # grid1.swap_seq(res1)
    # grid2.swap_seq(res2)
    # grid3.swap_seq(res3)
    # solv1.place(7)
    # print(grid1)
    # print(grid2)
    # print(grid3)
    pass






        

