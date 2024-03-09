"""
This is the graph module. It contains a minimalistic Graph class.
"""
from grid import Grid

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
        graph = self.graph

        # détermination d'un chemin reliant src et dst
        queue = graph[src]
        visited = [src]

        father = {}
        for node in queue:
            father[node] = src

        while queue:
            current = queue.pop(0)  # on prend le premier élément de la file.
            visited.append(current)  # on le visite.

            neighbors = graph[current]  # on isole ses voisins.
            for neighbor in neighbors:
                if neighbor == dst:  # dans ce cas on a trouvé un chemin reliant src et dst donc pas besoin de continuer la recherche.
                    visited.append(dst)
                    father[dst] = current
                    queue = []  # permet de sortir de la boucle while.

                elif (neighbor not in visited) and (neighbor not in queue):  # si neighbor n'a pas encore été considéré.
                    queue.append(neighbor)  # on le met dans la file.
                    father[neighbor] = current

        if visited[-1] != dst:  # on vérifie qu'un chemin entre src et dst existe.
            return None

        # optimisation du chemin reliant src et dst à partir de visited.
        child = dst
        father = father[dst]
        chemin = [dst]  # on va remplir le chemin en partant de dst.
        while child != src :
            child = father
            father = father[child]
            chemin = [child] + chemin
        return chemin

    
    def A_star(self,src,dst):
        open_list=[(src.hash(),0,src.dist(dst,self),[])] # içi la liste source n'a pas de père.
        closed_list=[]
        path=[]
          
        while open_list:
            if open_list[0][0]==dst:
                
                path.append(dst)
                father=open_list[0][3]
                while father: # Permet de remonter jusqu'a la grille source qui est la seule à ne pas avoir de père.
                    
                    for acn in closed_list : #acn pour already closed nodes.
                        if acn[0] ==father:
                            open_list[0]=acn
                            path.append(acn[0])
                            father=open_list[0][3]
                open_list=[] #Permet de sortir de la première boucle while.
            else:
                icl=False #icl pour in closed list.
                for i in range (0, len(closed_list)): 
                    if closed_list[i][0]==open_list[0][0]:
                        icl= True
                        if closed_list[i][2]> open_list[0][2]: #si  l'heuristique du noeud déjà visité est meilleure alors on le remplace  dans la liste afin d'obtenir le meilleur père possible. 
                            closed_list[i]= open_list[0]
                            neighbors = graph[open_list[0][0]]
                            for neighbor in neighbors:
                                neighbor1=Grid(src.m, src.n, neighbor)
                                open_list.append((neighbor1.hash(), open_list[0][1]+1, open_list[0][1]+1+neighbor1.dist(dst, self), open_list[0][0])) #on définit le nouveau coût de ses voisins ainsi que la nouvelle heuristique.
                        open_list.pop(0)
                        open_list.sort(key=lambda x: x[2]) # Permet de trier la grille selon les heuristiques.
                        
                if not icl: # Si icl vaut True on a déjà effectué les opérations nécessaires.
                    closed_list.append(open_list[0])
                    neighbors = graph[open_list[0][0]]
                    for neighbor in neighbors:
                        neighbor1 = Grid(src.m, src.n, neighbor)
                        open_list.append((neighbor1.hash(), open_list[0][1]+1, open_list[0][1]+1+neighbor1.dist(dst, self), open_list[0][0]))
                    open_list.pop(0)
                    open_list.sort(key=lambda x: x[2])

        return path

                    

                


                




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
                    graph.add_edge(node1, node2)  # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph

