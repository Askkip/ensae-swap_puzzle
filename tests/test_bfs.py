# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")
sys.path.append("input/")
import unittest
from graph import Graph
import numpy as np


class Test_SolutionBFS(unittest.TestCase):
    def test_solution_naive(self):
        g1 = Graph.graph_from_file("input/graph1.in")
        g2 = Graph.graph_from_file("input/graph2.in")
        with open("input/graph1.path.out", "r") as file:
            for _ in range(190):
                row = file.readline().strip().split()
                #print(row)
                src,dst,length = int(row[0]),int(row[1]),int(row[2])
                path = [int(element.removeprefix("[").removesuffix(']').removesuffix(",")) for element in row[3:]]
                path_to_test = g1.bfs(src,dst)
                self.assertEqual(np.array_equal(path_to_test,path), True)
        with open("input/graph2.path.out", "r") as file:
            for _ in range(190):
                row = file.readline().strip().split()
                src,dst,length = int(row[0]),int(row[1]),eval(row[2])
                path = [int(element.removeprefix("[").removesuffix(']').removesuffix(",")) for element in row[3:]]
                path_to_test = g2.bfs(src,dst)
                #print(f"{path} et le testé est {path_to_test}")
                if length == None:
                    if path_to_test == None :
                        continue
                self.assertEqual(np.array_equal(path_to_test,path), True)

        

if __name__ == '__main__':
    unittest.main()