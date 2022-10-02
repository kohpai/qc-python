from collections import Counter
from functools import reduce
from networkx import Graph
import tequila as tq
from tequila import gates
from scipy.optimize import minimize


def mixer(g: Graph, beta: float):
    return gates.Rx(2 * beta, list(g.nodes()))


def problem(g: Graph, gamma: float):
    return reduce(lambda c, e: c + gates.ExpPauli({e[0]: 'Z', e[1]: 'Z'}, gamma), g.edges(), tq.QCircuit())


def qaoa_circuit(g: Graph, theta: list[float]):
    mid = len(theta) // 2
    betas = theta[:mid]
    gammas = theta[mid:]
    c = gates.H(list(g.nodes()))
    for i in range(mid):
        c += problem(g, gammas[i]) + mixer(g, betas[i])

    return c


def maxcut_obj(x: str, g: Graph):
    return reduce(lambda obj, e : obj - (1 if x[e[0]] != x[e[1]] else 0), g.edges(), 0)


def compute_expectation(cuts: Counter, g: Graph):
    sum, count = reduce(lambda t, c: (t[0] + (maxcut_obj(c, g) * cuts[c]), t[1] + cuts[c]), cuts, (0, 0))
    return sum / count


def get_expectation(g: Graph, shots=512):
    def execute_circ(params: list[float]):
        qc = qaoa_circuit(g, params)
        results = tq.simulate(qc, samples=shots, read_out_qubits=[0,1,2,3])
        counter = Counter({str(k.binary): int(v) for k, v in results.items()})
        return compute_expectation(counter, g)

    return execute_circ


g = Graph()
g.add_nodes_from([0, 1, 2, 3])
g.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

expectation = get_expectation(g)
res = minimize(expectation, [1.0, 1.0, 1.0, 1.0], method='COBYLA')
circuit = qaoa_circuit(g, res.x)
results = tq.simulate(circuit, samples=512, read_out_qubits=[0,1,2,3])
count = Counter({str(k.binary): int(v) for k, v in results.items()})
print(count["1010"])
print(count["0101"])
