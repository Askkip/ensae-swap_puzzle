from queue import Queue

"""
This is the graph module. It contains a minimalistic Graph class.
"""


class Graph:
    """
    A class representing undirected graphs as adjacency lists. 

    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes 
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        
    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return f"<graph.Graph: nb_nodes={self.nb_nodes}, nb_edges={self.nb_edges}>"

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 
        When adding an edge between two nodes, if one of the ones does not exist it is added to the list of nodes.

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if not ((node1,node2) in self.edges or (node2,node1) in self.edges) : 
            if node1 not in self.graph:
                self.graph[node1] = []
                self.nb_nodes += 1
                self.nodes.append(node1)
            if node2 not in self.graph:
                self.graph[node2] = []
                self.nb_nodes += 1
                self.nodes.append(node2)

            self.graph[node1].append(node2)
            self.graph[node2].append(node1)
            self.nb_edges += 1
            self.edges.append((node1, node2))


    def bfs(self, src, dst): 
        """
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
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
        seen = [False for _ in range(0,self.nb_nodes)]
        distance = [float("inf") for _ in range(0,self.nb_nodes)]
        predecessors = [-1 for _ in range(0,self.nb_nodes)]
        #there is a bijection between [0....nb_nodes] and [self.node[0] ... self.nodes[nb_nodes]]
        #initialization
        distance[self.nodes.index(src)]  = 0
        queue.put(src)
        seen[self.nodes.index(src)]  = True

        while not queue.empty():
            elt = queue.get()
            idx_elt = self.nodes.index(elt)
            for neighbor in self.graph[elt]:
                idx_neigh = self.nodes.index(neighbor)
                if not seen[idx_neigh] :
                    queue.put(neighbor)
                    seen[idx_neigh] = True
                    distance[idx_neigh] = distance[idx_elt]+1
                    predecessors[idx_neigh] = elt
                if neighbor == dst:
                    path = [dst]
                    idx_dst = self.nodes.index(dst)
                    x = predecessors[idx_dst]
                    while x != src :
                        path.append(x)
                        x = predecessors[self.nodes.index(x)]
                    path.append(x)
                    path.reverse()
                    return path
        return None


    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters: 
        -----------
        file_name: str
            The name of the file

        Outputs: 
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2) # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph
    
if __name__ == '__main__':
    # g = Graph([((1, 2), (3, 4)), ((1, 2), (4, 3)), ((1, 3), (2, 4)), ((1, 3), (4, 2)), ((1, 4), (2, 3)), ((1, 4), (3, 2)), ((2, 1), (3, 4)), ((2, 1), (4, 3)), ((2, 3), (1, 4)), ((2, 3), (4, 1)), ((2, 4), (1, 3)), ((2, 4), (3, 1)), ((3, 1), (2, 4)), ((3, 1), (4, 2)), ((3, 2), (1, 4)), ((3, 2), (4, 1)), ((3, 4), (1, 2)), ((3, 4), (2, 1)), ((4, 1), (2, 3)), ((4, 1), (3, 2)), ((4, 2), (1, 3)), ((4, 2), (3, 1)), ((4, 3), (1, 2)), ((4, 3), (2, 1))])
    # print(g)
    # g.add_edge("f","e")
    # g.add_edge("f","e")
    # g.add_edge("f","a")
    # g.add_edge("e",'a')
    # g.add_edge("a","x")
    # g.add_edge("y","x")
    # print(g)
    # print(g.graph)
    # print(g.nodes)
    # print(g.edges)
    # print(g.bfs("f","y"))
    pass


