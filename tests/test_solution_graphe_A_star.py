# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph




class Test_SolutionGrapheAstar(unittest.TestCase):
    def test_solution_graphe(self):
        grid0 = Grid.grid_from_file("input/grid0.in")
        grid1 = Grid.grid_from_file("input/grid1.in")
        grid2= Grid.grid_from_file("input/grid2.in")
        grid3= Grid.grid_from_file("input/grid3.in")
        grid4= Grid.grid_from_file("input/grid4.in")
        #grid3= Grid.build_controlled_difficulty_grid(1,100,2)
        solv0= Solver(grid0)
        solv1= Solver(grid1)
        solv2 = Solver(grid2)
        solv3=Solver(grid3)
        solv4=Solver(grid4)
        res0= solv0.get_solution_graphe_a_star(Graph.h_wrong_place)
        res1= solv1.get_solution_graphe_a_star(Graph.h_wrong_place)
        res2= solv2.get_solution_graphe_a_star(Graph.h_wrong_place)
        res3= solv3.get_solution_graphe_a_star(Graph.h_wrong_place)
        res4= solv4.get_solution_graphe_a_star(Graph.h_wrong_place)
        self.assertEqual(grid0.is_sorted(), True)
        self.assertEqual(grid1.is_sorted(), True)
        self.assertEqual(grid2.is_sorted(), True)
        self.assertEqual(grid3.is_sorted(), True)
        self.assertEqual(grid4.is_sorted(), True)

if __name__ == '__main__':
    unittest.main()