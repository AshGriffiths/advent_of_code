from functools import cache


@cache
def count_possibilities(springs: str, groups: tuple[int, ...]) -> int:
    if not groups:
        if all(spring in [".", "?"] for spring in springs):
            return 1
        return 0

    car_int = groups[0]
    cdr_ints = groups[1:]
    after = sum(cdr_ints) + len(cdr_ints)
    count = 0
    for before in range(len(springs) - after - car_int + 1):
        possible_springs = "." * before + "#" * car_int + "."
        if all(
            spring == possible_spring or spring == "?"
            for spring, possible_spring in zip(springs, possible_springs)
        ):
            count += count_possibilities(springs[len(possible_springs) :], cdr_ints)
    return count


with open("input.txt", "r") as input:
    rows = [
        [splits[0], splits[1]]
        for splits in [line.split() for line in input.readlines()]
    ]
    total_p1 = 0
    total_p2 = 0
    for row in rows:
        pattern, groups = row
        int_groups = tuple(map(int, groups.split(",")))
        total_p1 += count_possibilities(pattern, int_groups)
        total_p2 += count_possibilities("?".join((pattern,) * 5), int_groups * 5)
    print(f"Part One : {total_p1}")
    print(f"Part Two : {total_p2}")
