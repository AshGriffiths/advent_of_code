from collections.abc import Callable
from copy import deepcopy
from functools import reduce
from operator import mul, gt, lt
from typing import Any, NamedTuple


class ValidRange(NamedTuple):
    min_value: int
    max_value: int


class Rule(NamedTuple):
    category: str
    fn: Callable
    value: int
    dest: str

    def run(self, target: int) -> bool:
        return self.fn(target, self.value)

    def calculate_passing_ranges(
        self, attribute_ranges: dict[str, ValidRange]
    ) -> tuple[dict[str, ValidRange] | None, ...]:
        passing_ranges = deepcopy(attribute_ranges)
        failing_ranges = deepcopy(attribute_ranges)
        if self.fn is gt:
            passing_ranges[self.category] = ValidRange(
                self.value + 1, passing_ranges[self.category].max_value
            )
            failing_ranges[self.category] = ValidRange(
                failing_ranges[self.category].min_value, self.value
            )
            if passing_ranges[self.category].max_value <= self.value:
                return None, failing_ranges
            elif failing_ranges[self.category].min_value > self.value:
                return passing_ranges, None
        elif self.fn is lt:
            passing_ranges[self.category] = ValidRange(
                passing_ranges[self.category].min_value, self.value - 1
            )
            failing_ranges[self.category] = ValidRange(
                self.value, failing_ranges[self.category].max_value
            )
            if failing_ranges[self.category].min_value >= self.value:
                return passing_ranges, None
            elif passing_ranges[self.category].max_value < self.value:
                return None, failing_ranges
        return passing_ranges, failing_ranges


class WorkFlow(NamedTuple):
    rules: list[Rule]


def always(*args) -> bool:
    return True


def do_workflow(workflow: WorkFlow, part: dict[str, int]) -> str:
    for rule in workflow.rules:
        if rule.run(part[rule.category]):
            return rule.dest
    raise ValueError("Something went horribly wrong.")


def process_parts(parts: list[dict[str, int]], workflows: dict[str, WorkFlow]) -> int:
    total = 0
    for part in parts:
        next_workflow = "in"
        while next_workflow != "A" and next_workflow != "R":
            next_workflow = do_workflow(workflows[next_workflow], part)
        if next_workflow == "A":
            total += sum(part.values())
    return total


def process_ranges(workflows: dict[str, WorkFlow]) -> int:
    initial_attribute_ranges = {
        "x": ValidRange(1, 4000),
        "m": ValidRange(1, 4000),
        "a": ValidRange(1, 4000),
        "s": ValidRange(1, 4000),
    }
    stack = [(initial_attribute_ranges, "in", 0)]
    valid_ranges: list[dict[str, ValidRange]] = []
    while stack:
        attribute_ranges, label, current_rule = stack.pop()
        rule = workflows[label].rules[current_rule]
        passing_ranges, failing_ranges = (
            workflows[label]
            .rules[current_rule]
            .calculate_passing_ranges(attribute_ranges)
        )
        if passing_ranges:
            if rule.dest in "AR":
                if rule.dest == "A":
                    valid_ranges.append(passing_ranges)
            else:
                stack.append((passing_ranges, rule.dest, 0))

        if failing_ranges:
            current_rule += 1
            if current_rule < len(workflows[label].rules):
                next_workflow = label
            else:
                next_workflow = workflows[label].rules[-1].dest
                current_rule = 0
            if next_workflow in "AR":
                if next_workflow == "A":
                    valid_ranges.append(failing_ranges)
            else:
                stack.append((failing_ranges, next_workflow, current_rule))
    return sum(count_ranges(valid_range) for valid_range in valid_ranges)


def count_ranges(attribute_ranges: dict[str, ValidRange]) -> int:
    return reduce(
        mul,
        (
            attribute_ranges[category][1] - attribute_ranges[category][0] + 1
            for category in "xmas"
        ),
    )


with open("input.txt", "r") as input_file:
    workflows_desc, parts_desc = input_file.read().split("\n\n")
    workflows: dict[str, WorkFlow] = {}
    parts: list[dict[str, int]] = []
    for workflow in workflows_desc.split():
        label, instructions = workflow.split("{")
        instructions_desc = instructions[:-1]
        rules: list[Rule] = []
        for ins in instructions_desc.split(","):
            if ":" in ins:
                expr, dest = ins.split(":")
                attribute = expr[0]
                op = expr[1]
                value = int(expr[2:])
                rules.append(Rule(attribute, gt if op == ">" else lt, value, dest))
            else:
                rules.append(Rule("x", always, 1, ins))
        workflows[label] = WorkFlow(rules)
    for part in parts_desc.splitlines():
        attributes = part[1:-1].split(",")
        part_dict: dict[str, int] = {}
        for attribute in attributes:
            category, target = attribute.split("=")
            part_dict[category] = int(target)
        parts.append(part_dict)
    p1_total = process_parts(parts, workflows)
    p2_total = process_ranges(workflows)
    print(f"Part One : {p1_total}, error = {p1_total - 489392}")
    print(f"Part Two : {p2_total}, error = {p2_total - 134370637448305}")
