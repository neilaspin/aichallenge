# recursive
def dfs_recursive(graph, vertex, path=[]):
    path += [vertex]

    for neighbor in graph[vertex]:
        if neighbor not in path:
            path = dfs_recursive(graph, neighbor, path)

    return path


adjacency_matrix = {1: [2, 3], 2: [4, 5],
                    3: [5], 4: [6], 5: [6],
                    6: [7], 7: []}

print(dfs_recursive(adjacency_matrix, 1))

# non-recursive

def dfs_iterative(graph, start):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        path.append(vertex)
        for neighbour in graph[vertex]:
            stack.append(neighbour)
    return path

# adjacency_matrix = {1: [2, 3], 2: [4, 5],
#                     3: [5], 4: [6], 5: [6],
#                     6: [7], 7: []}
print(dfs_iterative(adjacency_matrix, 1))