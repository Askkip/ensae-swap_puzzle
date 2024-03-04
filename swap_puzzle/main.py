import sys
sys.path.append("swap_puzzle/")
sys.path.append("tests/")

import unittest

# Importez vos fichiers de test
from test_is_sorted import Test_IsSorted as Test1
from test_solution_BFS_optimized import Test_SolutionGrapheOptimized as Test2
from test_solution_graphe_1xn import Test_SolutionGraphe1xn as Test3
from test_solution_graphe_A_star import Test_SolutionGrapheAstar as Test4
from test_solution_naive import Test_SolutionNaive as Test5
from test_bfs import Test_SolutionBFS as Test6
from test_solution_graphe_A_star_with_forbiden_moves import Test_SolutionGrapheAstarForbidenMoves as Test7
from test_swap import Test_Swap as Test8
from test_grid_from_file import Test_GridLoading as Test9
def main():
    # Créez une suite de tests
    suite = unittest.TestSuite()

    # Chargez les tests Test_Swapà partir des classes de test
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test1))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test2))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test3))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test4))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test5))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test6))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test7))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test8))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test9))
    # Exécutez la suite de tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

if __name__ == "__main__":
    main()
