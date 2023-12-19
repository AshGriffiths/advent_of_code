from copy import deepcopy


def roll_rocks(grid: list[list[str]], direction: str = "N") -> list[list[str]]:
    height = len(grid)
    width = len(grid[0])
    range_y = range(height)
    range_x = range(width)
    match direction:
        case "S":
            range_y = range(height)[::-1]
        case "E":
            range_x = range(width)[::-1]
    for y in range_y:
        for x in range_x:
            if grid[y][x] == "O":
                match direction:
                    case "N":
                        next_pos = y
                        while next_pos > 0:
                            if grid[next_pos - 1][x] == ".":
                                next_pos -= 1
                            else:
                                break
                        grid[y][x] = "."
                        grid[next_pos][x] = "O"
                    case "W":
                        next_pos = x
                        while next_pos > 0:
                            if grid[y][next_pos - 1] == ".":
                                next_pos -= 1
                            else:
                                break
                        grid[y][x] = "."
                        grid[y][next_pos] = "O"
                    case "S":
                        next_pos = y
                        while next_pos < height - 1:
                            if grid[next_pos + 1][x] == ".":
                                next_pos += 1
                            else:
                                break
                        grid[y][x] = "."
                        grid[next_pos][x] = "O"
                    case "E":
                        next_pos = x
                        while next_pos < width - 1:
                            if grid[y][next_pos + 1] == ".":
                                next_pos += 1
                            else:
                                break
                        grid[y][x] = "."
                        grid[y][next_pos] = "O"

    return grid


def perform_one_cycle(grid: list[list[str]]) -> str:
    for direction in ["N", "W", "S", "E"]:
        roll_rocks(grid, direction)
    return "".join(["".join(row) for row in grid])


def calculate_load(grid: list[list[str]]) -> int:
    height = len(grid)
    load = 0
    for i, row in enumerate(grid):
        for col in row:
            if col == "O":
                load += height - i
    return load


with open("input.txt", "r") as input_file:
    platform = [[c for c in line.strip()] for line in input_file.readlines()]
    p1_grid = deepcopy(platform)
    p1_total = calculate_load(roll_rocks(p1_grid))
    print("\n".join(["".join(row) for row in p1_grid]))
    print()
    p2_grid = deepcopy(platform)
    total_cycles = 1_000_000_000
    seen_layouts = {"".join(["".join(row) for row in p2_grid]): 0}
    current_cycle = 0
    while current_cycle < total_cycles:
        current_cycle += 1
        key = perform_one_cycle(p2_grid)
        if key in seen_layouts:
            delta = current_cycle - seen_layouts[key]
            current_cycle += ((total_cycles - current_cycle) // delta) * delta
            break
        seen_layouts[key] = current_cycle
    while current_cycle < total_cycles:
        current_cycle += 1
        perform_one_cycle(p2_grid)
    p2_total = calculate_load(p2_grid)
    print("\n".join(["".join(row) for row in p2_grid]))
    print()
    print(f"Part One : {p1_total}")
    print(f"Part Two : {p2_total}")
