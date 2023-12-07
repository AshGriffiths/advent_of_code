from functools import cmp_to_key

# Part 1
# RANKED_CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
# Part 2
RANKED_CARDS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def rank_hand(hand):
    count = {}
    for card in hand:
        if card in count:
            count[card] += 1
        else:
            count[card] = 1
    # Part 1
    # count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    # End Part 1
    # Part 2
    J_count = count.pop("J", 0)
    if not count:
        return 7
    count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    x, y = count[0]
    count[0] = (x, y + J_count)
    # End Part 2
    match count[0][1]:
        case 5:
            return 7
        case 4:
            return 6
        case 3:
            return 5 if count[1][1] == 2 else 4
        case 2:
            return 3 if count[1][1] == 2 else 2
        case other:
            return 1


def compare_hands(a, b):
    hand_a = a[0]
    hand_b = b[0]
    difference = rank_hand(hand_a) - rank_hand(hand_b)
    if difference != 0:
        return difference
    for i in range(0, len(hand_a)):
        diff = RANKED_CARDS.index(hand_a[i]) - RANKED_CARDS.index(hand_b[i])
        if diff != 0:
            return -diff


with open("input.txt", "r") as input:
    lines = input.readlines()
    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append((hand, bid))
    ranked_hands = sorted(hands, key=cmp_to_key(compare_hands))
    total = 0
    for i in range(0, len(ranked_hands)):
        total += int(ranked_hands[i][1]) * (i + 1)
    print(f"Total : {total}")
