from collections import deque
from copy import deepcopy
from typing import NamedTuple, TypeAlias

# To, From, Value
QUEUE: deque[tuple[str, str, bool]] = deque()


class Broadcaster(NamedTuple):
    dest: list[str]
    state: dict[str, bool] = {"button": False}
    label: str = "broadcaster"

    def recv(self, src: str, signal: bool):
        # Always receives low
        for component in self.dest:
            QUEUE.append((component, self.label, self.state[src]))


class Conjunction(NamedTuple):
    label: str
    state: dict[str, bool]
    dest: list[str]

    def recv(self, src: str, x: bool):
        # Set state of input from src
        self.state[src] = x
        output = True
        # If all the states are high send low, else high
        if all(self.state.values()):
            output = False
        for component in self.dest:
            QUEUE.append((component, self.label, output))


class FlipFlop(NamedTuple):
    label: str
    state: dict[str, bool]
    dest: list[str]

    def recv(self, src: str, x: bool):
        # if high, do nothing
        if x:
            pass
        # If low, flip the state of the src
        else:
            self.state[""] = not self.state[""]
            output = False
            # If state is now high, send high, else low
            if self.state[""]:
                output = True
            for component in self.dest:
                QUEUE.append((component, self.label, output))


class Output(NamedTuple):
    label: str
    state: dict[str, bool]

    def recv(self, src: str, x: bool):
        self.state[src] = x


Component: TypeAlias = Broadcaster | FlipFlop | Conjunction | Output


def process_button_press(graph: dict[str, Component]) -> tuple[int, int]:
    high = 0
    low = 0
    while QUEUE:
        next_cmpnt, prev_cmpnt, signal = QUEUE.popleft()
        if signal:
            high += 1
        else:
            low += 1
        graph[next_cmpnt].recv(prev_cmpnt, signal)
    return high, low


def process_all_button_presses(graph: dict[str, Component], times: int = 1000) -> int:
    high = 0
    low = 0
    for i in range(times):
        QUEUE.append(("broadcaster", "button", False))
        result = process_button_press(graph)
        high += result[0]
        low += result[1]
    return high * low


def find_all_cycle_lengths(graph: dict[str, Component]) -> dict[str, int]:
    lengths: dict[str, int] = {}
    output_node = graph["rx"]
    terminal_nodes = [graph[node] for node in output_node.state.keys()]
    terminal_node_inputs = {
        terminal_node.label: [graph[node] for node in terminal_node.state.keys()]
        for terminal_node in terminal_nodes
    }
    for input_nodes in terminal_node_inputs.values():
        for node in input_nodes:
            lengths[node.label] = int(1e100)
    return lengths


with open("input.txt", "r") as input_file:
    components: dict[str, Component] = {}
    component_defn = input_file.readlines()
    cmpnt_inp_map: dict[str, list[str]] = {}
    for line in component_defn:
        cmpnt_desc, dest_list = line.split(" -> ")
        dests = dest_list.strip().split(", ")
        cmpnt: Component
        if cmpnt_desc == "broadcaster":
            cmpnt_type = "b"
            cmpnt_label = cmpnt_desc
        else:
            cmpnt_type = cmpnt_desc[0]
            cmpnt_label = cmpnt_desc[1:]
        for dest in dests:
            if dest in cmpnt_inp_map.keys():
                cmpnt_inp_map[dest].append(cmpnt_label)
            else:
                cmpnt_inp_map[dest] = [cmpnt_label]
        if cmpnt_type == "%":
            cmpnt = FlipFlop(cmpnt_label, {"": False}, dests)
        elif cmpnt_type == "&":
            cmpnt = Conjunction(cmpnt_label, {}, dests)
        else:
            cmpnt = Broadcaster(dests)
        components[cmpnt_label] = cmpnt
    for cmpnt_label in cmpnt_inp_map.keys():
        if cmpnt_label not in components.keys():
            components[cmpnt_label] = Output(cmpnt_label, {})
    for label, cmpnt in components.items():
        if isinstance(cmpnt, Conjunction) or isinstance(cmpnt, Output):
            cmpnt.state.update({inp: False for inp in cmpnt_inp_map[cmpnt.label]})
    p2_components = deepcopy(components)
    p1_total = process_all_button_presses(components)
    print(f"Part One : {p1_total}")
    print(find_all_cycle_lengths(p2_components))
