import re

with open("input.txt", "r") as input:
    total = 0
    cards = input.readlines()
    card_count = {}
    for card in cards:
        card_split = card.split(": ", maxsplit=1)
        card_num = card_split[0]
        card_pattern = r"^Card[ ]+(\d+)"
        card_num = re.findall(card_pattern, card_num)[0]
        numbers = card_split[1]
        numbers = numbers.strip()
        split_numbers = numbers.split(" | ", maxsplit=1)
        winning_numbers = list(
            filter(lambda num: num != "", split_numbers[0].split(" "))
        )
        playing_numbers = list(
            filter(lambda num: num != "", split_numbers[1].split(" "))
        )
        print(
            f"Card: {card_num}, Winning: {winning_numbers}, Playing : {playing_numbers}"
        )
        win_count = 0
        for num in winning_numbers:
            if num in playing_numbers:
                win_count += 1
        if win_count:
            card_total = 2 ** (win_count - 1)
        else:
            card_total = 0
        total += card_total
        card_count[int(card_num)] = win_count
    final_card_count = {}
    for card, wins in card_count.items():
        if card in final_card_count:
            c, w = final_card_count[card]
            final_card_count[card] = (c + 1, w)
        else:
            final_card_count[card] = (1, wins)
        for i in range(card + 1, card + wins + 1):
            if i in final_card_count:
                c, w = final_card_count[i]
                final_card_count[i] = (c + final_card_count[card][0], w)
            else:
                final_card_count[i] = (final_card_count[card][0], card_count[i])
        print(
            f"Card {card}, Count {final_card_count[card][0]}, Wins {final_card_count[card][1]}"
        )
    print(f"Total : {total}")
    total_cards = 0
    for value in final_card_count.values():
        total_cards += value[0]
    print(f"Cards : {total_cards}")
