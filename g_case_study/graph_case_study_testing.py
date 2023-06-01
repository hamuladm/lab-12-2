
from graph import LinkedDirectedGraph, LinkedVertex
from linkedstack import LinkedStack
from collections import deque

def read_file(path):
    graph = LinkedDirectedGraph()
    vertices = {}
    with open(path) as file:
        next(file)
        for line in file.readlines():
            node_data = line.split()
            node_label = node_data[0]
            if node_label not in vertices:
                node = LinkedVertex(node_label)
                vertices[node_label] = node
                graph.addVertex(node_label)
            else:
                node = vertices[node_label]
            adjacent_nodes = str(node_data[1:])[3:-3].replace(',', '').replace("'", '').split() # specical for reading correctly the line with two and more adjacent vertices
            for adj_node_label in adjacent_nodes:
                if adj_node_label != 'none':
                    if adj_node_label not in vertices:
                        adj_node = LinkedVertex(adj_node_label)
                        vertices[adj_node_label] = adj_node
                        graph.addVertex(adj_node_label)
                    else:
                        adj_node = vertices[adj_node_label]
                    if not graph.containsEdge(node_label, adj_node_label):
                        graph.addEdge(node_label, adj_node_label, None)
    return graph

def dfs_test(graph: LinkedDirectedGraph, vertex_position: LinkedVertex):
    graph.clearVertexMarks()
    stack = LinkedStack()
    path = []
    vertex_position.setMark()
    stack.push(vertex_position)
    while not stack.isEmpty():
        current_vertex = stack.pop()
        path.append(current_vertex.getLabel())
        for vertex in graph.neighboringVertices(current_vertex.getLabel()):
            if not vertex.isMarked():
                vertex.setMark()
                stack.push(vertex)
    return path
    
def bfs_test(graph: LinkedDirectedGraph, vertex_position: LinkedVertex):
    graph.clearVertexMarks()
    path = []
    queue = deque([vertex_position])
    vertex_position.setMark()
    while queue:
        current_vertex = queue.popleft()
        path.append(current_vertex.getLabel())
        for vertex in graph.neighboringVertices(current_vertex.getLabel()):
            if not vertex.isMarked():
                vertex.setMark()
                queue.append(vertex)
    return path

def topological_sort_test(graph: LinkedDirectedGraph, start_label = None):
    graph.clearVertexMarks()
    stack = LinkedStack()
    def dfs_1(graph, vertex_position, stack):
        vertex_position.setMark()
        for vertex in graph.neighboringVertices(vertex_position.getLabel()):
            if not vertex.isMarked():
                dfs_1(graph, vertex, stack)
        stack.push(vertex_position)
    if start_label is not None:
        start_vertex = graph.getVertex(start_label)
        dfs_1(graph, start_vertex, stack)
    else:
        for vertex in graph.vertices():
            if not vertex.isMarked():
                dfs_1(graph, vertex, stack)
    return stack

def main():
    graph = read_file('stanford_cs.txt')
    vertex_position = graph.getVertex('CS161')
    dfs = dfs_test(graph, vertex_position)
    bfs = bfs_test(graph, vertex_position)
    topo_sort = topological_sort_test(graph)
    return dfs, bfs, topo_sort


if __name__ == '__main__':
    dfs, bfs, topo_sort = main()
    print(f'DFS Result: {dfs}\nBFS Result: {bfs}\nTopological sort: {topo_sort}')
