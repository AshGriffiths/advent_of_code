from heapq import heappop, heappush


class Directions:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    movements = [UP, LEFT, DOWN, RIGHT]

    @staticmethod
    def invert(dir: tuple[int, int]) -> tuple[int, int]:
        if dir == Directions.UP:
            return Directions.DOWN
        if dir == Directions.DOWN:
            return Directions.UP
        if dir == Directions.LEFT:
            return Directions.RIGHT
        if dir == Directions.RIGHT:
            return Directions.LEFT
        raise ValueError("Not a valid direction.")


def djikstra(
    graph: list[list[int]],
    value: tuple[int, tuple[int, int], tuple[int, int] | None],
    min_travel: int = 1,
    max_travel: int = 3,
) -> int:
    height = len(graph)
    width = len(graph[0])
    queue = [value]
    visited = set()
    weights: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    while queue:
        weight, pos, forbidden = heappop(queue)
        x, y = pos
        if x == width - 1 and y == height - 1:
            return weight
        if (pos, forbidden) in visited:
            continue
        visited.add((pos, forbidden))
        for dir in Directions.movements:
            weight_change = 0
            if forbidden and (dir == forbidden or Directions.invert(dir) == forbidden):
                continue
            for dist in range(1, max_travel + 1):
                next_x = x + (dir[0] * dist)
                next_y = y + (dir[1] * dist)
                if next_x in range(width) and next_y in range(height):
                    weight_change += graph[next_y][next_x]
                    if dist < min_travel:
                        continue
                    new_weight = weight + weight_change
                    key = ((next_x, next_y), dir)
                    if key in weights:
                        if new_weight > weights[key]:
                            continue
                    weights[key] = new_weight
                    heappush(queue, (new_weight,) + key)
    raise ValueError("No path found. Make sure there is no negative cycle.")


with open("input.txt", "r") as input:
    maze = [[int(x) for x in line.strip()] for line in input.readlines()]
    p1_total = djikstra(maze, (0, (0, 0), None))
    print(f"Part One : {p1_total}")
    p2_total = djikstra(maze, (0, (0, 0), None), 4, 10)
    print(f"Part Two : {p2_total}")
