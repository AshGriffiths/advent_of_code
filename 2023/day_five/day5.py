def process_values(values, maps):
    for map in maps:
        next_cell = []
        for dest, src, size in map:
            i = 0
            while i < len(values):
                start, length = values[i]
                if src <= start < src + size <= start + length:
                    next_cell.append((start - src + dest, src + size - start))
                    values[i] = (src + size, start + length - src - size)
                elif start <= src < start + length <= src + size:
                    next_cell.append((dest, start + length - src))
                    values[i] = (start, src - start)
                elif start <= src < src + size <= start + length:
                    next_cell.append((dest, size))
                    values[i] = (start, src - start)
                    values.append((src + size, start + length - src - size))
                if src <= start < start + length <= src + size:
                    next_cell.append((start - src + dest, length))
                    values[i] = values[-1]
                    del values[-1]
                else:
                    i += 1
        values += next_cell
    return values


with open("input.txt", "r") as input_file:
    seed_section, *map_sections = input.read().split("\n\n")
    seeds = [int(seed) for seed in seed_section.split()[1:]]
    maps = [
        [[int(val) for val in entry.split()] for entry in map_def.splitlines()[1:]]
        for map_def in map_sections
    ]

    p1_values = [(seed, 1) for seed in seeds]
    p2_values = list(zip(seeds[::2], seeds[1::2]))

    p1_soln = min(start for start, _ in process_values(p1_values, maps))
    p2_soln = min(start for start, _ in process_values(p2_values, maps))

    print(f"Part 1: {p1_soln}, Part 2: {p2_soln}")
