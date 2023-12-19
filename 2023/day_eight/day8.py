import re

from itertools import cycle
from math import gcd

EDGE_PATTERN = r"\(([A-Z]{,3}), ([A-Z]{,3})\)"


def check_loop(path, graph, start):
    step_one = start
    step_two = start
    period = len(path)
    dir_one = cycle(path)
    dir_two = cycle(path)
    for i, direction in enumerate(dir_one, start=1):
        step_one = graph[step_one][direction]
        step_two = graph[step_two][next(dir_two)]
        step_two = graph[step_two][next(dir_two)]
        if step_one == step_two and i % period == (i * 2) % period:
            return i


def lcm(periods):
    if len(periods) == 2:
        return periods[0] * periods[1] // gcd(periods[0], periods[1])
    return lcm([periods[0], lcm(periods[1:])])


with open("input.txt", "r") as input_file:
    path, node_desc = input_file.read().split("\n\n")
    nodes = node_desc.split("\n")
    graph = {}
    for node in nodes:
        label, edge_desc = node.split(" = ")
        edges = re.findall(EDGE_PATTERN, edge_desc)[0]
        graph[label] = {"L": edges[0], "R": edges[1]}
    p1_root = "AAA"
    p1_terminal = "ZZZ"
    p1_current = p1_root
    p1_steps = 0
    while p1_current != p1_terminal:
        for direction in path:
            p1_steps += 1
            p1_current = graph[p1_current][direction]
            if p1_current == p1_terminal:
                break
    p2_roots = frozenset(
        {
            root
            for root in filter(
                lambda node: node[-1] == "A", (node for node in graph.keys())
            )
        }
    )
    periods = [check_loop(path, graph, start) for start in p2_roots]

    print(f"Part One : {p1_steps}")
    print(f"Part Two : {lcm(periods)}")
