import re

EDGE_PATTERN = r"\(([A-Z]{,3}), ([A-Z]{,3})\)"

with open("input.txt", "r") as input:
    path, node_desc = input.read().split("\n\n")
    nodes = node_desc.split("\n")
    graph = {}
    for node in nodes:
        label, edge_desc = node.split(" = ")
        edges = re.findall(EDGE_PATTERN, edge_desc)[0]
        graph[label] = {"L": edges[0], "R": edges[1]}
    root = "AAA"
    terminal = "ZZZ"
    current = root
    steps = 0
    while current != terminal:
        for dir in path:
            steps += 1
            current = graph[current][dir]
            if current == terminal:
                break
    print(f"Total Steps : {steps}")
