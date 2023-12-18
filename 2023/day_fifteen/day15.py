def calculate_hash(instruction: str) -> int:
    current_value = 0
    for chr in instruction:
        current_value += ord(chr)
        current_value *= 17
        current_value %= 256
    return current_value


def calculate_focusing_power(hashmap: dict[int, list[dict[str, int]]]) -> int:
    total = 0
    for box_no, box in hashmap.items():
        for slot, lens in enumerate(box):
            total += (box_no + 1) * (slot + 1) * lens[list(lens.keys())[0]]
    return total


with open("input.txt", "r") as input_file:
    sequence = input.read()
    steps = sequence.split(",")
    p1_total = sum(map(calculate_hash, steps))
    print(f"Part One : {p1_total}")
    hashmap: dict[int, list[dict[str, int]]] = {key: [] for key in range(256)}
    for step in steps:
        if step[-1].isdigit():
            focal_length = int(step[-1])
            label = step[:-2]
            hash_value = calculate_hash(label)
            box = hashmap[hash_value]
            if len(box) != 0:
                labels = list({k: None for lens in box for k in lens.keys()}.keys())
                if label in labels:
                    idx = labels.index(label)
                    box[idx][label] = focal_length
                else:
                    box.append({label: focal_length})
            else:
                box.append({label: focal_length})
        else:
            label = step[:-1]
            hash_value = calculate_hash(label)
            box = hashmap[hash_value]
            labels = list({k: None for lens in box for k in lens.keys()}.keys())
            if label in labels:
                del box[labels.index(label)]
    p2_total = calculate_focusing_power(hashmap)
    print(f"Part Two : {p2_total}")
