from grid import Grid
from graph import Graph
import copy
import random
import sys
import numpy as np
from itertools import permutations
from queue import Queue
from heapq import *

class dict_default_modified(dict):
    """
    Create a dict where if there is a missing key we return inf.
    It's used to implement dist
    """
    def __missing__(self, key, value_by_default = float("inf")):
        return value_by_default

def factorielle(n):
    if n < 0:
        raise ValueError("Negative value")
    elif n == 0:
        return 1
    else:
        resultat = [1] * (n + 1)
        for i in range(2, n + 1):
            resultat[i] = resultat[i - 1] * i
    return resultat

UP = (-1,0)
DOWN =(1,0)
RIGHT = (0,1)
LEFT = (0,-1)
directions = [UP,DOWN,RIGHT,LEFT]

class Solver(): 
    """
    Input : 
        grid : Grid object
        forbiden_moves : list of tuples by default []
                        example : [((1,1),(2,1)),((0,0),(1,0))]
    We decided that each solver has his initial grid 
    """
    def __init__(self,grid,forbiden_moves=[]) -> None:
        self.grid = grid
        self.forbiden_moves = forbiden_moves


    
    def legal_move(self,x,y):
        i1,j1 = x
        i2,j2 =y
        not_forbiden = True
        if (x,y) in self.forbiden_moves or (y,x) in self.forbiden_moves:
            not_forbiden = False
        return 0<=i1<self.grid.m and 0<=j1<self.grid.n and 0<=i2<self.grid.m and 0<=j2<self.grid.n and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)) and not_forbiden 
    
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
    def move_needed(state1,state2,forbiden_moves=[]):
        """
        Giving 2 grid that differs from one swap, find the swap they have in common
        """
        state1l = [list(inner_tuple) for inner_tuple in state1]
        state2l = [list(inner_tuple) for inner_tuple in state2]
        g1 = Grid(len(state1),len(state1[0]),state1l)
        g2 = Grid(len(state2),len(state2[0]),state2l)
        solv = Solver(g1,forbiden_moves)
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
                move_close_to_x = [Solver.sum_term_tuple(x,y) for y in directions]
                for t in move_close_to_x:
                    if self.legal_move(x,t) and (t,x) not in possible_moves and (t,x) not in self.forbiden_moves :
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
     
        while actual_place != right_place :
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
            moves = moves + self.place(i)
        return moves
    #Complexité en O(mn^2) et en moyenne en O(mn*max(n,m))


    @staticmethod
    def generate_matrices(n, m):
        """
        Return a list of all the possible n x m matrix filled with numbers from 1 to nm
        Output : list of tuples ; each tuple is a grid
        Example : [((1,2),(3,4)),((2,1),(3,4)).....]
        """
        numbers = [i for i in range(1, n*m + 1)]
        perms = permutations(numbers, n*m)
        matrices = []

        for perm in perms:
            matrix = tuple([tuple(perm[i*m:(i+1)*m]) for i in range(n)])
            matrices.append(matrix)

        return matrices
    
    

    def build_edges(self,g,state):
        """
        Connect each state to his neighbours because we firstly built the nodes then now we connect them
        No output
        """
        list_state = [list(t) for t in state]
        grid = Grid(self.grid.m,self.grid.n,list_state)
        self.grid = grid
        l = self.possible_moves()
        for cell1,cell2 in l :
            self.grid.swap(cell1,cell2)
            node = self.grid.hashable_state()
            g.add_edge(state,node)
            self.grid.swap(cell1,cell2) #put back the changement

    
    def build_graph(self):
        """
        Build a graph where each node is a state of the grid and there is an edge between 2 nodes
        if and only if u can go from a state to another with a legal swap
        Output : Graph object
        Side effect : None
        """
        tmp = copy.deepcopy(self.grid.state) #to put back any changement
        matrices = Solver.generate_matrices(self.grid.m,self.grid.n)
        g = Graph(matrices)
        for state in g.nodes:
            self.build_edges(g,state)
        self.grid.state = tmp
        return g
    #Complexité en O((nm)!)



    def get_solution_graphe(self):
        """
        Find the shortest path in the state graph built previously
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 

        """
        if self.grid.m == 1:
            return self.get_solution_1xn_case()
        g = self.build_graph()
        src = self.grid.hashable_state()
        goal = Grid(self.grid.m,self.grid.n)
        dst = goal.hashable_state()
        state_path = g.bfs(src,dst)
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
    #Complexity is O((mn)!) worst than the naive solution

    @staticmethod
    def compute_neighbors(graph,state,m,n,forbiden_moves=[]):
        """
        Add the neighbors of elt in the graph
        Input : 
        graph = Graph Object ; 
        state = hashable object
        Output : NA
        """
        list_state = [list(t) for t in state]
        solver = Solver(Grid(m,n,list_state),forbiden_moves) #solver associated with the state of which we want to compute neighbors
        possible_moves = solver.possible_moves()
        for cell1,cell2 in possible_moves:
            solver.grid.swap(cell1,cell2)
            hashable_node = solver.grid.hashable_state()
            graph.add_edge(hashable_node,state)
            solver.grid.swap(cell1,cell2)


    def bfs_optimized(self, graph,src, dst): 
        """
        Finds a shortest path from src to dst by BFS following the solving graph optimized method.
        My idea is to modify the BFS, it starts with a graph that only contain the src node 
        and when it explores a node we build all its neighbours   

        Parameters: 
        -----------
        graph : Graph object
            The graph with only 1 node that is the source node.
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """ 
        queue = Queue()
        sup = factorielle(self.grid.m*self.grid.n)[self.grid.m*self.grid.n]
        seen = [False for _ in range(0,sup)] #way too large, I could replace it by a dict TODO
        distance = [float("inf") for _ in range(0,sup)]
        predecessors = [-1 for _ in range(0,sup)]
        #there is a bijection between [0....nb_nodes] and [self.node[0] ... self.nodes[nb_nodes]]
        #initialization

        distance[graph.nodes.index(src)]  = 0
        queue.put(src)
        seen[graph.nodes.index(src)]  = True

        while not queue.empty():
            elt = queue.get()
            idx_elt = graph.nodes.index(elt)
            Solver.compute_neighbors(graph,elt,self.grid.m,self.grid.n,self.forbiden_moves) #add the neighbors of elt in the graph
            for neighbor in graph.graph[elt]:
                idx_neigh = graph.nodes.index(neighbor)
                if not seen[idx_neigh] :
                    queue.put(neighbor)
                    seen[idx_neigh] = True
                    distance[idx_neigh] = distance[idx_elt]+1
                    predecessors[idx_neigh] = elt
                if neighbor == dst: #BFS assure you that the fisrt time you visit the dst node, is the good one
                    #Build the path
                    path = [dst] 
                    idx_dst = graph.nodes.index(dst)
                    x = predecessors[idx_dst]
                    while x != src :
                        path.append(x)
                        x = predecessors[graph.nodes.index(x)]
                    path.append(x)
                    path.reverse()
                    return path
        return None    
    
    def get_solution_graphe_optimized(self):
        """
        Find the shortest path in the graph which is built gradually
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 

        My idea is to modify the BFS, it starts with a graph that only contain the src node 
        and when it explores a node we build all its neighbours 

        Side effect : Solve the grid
        """
        if self.grid.m == 1:
            return self.get_solution_1xn_case()
        src = self.grid.hashable_state()
        goal = Grid(self.grid.m,self.grid.n)
        dst = goal.hashable_state()
        graph = Graph([src])
        state_path = self.bfs_optimized(graph,src,dst)
        if state_path == None :
            return None
        #we have the list of the different state we need to follow to order the grid
        #but we want the sequence of swaps, so we are gonna extrat the list of the swap neccessary
        path = []
        for i in range(0,len(state_path)-1):
            state1,state2 = state_path[i],state_path[i+1]
            move_needed = Solver.move_needed(state1,state2)
            path.append(move_needed)
        self.grid.swap_seq(path)
        return path
    

    
    def a_star_opimized(self,graph,src,dst,h):
        """
        Finds a shortest path from src to dst by A* by building the graph gradually.
        My idea is to modify the A* function, it starts with a graph that only contain the src node 
        and when it explores a node we build all its neighbours   

        Parameters: 
        -----------
        graph : Graph object
            The graph with only 1 node that is the source node.
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.
        h : The heuristic function (NodeType -> int)

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """ 
        prio_queue = []
        dist = dict_default_modified({}) #dist[v] = the actual shortest distance btw src and v 
        dist[src] = 0
        parents = {}
        heappush(prio_queue,(h(src),src))

        while len(prio_queue) != 0:
            heur, node = heappop(prio_queue)
            Solver.compute_neighbors(graph,node,self.grid.m,self.grid.n,self.forbiden_moves) #add the neighbors of elt in the graph
            if node == dst :
                node_path = Graph.reconstruct(parents,src,dst)
                return node_path
            for neighbour in graph.graph[node]:
                d = dist[node] + 1 # p(node->neighbour) = 1 because our graph is not ponderated
                if d < dist[neighbour]:
                    dist[neighbour] = d
                    parents[neighbour] = node
                    Graph.decrease_or_push(prio_queue,neighbour,d+h(neighbour))
        return None    
    

    def get_solution_graphe_a_star(self,h=(lambda x : 0)):
        """
        Find the shortest path with A* in the graph which is built gradually
        Solves the grid and returns the sequence of swaps at the format 
        Output : [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 

        Side effect : Solve the grid
        """
        if self.grid.m == 1:
            return self.get_solution_1xn_case()
        src = self.grid.hashable_state()
        goal = Grid(self.grid.m,self.grid.n)
        dst = goal.hashable_state()
        graph = Graph([src])
        state_path = self.a_star_opimized(graph,src,dst,h)
        if state_path == None :
            return None
        #we have the list of the different state we need to follow to order the grid
        #but we want the sequence of swaps, so we are gonna extrat the list of the swap neccessary
        path = []
        for i in range(0,len(state_path)-1):
            state1,state2 = state_path[i],state_path[i+1]
            move_needed = Solver.move_needed(state1,state2)
            path.append(move_needed)
        self.grid.swap_seq(path)
        return path
    
    def get_solution_1xn_case(self):
        """
        We use an insertion sort because our grid is a list and the insertion sort is the 
        sort algorithm with the smallest amount of swaps
        
        Side effect : Solve the grid
        Output : Swaps made to solve the grid
                    example : [((0,0),(0,2)),((0,1),(0,3)),..]
        """
        assert(self.grid.m == 1)
        liste = self.grid.state[0]
        swap = []  
    
        for i in range(1, len(liste)):
            element_courant = liste[i]
            j = i - 1
            while j >= 0 and liste[j] > element_courant:
                liste[j + 1] = liste[j]
                swap.append(((0,j),(0,j + 1)))  
                j -= 1
            liste[j + 1] = element_courant

        return swap





if __name__ == '__main__':
    pass





        

