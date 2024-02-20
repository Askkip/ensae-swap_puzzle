# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph

def test_forbid(tested,forb=[]):
    for t in tested:
        (x,y) = t
        if (x,y) in forb or (y,x) in forb:
            return False
    return True


class Test_SolutionGrapheAstarForbidenMoves(unittest.TestCase):
    def test_solution_graphe(self):
        grid0 = Grid.grid_from_file("input/grid0.in")
        grid1 = Grid.grid_from_file("input/grid1.in")
        grid2= Grid.grid_from_file("input/grid2.in")
        grid3= Grid.grid_from_file("input/grid3.in")
        grid4= Grid.grid_from_file("input/grid4.in")
        fm0 = [((1,1),(1,0))]
        fm1 = [((0,0),(1,0)),((3,0),(3,1))]
        fm2 = [((1,1),(1,0)),((1,1),(1,2)),((1,1),(2,1))]
        fm3 = [((1,1),(1,0)),((1,1),(2,1)),((3,3),(2,3))]
        #grid3= Grid.build_controlled_difficulty_grid(4,4,2)
        solv0= Solver(grid0,fm0)
        solv1= Solver(grid1,fm1)
        solv2 = Solver(grid2,fm2)
        solv3=Solver(grid3,fm3)
        solv4=Solver(grid4)
        res0= solv0.get_solution_graphe_a_star(Graph.h_wrong_place)
        res1= solv1.get_solution_graphe_a_star(Graph.h_wrong_place)
        res2= solv2.get_solution_graphe_a_star(Graph.h_wrong_place)
        res3= solv3.get_solution_graphe_a_star(Graph.h_wrong_place)
        res4= solv4.get_solution_graphe_a_star(Graph.h_wrong_place)

        self.assertEqual(test_forbid(res0,fm0), True)
        self.assertEqual(test_forbid(res1,fm1), True)
        self.assertEqual(test_forbid(res2,fm2), True)
        self.assertEqual(test_forbid(res3,fm3), True)

        self.assertEqual(grid0.is_sorted(), True)
        self.assertEqual(grid1.is_sorted(), True)
        self.assertEqual(grid2.is_sorted(), True)
        self.assertEqual(grid3.is_sorted(), True)
        self.assertEqual(grid4.is_sorted(), True)

if __name__ == '__main__':
    unittest.main()