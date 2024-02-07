# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver


"""
Creating the graph for a bigger graph than 3x3 is way too slow
3X3 is already slow (representing a 9! nodes graph)
I might optimize my program for solving 3x3 faster but we can't imagine solving NxM grid with n,m>=4 by
building the entire graph
"""

class Test_SolutionGrapheOptimized(unittest.TestCase):
    def test_solution_graphe(self):
        grid1 = Grid.grid_from_file("input/grid1.in")
        grid2= Grid.grid_from_file("input/grid2.in")
        grid3= Grid.grid_from_file("input/grid0.in")
        solv1= Solver(grid1)
        solv2 = Solver(grid2)
        solv3=Solver(grid3)
        res1= solv1.get_solution_graphe_optimized()
        res2= solv2.get_solution_graphe_optimized()
        res3= solv3.get_solution_graphe_optimized()
        grid1.swap_seq(res1)
        grid2.swap_seq(res2)
        grid3.swap_seq(res3)
        self.assertEqual(grid1.is_sorted(), True)
        self.assertEqual(grid2.is_sorted(), True)
        self.assertEqual(grid3.is_sorted(), True)

if __name__ == '__main__':
    unittest.main()