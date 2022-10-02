import qsharp
from collections import Counter
from functools import reduce
from MaxCut import PrepareAnsatzes
from scipy.optimize import minimize


def maxcut_obj(x: str):
    return reduce(lambda obj, e: obj - (1 if x[e[0]] != x[e[1]] else 0), [(0, 1), (1, 2), (2, 3), (3, 0)], 0)


def compute_expectation(cuts: Counter):
    sum, count = reduce(lambda t, c: (t[0] + (maxcut_obj(c) * cuts[c]), t[1] + cuts[c]), cuts, (0, 0))
    return sum / count


def get_expectation(shots=512):
    def execute_circ(params: list[float]):
        results = PrepareAnsatzes.simulate(theta=params, shots=shots)
        return compute_expectation(Counter(results))

    return execute_circ


expectation = get_expectation()
res = minimize(expectation, [1.0, 1.0, 1.0, 1.0], method='COBYLA')
results = PrepareAnsatzes.simulate(theta=res.x, shots=512)
count = Counter(results)
print(count["1010"])
print(count["0101"])