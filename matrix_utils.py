from Router import Router

def create_adjacency_matrix(nodes: list["Router"]):
    # Map each router to an index in the matrix
    index = {node: i for i, node in enumerate(nodes)}

    n = len(nodes)

    # Initialize matrix with infinity (no connection)
    matrix = [[float("inf") for _ in range(n)] for _ in range(n)]

    # Distance from a node to itself is 0
    for i in range(n):
        matrix[i][i] = 0

    # Fill in edges
    for node in nodes:
        i = index[node]

        for neighbor, cost in node.neighbors.items():
            j = index[neighbor]
            matrix[i][j] = cost

    return matrix

def print_adjacency_matrix(nodes: list["Router"], matrix):
    cell_width = 2

    def print_separator():
        print("+" + "+".join(["-" * (cell_width + 2)] * (len(nodes) + 1)) + "+")

    def print_row(values):
        print("|", end="")
        for value in values:
            print(f" {value:>{cell_width}} |", end="")
        print()

    # Header
    print_separator()
    print_row([""] + [node.id for node in nodes])
    print_separator()

    # Matrix rows
    for i, row in enumerate(matrix):
        formatted_row = [
            "∞" if value == float("inf") else value
            for value in row
        ]
        print_row([nodes[i].id] + formatted_row)
        print_separator()