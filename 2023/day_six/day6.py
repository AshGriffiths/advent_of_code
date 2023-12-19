from functools import reduce

with open("input.txt", "r") as input_file:
    time, dist = input_file.read().split("\n")
    times = [int(t) for t in filter(lambda x: x, time.split(":")[1].split())]
    dists = [int(d) for d in filter(lambda x: x, dist.split(":")[1].split())]
    p1 = zip(times, dists)
    p2 = [(int("".join(str(t) for t in times)), int("".join(str(d) for d in dists)))]
    # just switch records def for p1
    # records = p1
    # just brute force it, the numbers arent that big
    records = p2
    results = []
    for race in records:
        t, d = race
        wins = 0
        for i in range(0, t + 1):
            sp = i
            rem = t - i
            res = sp * rem
            if res > d:
                wins += 1
        results.append(wins)
    print(f"Result: {reduce(lambda a, r: a * r, results, 1)}")
