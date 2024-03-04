# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph
from copy import deepcopy



class Test_SolutionGrapheAstar(unittest.TestCase):
    def test_solution_graphe(self):
        grid0 = Grid.build_controlled_difficulty_grid(1,70,2)
        cgrid0 = Grid(1,70,deepcopy(grid0.state)) 
        grid1 = Grid.build_controlled_difficulty_grid(1,70,3)
        cgrid1 = Grid(1,70,deepcopy(grid1.state)) 
        grid2= Grid.build_controlled_difficulty_grid(1,20,2)
        grid4= Grid.build_controlled_difficulty_grid(1,500,2)
        grid3= Grid.build_controlled_difficulty_grid(1,100,2)

        solv0= Solver(grid0)
        solvc0 = Solver(cgrid0)
        solv1= Solver(grid1)
        solvc1 = Solver(cgrid1)
        solv2 = Solver(grid2)
        solv3=Solver(grid3)
        solv4=Solver(grid4)

        res0= solv0.get_solution_1xn_case()
        cres0 = solvc0.get_solution_graphe_optimized()
        res1= solv1.get_solution_1xn_case()
        cres1 = solvc1.get_solution_graphe_optimized()
        res2= solv2.get_solution_1xn_case()
        res3= solv3.get_solution_1xn_case()
        res4= solv4.get_solution_1xn_case()

        self.assertEqual(grid0.is_sorted(), True)
        self.assertEqual(grid1.is_sorted(), True)
        self.assertEqual(grid2.is_sorted(), True)
        self.assertEqual(grid3.is_sorted(), True)
        self.assertEqual(grid4.is_sorted(), True)
        
        self.assertEqual(len(cres0), len(res0))
        self.assertEqual(len(cres1), len(res1))

if __name__ == '__main__':
    unittest.main()