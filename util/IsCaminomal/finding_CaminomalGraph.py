class Graph:
    def __init__(self):
        self.adjacency_list = {}
    
    def add_edge(self, start, end):
        if start not in self.adjacency_list:
            self.adjacency_list[start] = []
        if end not in self.adjacency_list:
            self.adjacency_list[end] = []
        self.adjacency_list[start].append(end)
        self.adjacency_list[end].append(start)
    
    def get_dfs_code(self):
        # Start DFS from the lexicographically smallest node
        nodes = (self.adjacency_list.keys())
        nodesList=[]
        for node in nodes:
            nodesList.append(node)
        if not nodes:
            return []
        start_node = nodesList[0]
        visited = set()
        code = []
        self._dfs(start_node, visited, code)
        return code

    def _dfs(self, current, visited, code):
        visited.add(current)
        for neighbor in (self.adjacency_list[current]):
            if neighbor not in visited:
                code.append({current, neighbor})
                self._dfs(neighbor, visited, code)

def is_canonical(subgraph):
    newGraph=[]
    subgraphList=[]

    for node in subgraph:
        subgraphList.append(node)
    for i in range (0,len(subgraphList)-1,1):
        newGraph.append({subgraphList[i],subgraphList[i+1]})
    graph = Graph()
    for start, end in newGraph:
        graph.add_edge(start, end)
    g00 = graph.get_dfs_code()
    return newGraph == g00