class Directions:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


with open("input.txt", "r") as input:
    instructions = [
        (x, int(y), z)
        for x, y, z in [line.split() for line in input.read().strip().split("\n")]
    ]
    p1_x, p1_y, p1_perimeter, p1_area = 0, 0, 0, 0
    p2_x, p2_y, p2_perimeter, p2_area = 0, 0, 0, 0
    dir_decode = str.maketrans("0123", "RDLU")
    for instruction in instructions:
        p1_direction, p1_count, colour = instruction
        p1_dir_tup = (0, 0)
        p2_count = int(colour[2:7], 16)
        p2_direction = colour[-2].translate(dir_decode)
        p2_dir_tup = (0, 0)
        match p1_direction:
            case "U":
                p1_dir_tup = Directions.UP
            case "D":
                p1_dir_tup = Directions.DOWN
            case "L":
                p1_dir_tup = Directions.LEFT
            case "R":
                p1_dir_tup = Directions.RIGHT
        match p2_direction:
            case "U":
                p2_dir_tup = Directions.UP
            case "D":
                p2_dir_tup = Directions.DOWN
            case "L":
                p2_dir_tup = Directions.LEFT
            case "R":
                p2_dir_tup = Directions.RIGHT
        p1_dx, p1_dy = p1_dir_tup[0] * p1_count, p1_dir_tup[1] * p1_count
        p1_x += p1_dx
        p1_y += p1_dy
        p1_perimeter += p1_count
        p1_area += p1_x * p1_dy
        p2_dx, p2_dy = p2_dir_tup[0] * p2_count, p2_dir_tup[1] * p2_count
        p2_x += p2_dx
        p2_y += p2_dy
        p2_perimeter += p2_count
        p2_area += p2_x * p2_dy
    print(f"Part One : {p1_area + p1_perimeter // 2 + 1}")
    print(f"Part Two : {p2_area + p2_perimeter // 2 + 1}")
