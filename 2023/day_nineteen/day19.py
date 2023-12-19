from collections import deque


def do_workflow(workflow: list[tuple[str, str]], part: dict[str, int]) -> str:
    for rule in workflow:
        expr, dest = rule
        if expr == "ALWAYS":
            return dest
        attribute = expr[0]
        op = expr[1]
        value = int(expr[2:])
        match op:
            case "<":
                if part[attribute] < value:
                    return dest
            case ">":
                if part[attribute] > value:
                    return dest
            case _:
                raise ValueError("Unknown operator.")
    raise ValueError("Something went horribly wrong.")


def process_parts(
    parts: list[dict[str, int]], workflows: dict[str, list[tuple[str, str]]]
) -> int:
    total = 0
    for part in parts:
        next_workflow = "in"
        while next_workflow != "A" and next_workflow != "R":
            next_workflow = do_workflow(workflows[next_workflow], part)
        if next_workflow == "A":
            total += sum(part.values())
    return total


def recurse_workflow(
    workflows: dict[str, list[tuple[str, str]]],
    visited: set[str],
    queue: deque[str],
) -> str:
    label = queue.pop()
    if label == "A":
        pass
    elif label == "R":
        pass
    workflow = workflows[label]
    for rule in workflow:
        expr, dest = rule
        if expr == "ALWAYS":
            return dest
        attribute = expr[0]
        op = expr[1]
        value = int(expr[2:])
        match op:
            case "<":
                return dest
            case ">":
                return dest
            case _:
                raise ValueError("Unknown operator.")
    raise ValueError("Something went horribly wrong.")


def evaluate_workflow(workflows: dict[str, list[tuple[str, str]]]) -> None:
    valid_ranges = {
        "x": {"min": 1, "max": 4000},
        "m": {"min": 1, "max": 4000},
        "a": {"min": 1, "max": 4000},
        "s": {"min": 1, "max": 4000},
    }
    for label, workflow in workflows.items():
        pass


with open("input.txt", "r") as input_file:
    workflows_desc, parts_desc = input_file.read().split("\n\n")
    workflows: dict[str, list[tuple[str, str]]] = {}
    parts: list[dict[str, int]] = []
    for workflow in workflows_desc.split():
        label, instructions = workflow.split("{")
        instructions_desc = instructions[:-1]
        rules = []
        for ins in instructions_desc.split(","):
            if ":" in ins:
                rule, dest = ins.split(":")
                rules.append((rule, dest))
            else:
                rules.append(("ALWAYS", ins))
        workflows[label] = rules
    for part in parts_desc.splitlines():
        attributes = part[1:-1].split(",")
        part_dict = {}
        for attribute in attributes:
            category, value = attribute.split("=")
            part_dict[category] = int(value)
        parts.append(part_dict)
    p1_total = process_parts(parts, workflows)
    evaluate_workflow(workflows)
    print(f"Part One : {p1_total}")
