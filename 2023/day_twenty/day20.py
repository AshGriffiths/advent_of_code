from collections import deque
from typing import NamedTuple

# To, From, Value
QUEUE: deque[tuple[str, str, bool]] = deque()


class Button(NamedTuple):
    label: str = "button"

    def recv(self):
        # Always sends low to broadcaster
        QUEUE.append("broadcaster", self.label, False)


class Broadcaster(NamedTuple):
    dest: list[str]
    label: str = "broadcaster"

    def recv(self):
        # Always receives low
        for component in self.dest:
            QUEUE.append(component, self.label, False)


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
            if self.state:
                output = True
            for component in self.dest:
                QUEUE.append((component, self.label, output))


with open("input.txt", "r") as input_file:
    components: dict[str, Broadcaster | FlipFlop | Conjunction] = {}
    component_defn = input_file.readlines()
    cmpnt_inp_map: dict[str, list[str]] = {}
    for line in component_defn:
        cmpnt_desc, dest_list = line.split(" -> ")
        dests = dest_list.strip().split(", ")
        cmpnt: Broadcaster | FlipFlop | Conjunction
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
    for cmpnt in components.values():
        if isinstance(cmpnt, Conjunction):
            cmpnt.state.update({inp: False for inp in cmpnt_inp_map[cmpnt.label]})
    print(components)
