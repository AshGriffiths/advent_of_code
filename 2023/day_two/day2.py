import re

with open("input.txt", "r") as input_file:
    total = 0
    total_power = 0
    red_max = 12
    green_max = 13
    blue_max = 14
    games = input_file.readlines()
    game_number_pattern = r"^Game (\d+):"
    cube_pattern = r"(\d+) (red|green|blue)"
    for game in games:
        possible = True
        min_red = 1
        min_blue = 1
        min_green = 1
        game_number = int(re.findall(game_number_pattern, game)[0])
        print(f"Game: {game_number}")
        game_rounds = game.split(":")[1:]
        rounds = "".join(game_rounds).split(";")
        for current_round in rounds:
            cubes = current_round.strip().split(",")
            print(f"  Round: {rounds.index(current_round) + 1}\n    Cubes: {cubes}")
            for colour_sets in cubes:
                matches = re.findall(cube_pattern, colour_sets)
                count, colour = matches[0]
                count = int(count)
                match colour:
                    case "red":
                        if count > red_max:
                            possible = False
                        if count > min_red:
                            min_red = count
                    case "green":
                        if count > green_max:
                            possible = False
                        if count > min_green:
                            min_green = count
                    case "blue":
                        if count > blue_max:
                            possible = False
                        if count > min_blue:
                            min_blue = count
        if possible:
            print("  Possible")
            total += game_number
        else:
            print("  Not Possible")
        power = min_red * min_green * min_blue
        print(f"  Power of set: {power}")
        total_power += power
    print(f"Total of possible game numbers: {total}")
    print(f"Total Power of all games: {total_power}")
