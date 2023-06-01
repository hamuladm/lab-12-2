
from graph import Graph

def read_file(path: str, graph = Graph(), vertices = {}) -> Graph:
    with open(path) as file:
        next(file)
        for line in file.readlines():
            node = line.split()[0]
            if node not in vertices:
                node = graph.insert_vertex(node)
                vertices[node] = node
            else:
                node = vertices[node]
            adj_nodes = str(line.split()[1:])[3 : -3].replace(',', '').replace("'", '').split()
            for adj_node_1 in adj_nodes:
                if adj_node_1 != 'none':
                    if adj_node_1 not in vertices:
                        adj_node = graph.insert_vertex(adj_node_1)
                        vertices[adj_node_1] = adj_node
                    else:
                        adj_node = vertices[adj_node_1]
                    existing_edge = None
                    for edge in graph.incident_edges(node):
                        if edge.opposite(node) == adj_node:
                            existing_edge = edge
                            break
                    if existing_edge is None:
                        graph.insert_edge(node, adj_node)
    return graph

def dfs_test(graph: Graph, forest = {}, discovered = {}):
    def DFS(u: Graph.Vertex, edge: Graph.Edge):
        if u not in discovered:
            if edge is not None:
                forest[u.element()] = edge.endpoints()[0].element(), edge.endpoints()[1].element()
            else:
                forest[u.element()] = edge
            discovered[u] = edge
            for e in graph.incident_edges(u):
                v = e.opposite(u)
                DFS(v, e)
    for vertex in graph.vertices():
        if vertex not in forest:
            DFS(vertex, None)
    return forest

def bfs_test(graph: Graph, forest = {}) -> dict:
    def BFS(graph, s, discovered):
        level = [s]
        while len(level) > 0:
            next_level = []
            for u in level:
                for e in graph.incident_edges(u):
                    v = e.opposite(u)
                    if v not in discovered:
                        discovered[v] = e
                        next_level.append(v)
            level = next_level
    for u in graph.vertices():
        if u not in forest:
            forest[u] = None
            BFS(graph, u, forest)
    for key in list(forest.keys()):
        val = forest.pop(key)
        if val is not None:
            val = val.endpoints()[0].element(), val.endpoints()[1].element()
        key = key.element()
        forest[key] = val
    return forest

def main():
    graph = read_file('stanford_cs.txt')
    dfs = dfs_test(graph)
    bfs = bfs_test(graph)
    return dfs, bfs


if __name__ == '__main__':
    dfs, bfs = main()
    print(f'DFS: {dfs}' + '\n')
    print(f'BFS: {bfs}' + '\n')