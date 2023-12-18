from collections import deque

VALID_NORTH = ["|", "F", "7"]
VALID_EAST = ["-", "J", "7"]
VALID_SOUTH = ["|", "L", "J"]
VALID_WEST = ["-", "L", "F"]

REPLACE_PIPES = {
    "|": "│",
    "-": "─",
    "F": "┌",
    "L": "└",
    "7": "┐",
    "J": "┘",
    ".": "•",
    "S": "┘",
}


def get_valid_adjacent_locations(location, height, width):
    locations = []
    x, y = location
    if x == 0 and y == 0:
        locations.append((x, y + 1))
        locations.append((x + 1, y))
    elif x == (width - 1) and y == (height - 1):
        locations.append((x, y - 1))
        locations.append((x - 1, y))
    elif x == 0 and y == (height - 1):
        locations.append((x, y - 1))
        locations.append((x + 1, y))
    elif x == (width - 1) and y == 0:
        locations.append((x, y + 1))
        locations.append((x - 1, y))
    elif x == 0:
        locations.append((x, y - 1))
        locations.append((x + 1, y))
        locations.append((x, y + 1))
    elif y == 0:
        locations.append((x + 1, y))
        locations.append((x, y + 1))
        locations.append((x - 1, y))
    elif x == (width - 1):
        locations.append((x, y - 1))
        locations.append((x, y + 1))
        locations.append((x - 1, y))
    elif y == (height - 1):
        locations.append((x, y - 1))
        locations.append((x + 1, y))
        locations.append((x - 1, y))
    else:
        locations.append((x, y - 1))
        locations.append((x + 1, y))
        locations.append((x, y + 1))
        locations.append((x - 1, y))
    return locations


def count_loop(sketch, start, next_locations):
    dir_one, dir_two = next_locations
    loop = deque([dir_one, start, dir_two])
    count = 1
    prev_locations = [start, start]
    while dir_one != dir_two:
        count += 1
        dir_one_x, dir_one_y = dir_one
        dir_two_x, dir_two_y = dir_two
        new_dir_one = get_next_location(
            prev_locations[0], dir_one, sketch[dir_one_y][dir_one_x]
        )
        new_dir_two = get_next_location(
            prev_locations[1], dir_two, sketch[dir_two_y][dir_two_x]
        )
        prev_locations = [dir_one, dir_two]
        dir_one = new_dir_one
        dir_two = new_dir_two
        loop.appendleft(dir_one)
        loop.append(dir_two)
    loop = list(loop)
    loop_left = loop[count:]
    loop_right = loop[1:count]
    loop = loop_left + loop_right
    return (count, loop)


def get_next_location(prev, curr, pipe):
    prev_x, prev_y = prev
    curr_x, curr_y = curr
    next_y = curr_y
    next_x = curr_x
    x_diff = prev_x - curr_x
    y_diff = prev_y - curr_y
    match pipe:
        case "|":
            if y_diff == -1:
                next_y = curr_y + 1
            else:
                next_y = curr_y - 1
        case "-":
            if x_diff == -1:
                next_x = curr_x + 1
            else:
                next_x = curr_x - 1
        case "L":
            if y_diff == -1:
                next_x = curr_x + 1
            else:
                next_y = curr_y - 1
        case "J":
            if y_diff == -1:
                next_x = curr_x - 1
            else:
                next_y = curr_y - 1
        case "7":
            if y_diff == 1:
                next_x = curr_x - 1
            else:
                next_y = curr_y + 1
        case "F":
            if y_diff == 1:
                next_x = curr_x + 1
            else:
                next_y = curr_y + 1
    return (next_x, next_y)


def get_inside_count(sketch, loop):
    inside_points = []
    count = 0
    for y, row in enumerate(sketch):
        prev_corner = None
        crossings = 0
        for x, col in enumerate(row):
            if (x, y) in loop:
                match col:
                    case "|":
                        crossings += 1
                    case "7":
                        if prev_corner == "L":
                            crossings += 1
                    case "J":
                        if prev_corner == "F":
                            crossings += 1
                    case "S":
                        crossings += 1
                if col != "-":
                    prev_corner = col
            else:
                if crossings % 2 == 1:
                    count += 1
                    inside_points.append((x, y))
    return (count, inside_points)


with open("input.txt", "r") as input_file:
    sketch = [[pos for pos in line.strip()] for line in input.readlines()]
    height = len(sketch)
    width = len(sketch[0])
    start = None
    for y in range(0, height):
        for x in range(0, width):
            if sketch[y][x] == "S":
                start = (x, y)
                break
        if start:
            break
    adjacent_locations = get_valid_adjacent_locations(start, height, width)
    adjacent_pipes = [sketch[tile[1]][tile[0]] for tile in adjacent_locations]
    next_locations = []
    for loc, pipe in zip(adjacent_locations, adjacent_pipes):
        next_x, next_y = loc
        x_diff = next_x - x
        y_diff = next_y - y
        valid = False
        if x_diff == 0:
            if y_diff == -1 and pipe in VALID_NORTH:
                valid = True
            elif y_diff == 1 and pipe in VALID_SOUTH:
                valid = True
        elif y_diff == 0:
            if x_diff == 1 and pipe in VALID_EAST:
                valid = True
            elif x_diff == -1 and pipe in VALID_WEST:
                valid = True
        if valid:
            next_locations.append((next_x, next_y))
    count, loop = count_loop(sketch, start, next_locations)
    inside_count, inside_points = get_inside_count(sketch, loop)
    print(f"Part One : {count}")
    print(f"Part Two : {inside_count}")
    for y, row in enumerate(sketch):
        print(str(y) + "\t", end="")
        for x, col in enumerate(row):
            col = REPLACE_PIPES[col]
            if (x, y) in loop:
                print("\033[42m\033[31m" + col + "\033[40m\033[37m", end="")
            elif (x, y) in inside_points:
                print("\033[41m\033[32m" + col + "\033[40m\033[37m", end="")
            else:
                print(col, end="")
        print()
