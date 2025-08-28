class Hypercube:
    """Generate all possible cases from a generate_component function.
    Parse > Itertools > Replace creation with generator or other > Generate"""

    # TODO : sel & mad: we need to be sure about the stuff we can use in the generators
    # (better to encapsulate everyhing in the tm.Generator + to have a "single generate to force value or smarter")

    def __init__(self, p: int):
        self.p = p

    def __repr__(self):
        return f"Hypercube(n={self.p})"

    def __str__(self):
        return f"Hypercube(n={self.p})"
