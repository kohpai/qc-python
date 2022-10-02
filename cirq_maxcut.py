from collections import Counter
from functools import reduce
from cirq import Circuit, H, LineQubit, measure, Rx, Simulator
from openfermion import Rzz
from scipy.optimize import minimize
from sympy import Symbol
from typing import NewType, Tuple

Graph = NewType('Graph', Tuple[list[LineQubit], list[Tuple[LineQubit, LineQubit]]])


def mixer(g: Graph, beta: Symbol):
    return [Rx(rads=2 * beta)(q) for q in g[0]]


def problem(g: Graph, gamma: Symbol):
    return [Rzz(rads=2 * gamma)(i, j) for i, j in g[1]]


def qaoa_circuit(g: Graph, theta: list[Symbol]):
    qubits = g[0]
    mid = len(theta) // 2
    betas = theta[:mid]
    gammas = theta[mid:]

    circuit = Circuit(H.on_each(*qubits))

    for i in range(mid):
        circuit.append(problem(g, gammas[i]))
        circuit.append(mixer(g, betas[i]))

    circuit.append(measure(*qubits, key="cut"))

    return circuit


def maxcut_obj(x: str, g: Graph):
    return reduce(lambda obj, e: obj - (1 if x[e[0].x] != x[e[1].x] else 0), g[1], 0)


def compute_expectation(cuts: Counter, g: Graph):
    total, count = reduce(
        lambda t, c: (t[0] + (maxcut_obj(c, g) * cuts[c]), t[1] + cuts[c]),
        cuts,
        (0, 0)
        )
    return total / count


def bits_to_str(bits: list[int]):
    return ''.join(list(map(lambda i: str(i), bits)))


def get_expectation(g: Graph, nparams: int, shots=512):
    sim = Simulator()
    mid = nparams // 2
    betas = [Symbol(f"beta{i}") for i in range(mid)]
    gammas = [Symbol(f"gamma{i}") for i in range(mid)]
    theta = betas + gammas
    qc = qaoa_circuit(g, theta)

    def execute_circ(params: list[float]):
        binding = {theta[i]:params[i] for i in range(len(params))}
        result = sim.run(qc, binding, shots)
        return compute_expectation(result.histogram(key="cut", fold_func=lambda x: ''.join(list(map(lambda i: str(i), x)))), g)

    return execute_circ


nodes = [LineQubit(i) for i in range(4)]
edges = [(nodes[i], nodes[(i + 1) % 4]) for i in range(4)]
graph = Graph((nodes, edges))

init_params = [1.0, 1.0, 1.0, 1.0]
expectation = get_expectation(graph, len(init_params))
res = minimize(expectation, init_params, method='COBYLA')

betas = [Symbol("beta0"), Symbol("beta1")]
gammas = [Symbol("gamma0"), Symbol("gamma1")]
theta = betas + gammas
qc = qaoa_circuit(graph, theta)
binding = {theta[i]: res.x[i] for i in range(4)}
result = Simulator().run(qc, binding, 512)
count = result.histogram(key="cut", fold_func=bits_to_str)
print(count["1010"])
print(count["0101"])
