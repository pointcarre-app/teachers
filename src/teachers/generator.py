import random
from typing import Any

import teachers.maths as tm


class MathsGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def random_integer(self, min_val: int=0, max_val: int=100) -> tm.Integer:
        """Includes both ends"""
        n = random.randint(min_val, max_val)
        return tm.Integer(n=n)

    def random_element_from(self, elements) -> Any:
        return random.choice(elements)
    
    def discrete_dirichlet_dist(self, n: int, q: int, exclude_zero: bool=True) -> list[tm.Fraction]:
        # NOTE: not all dirichlet distribution have the same probability

        probabilities = []

        if n == 1:
            return [tm.Integer(n=1)]
        
        lower_bound = int(exclude_zero)
        upper_bound = q - (n-1)

        for i in range(1, n):
            p = self.random_integer(
                lower_bound,
                upper_bound
            )
            probabilities.append(p)
            upper_bound = upper_bound -p.n + 1

        probabilities.append(tm.Integer(n=int(q-sum(x.n for x in probabilities))))
        # NOTE: do not erase, this illustrates what happens in the loop above with exclude_zero=True
        # p1 = gen.random_integer(1, upper_bound-3)
        # p2 = gen.random_integer(1, upper_bound-2-p1.n)
        # p3 = gen.random_integer(1, upper_bound-1-p1.n-p2.n)
        # p4 = tm.Integer(n=upper_bound - p1.n - p2.n - p3.n)
        probabilities = [p/q for p in probabilities]
        return tm.MathsCollection(elements=probabilities)
    
    def random_trinom(self, a_bounds=(-10, 10), b_bounds=(-10, 10), c_bounds=(-10, 10), symbol="x"):
        # TODO: use this whenever possible
        # TODO: affine
        x = tm.Symbol(s=symbol)
        a = self.random_integer(*a_bounds)
        b = self.random_integer(*b_bounds)
        c = self.random_integer(*c_bounds)
        expr = a * x**tm.Integer(n=2) + b * x + c
        return expr