with open("test.txt", "r") as input:
    grids = [row for row in [s.splitlines() for s in input.read().split("\n\n")]]
    for grid in grids:
        for line in grid:
            print(line)
        print()
