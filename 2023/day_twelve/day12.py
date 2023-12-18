from functools import cache


# Memoize this function, must only take immutables so it can be hashed
# thats why the groups has to be a tuple rather than a list
@cache
def count_possibilities(springs: str, groups: tuple[int, ...]) -> int:
    # Base case
    # i.e. is the tuple ()
    if not groups:
        # is everything left in springs either unknown or not a spring
        if all(spring in [".", "?"] for spring in springs):
            return 1
        return 0

    # (car groups)
    size_first_group = groups[0]
    # (cdr groups)
    remaining_groups = groups[1:]
    # Add the sizes of the remaining groups, plus 1 extra for each gap that must exist
    remaining_spring_spaces = sum(remaining_groups) + len(remaining_groups)
    count = 0
    for i in range(len(springs) - remaining_spring_spaces - size_first_group + 1):
        possible_springs = "." * i + "#" * size_first_group + "."
        if all(
            spring == possible_spring or spring == "?"
            for spring, possible_spring in zip(springs, possible_springs)
        ):
            count += count_possibilities(
                springs[len(possible_springs) :], remaining_groups
            )
    return count


with open("input.txt", "r") as input_file:
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
