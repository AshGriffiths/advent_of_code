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
    dest: list["FlipFlop" | "Conjunction"]
    label: str = "broadcaster"

    def recv(self):
        # Always receives low
        for component in self.dest:
            QUEUE.append(component.label, self.label, False)


class Conjunction(NamedTuple):
    label: str
    state: dict[str, bool]
    dest: list["FlipFlop" | "Conjunction"]

    def recv(self, src: str, x: bool):
        self.state[src] = x
        output = True
        if all(self.state.values()):
            output = False
        for component in self.dest:
            QUEUE.append((component.label, self.label, output))


class FlipFlop(NamedTuple):
    label: str
    state: dict[str, bool]
    dest: list["FlipFlop" | "Conjunction"]

    def recv(self, src: str, x: bool):
        if x:
            return
        else:
            self.state[src] = not self.state[src]
            output = False
            if self.state:
                output = True
            for component in self.dest:
                QUEUE.append((component.label, self.label, output))


with open("test1.txt", "r") as input_file:
    pass
