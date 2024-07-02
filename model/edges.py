from dataclasses import dataclass
from model.state import State


@dataclass
class edges:
    state1: State
    state2: State
    weight: int
