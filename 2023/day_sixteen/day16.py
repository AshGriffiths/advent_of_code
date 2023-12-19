from collections import deque


class Directions:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def bfs(
    graph: list[list[str]],
    value: tuple[tuple[int, int], tuple[int, int]],
    energized: list[list[int]],
    height: int,
    width: int,
) -> None:
    visited = {value}
    queue = deque([value])
    while queue:
        current = queue.popleft()
        pos, direction = current
        x, y = pos
        if not (x < 0 or y < 0 or x >= width or y >= height):
            energized[y][x] = energized[y][x] + 1
        next_pos = (x + direction[0], y + direction[1])
        next_x, next_y = next_pos
        if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
            continue
        cell = graph[next_y][next_x]
        updates = []
        match direction:
            case Directions.UP:
                match cell:
                    case "." | "|":
                        updates.append((next_pos, direction))
                    case "/":
                        updates.append((next_pos, Directions.RIGHT))
                    case "\\":
                        updates.append((next_pos, Directions.LEFT))
                    case "-":
                        updates.append((next_pos, Directions.LEFT))
                        updates.append((next_pos, Directions.RIGHT))
            case Directions.DOWN:
                match cell:
                    case "." | "|":
                        updates.append((next_pos, direction))
                    case "/":
                        updates.append((next_pos, Directions.LEFT))
                    case "\\":
                        updates.append((next_pos, Directions.RIGHT))
                    case "-":
                        updates.append((next_pos, Directions.LEFT))
                        updates.append((next_pos, Directions.RIGHT))
            case Directions.LEFT:
                match cell:
                    case "." | "-":
                        updates.append((next_pos, direction))
                    case "/":
                        updates.append((next_pos, Directions.DOWN))
                    case "\\":
                        updates.append((next_pos, Directions.UP))
                    case "|":
                        updates.append((next_pos, Directions.UP))
                        updates.append((next_pos, Directions.DOWN))
            case Directions.RIGHT:
                match cell:
                    case "." | "-":
                        updates.append((next_pos, direction))
                    case "/":
                        updates.append((next_pos, Directions.UP))
                    case "\\":
                        updates.append((next_pos, Directions.DOWN))
                    case "|":
                        updates.append((next_pos, Directions.UP))
                        updates.append((next_pos, Directions.DOWN))
        for value in updates:
            if value not in visited:
                visited.add(value)
                queue.append(value)


def calculate_path(
    graph: list[list[str]],
    start: tuple[tuple[int, int], tuple[int, int]],
    height: int,
    width: int,
) -> int:
    energized = [[0] * width for _ in range(height)]
    bfs(graph, start, energized, height, width)
    total = 0
    for row in energized:
        total += sum(min(value, 1) for value in row)
    return total


with open("input.txt", "r") as input_file:
    contraption = [[c for c in line.strip()] for line in input_file.readlines()]
    # Input is actually square
    length = len(contraption)
    p1_start = (-1, 0), (Directions.RIGHT)
    p1_total = calculate_path(contraption, p1_start, length, length)
    p2_total = 0
    for i in range(length):
        possible_starts = [
            ((i, length), Directions.UP),
            ((i, -1), Directions.DOWN),
            ((length, i), Directions.LEFT),
            ((-1, i), Directions.RIGHT),
        ]
        for start in possible_starts:
            p2_total = max(
                p2_total,
                calculate_path(contraption, start, length, length),
            )
    print(f"Part One : {p1_total}")
    print(f"Part Two : {p2_total}")
