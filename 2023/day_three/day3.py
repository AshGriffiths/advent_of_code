from collections import deque


def get_symbol_locations(
    engine: list[list[str]],
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    locations: list[tuple[int, int]] = []
    gear_locations: list[tuple[int, int]] = []
    for i, row in enumerate(engine):
        for j, col in enumerate(row):
            if not col.isdigit() and col != ".":
                locations.append((j, i))
                if col == "*":
                    gear_locations.append((j, i))
    return locations, gear_locations


def get_gear_locations(engine: list[list[str]]) -> list[tuple[int, int]]:
    locations = []
    for i, row in enumerate(engine):
        for j, col in enumerate(row):
            if col == "*":
                locations.append((j, i))
    return locations


def get_all_adjacent_numbers(
    engine: list[list[str]], locations: list[tuple[int, int]], height: int, width: int
) -> list[list[int]]:
    numbers: list[list[int]] = []
    for location in locations:
        numbers.append(get_adjacent_numbers(engine, location, height, width))
    return numbers


def get_adjacent_numbers(
    engine: list[list[str]], location: tuple[int, int], height: int, width: int
) -> list[int]:
    numbers: list[int] = []
    adjacent_locations = get_valid_adjacent_locations(location, height, width)
    checked: list[tuple[int, int]] = []
    for x, y in adjacent_locations:
        if (x, y) in checked:
            continue
        checked.append((x, y))
        if engine[y][x].isdigit():
            number: deque[str] = deque(engine[y][x])
            for i in range(x - 1, -1, -1):
                if engine[y][i].isdigit():
                    number.appendleft(engine[y][i])
                else:
                    break
            for i in range(x + 1, width):
                if engine[y][i].isdigit():
                    number.append(engine[y][i])
                    checked.append((i, y))
                else:
                    break
            numbers.append(int("".join(number)))
    return numbers


def get_valid_adjacent_locations(
    location: tuple[int, int], height: int, width: int
) -> list[tuple[int, int]]:
    locations: list[tuple[int, int]] = []
    x, y = location
    for i in range(0, width):
        for j in range(0, height):
            x_diff = abs(i - x)
            y_diff = abs(j - y)
            if (x_diff == 1 or x_diff == 0) and (y_diff == 1 or y_diff == 0):
                locations.append((i, j))
    locations.remove(location)
    return locations


with open("input.txt", "r") as input_file:
    engine_rows = input_file.read().splitlines()
    engine: list[list[str]] = []
    for row in engine_rows:
        engine.append([*row])
    height = len(engine)
    width = len(engine[0])
    symbol_locs, gear_locs = get_symbol_locations(engine)
    list_of_numbers = get_all_adjacent_numbers(engine, symbol_locs, height, width)
    list_of_gear_numbers = get_all_adjacent_numbers(engine, gear_locs, height, width)
    total_gear_ratio = 0
    for gear_numbers in list_of_gear_numbers:
        if len(gear_numbers) == 2:
            total_gear_ratio += gear_numbers[0] * gear_numbers[1]
    total = 0
    for numbers in list_of_numbers:
        total += sum(numbers)
    print(f"Part 1: {total} Part 2: {total_gear_ratio}")
