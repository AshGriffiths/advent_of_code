from itertools import pairwise


def next_reading(reading_set):
    if len(set(reading_set)) == 1:
        return reading_set[0]
    return reading_set[-1] + next_reading([x[1] - x[0] for x in pairwise(reading_set)])


with open("input.txt", "r") as input_file:
    readings = [[int(val) for val in line.split(" ")] for line in input.readlines()]
    p1_results = []
    p2_results = []
    for reading_set in readings:
        p1_results.append(next_reading(reading_set))
        p2_results.append(next_reading(reading_set[::-1]))
    print(f"Part One : {sum(p1_results)}")
    print(f"Part Two : {sum(p2_results)}")
