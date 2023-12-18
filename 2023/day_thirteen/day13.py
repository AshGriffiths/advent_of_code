def check_symmetry(grid: list[str], allowed_smudges: int = 0) -> int:
    no_of_rows = len(grid)
    no_of_cols = len(grid[0])
    for col in range(no_of_cols - 1):
        error_count = 0
        for split_col in range(no_of_cols):
            left = col - split_col
            right = col + 1 + split_col
            if 0 <= left < right < no_of_cols:
                for row in range(no_of_rows):
                    if grid[row][left] != grid[row][right]:
                        error_count += 1
        if error_count == allowed_smudges:
            return col + 1
    return 0


with open("input.txt", "r") as input_file:
    grids = [row for row in [s.splitlines() for s in input.read().split("\n\n")]]
    transposed_grids = [list("".join(x) for x in zip(*grid)) for grid in grids]
    p1_total = 0
    p2_total = 0
    for grid in grids:
        p1_total += check_symmetry(grid)
        p2_total += check_symmetry(grid, 1)
    for t_grid in transposed_grids:
        p1_total += 100 * check_symmetry(t_grid)
        p2_total += 100 * check_symmetry(t_grid, 1)
    print(f"Part One : {p1_total}")
    print(f"Part Two : {p2_total}")
