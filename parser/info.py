from dataclasses import dataclass


@dataclass(init=False, frozen=True)
class Engine:
    version = "0.0.1-Alpha1"
