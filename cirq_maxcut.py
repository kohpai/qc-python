from collections import Counter
from functools import reduce

from cirq import Circuit, H, LineQubit, measure, Rx, Simulator
from networkx import Graph
from openfermion import Rzz
from scipy.optimize import minimize
from sympy import Symbol


def mixer(g: Graph, beta: Symbol):
    return [Rx(rads=2 * beta)(q) for q in list(g.nodes())]


def problem(g: Graph, gamma: Symbol):
    return [Rzz(rads=2 * gamma)(i, j) for i, j in g.edges()]


def create_qaoa_circ(g: Graph, beta: Symbol, gamma: Symbol):
    return Circuit(
        H.on_each(*nodes),
        problem(g, gamma),
        mixer(g, beta),
        problem(g, gamma),
        mixer(g, beta),
        measure(*nodes, key="cut")
    )


def maxcut_obj(x: str, g: Graph):
    return reduce(lambda obj, e: obj - (1 if x[e[0].x] != x[e[1].x] else 0), g.edges(), 0)


def compute_expectation(cuts: Counter, g: Graph):
    total, count = reduce(lambda t, c: (t[0] + (maxcut_obj(c, g) * cuts[c]), t[1] + cuts[c]), cuts, (0, 0))
    return total / count


def bits_to_str(bits: list[int]):
    return ''.join(list(map(lambda i: str(i), bits)))


def get_expectation(g: Graph, shots=512):
    sim = Simulator()

    def execute_circ(params: list[float]):
        beta = Symbol("beta")
        gamma = Symbol("gamma")
        qc = create_qaoa_circ(g, beta, gamma)
        result = sim.run(qc, {beta: params[0], gamma: [params[1]]}, shots)
        return compute_expectation(result.histogram(key="cut", fold_func=bits_to_str), g)

    return execute_circ


if __name__ == '__main__':
    g = Graph()
    nodes = [LineQubit(i) for i in range(4)]
    edges = [(nodes[i], nodes[(i + 1) % 4]) for i in range(4)]
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    expectation = get_expectation(g)
    res = minimize(expectation, [1.0, 1.0], method='COBYLA')
    print(res)

    beta = Symbol("beta")
    gamma = Symbol("gamma")
    qc = create_qaoa_circ(g, beta, gamma)
    result = Simulator().run(qc, {beta: res.x[0], gamma: res.x[1]}, 512)
    count = result.histogram(key="cut", fold_func=bits_to_str)
    print(count["1010"])
    print(count["0101"])
