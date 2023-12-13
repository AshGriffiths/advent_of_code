with open("input.txt", "r") as input:
    observations = input.readlines()
    empty_rows = []
    empty_cols = []
    for i, row in enumerate(observations):
        if "#" not in row:
            empty_rows.append(i)
            continue

    flipped_observations = list(zip(*observations))
    for j, col in enumerate(flipped_observations):
        if "#" not in col:
            empty_cols.append(j)

    dist_y_p1 = -1
    dist_y_p2 = -1
    adjusted_galaxies_p1 = []
    adjusted_galaxies_p2 = []
    for k, rown in enumerate(observations):
        dist_y_p1 = dist_y_p1 + 2 if k in empty_rows else dist_y_p1 + 1
        dist_y_p2 = dist_y_p2 + 1_000_000 if k in empty_rows else dist_y_p2 + 1
        dist_x_p1 = -1
        dist_x_p2 = -1
        for l, coln in enumerate(rown):
            dist_x_p1 = dist_x_p1 + 2 if l in empty_cols else dist_x_p1 + 1
            dist_x_p2 = dist_x_p2 + 1_000_000 if l in empty_cols else dist_x_p2 + 1
            if coln == "#":
                adjusted_galaxies_p1.append((dist_x_p1, dist_y_p1))
                adjusted_galaxies_p2.append((dist_x_p2, dist_y_p2))

    total_distance_p1 = 0
    for m, start_galaxy in enumerate(adjusted_galaxies_p1):
        for dest_galaxy in adjusted_galaxies_p1[m + 1 :]:
            total_distance_p1 += abs(start_galaxy[0] - dest_galaxy[0]) + abs(
                start_galaxy[1] - dest_galaxy[1]
            )
    total_distance_p2 = 0
    for n, start_galaxy in enumerate(adjusted_galaxies_p2):
        for dest_galaxy in adjusted_galaxies_p2[n + 1 :]:
            total_distance_p2 += abs(start_galaxy[0] - dest_galaxy[0]) + abs(
                start_galaxy[1] - dest_galaxy[1]
            )

    print(f"Part One : {total_distance_p1}")
    print(f"Part Two : {total_distance_p2}")
