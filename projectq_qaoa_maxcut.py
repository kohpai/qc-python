from collections import Counter
from functools import reduce
from networkx import Graph
from projectq import MainEngine
from projectq.ops import All, H, Measure, QubitOperator, Rx, Rzz, X
from scipy.optimize import minimize


def mixer(g: Graph, beta: float):
    for n in g:
        Rx(2*beta) | n


def problem(g: Graph, gamma: float):
    for i, j in g.edges():
        Rzz(2*gamma) | (i, j)


def prepare_state(g: Graph, theta: list[float]):
    mid = len(theta) // 2
    betas = theta[:mid]
    gammas = theta[mid:]
    qubits = list(g.nodes())

    # make sure all qubits are zero
    All(Measure) | qubits
    for n in g:
        if int(n):
            X | n

    All(H) | qubits
    for i in range(mid):
        problem(g, gammas[i])
        mixer(g, betas[i])

    eng.flush()


def sample_circuit(g: Graph, theta: list[float]):
    qubits = list(g.nodes())

    prepare_state(g, theta)
    All(Measure) | qubits
    eng.flush()

    return ''.join(list(map(lambda x: str(int(x)), qubits)))


def get_expectation(g: Graph):
    def execute_circ(params: list[float]):
        prepare_state(g, params)
        return eng.backend.get_expectation_value(problem_hamiltonian, list(g.nodes()))

    return execute_circ


eng = MainEngine()
g = Graph()
nodes = eng.allocate_qureg(4)
edges = [(nodes[i], nodes[(i+1) % 4]) for i in range(4)]
g.add_nodes_from(nodes)
g.add_edges_from(edges)
problem_hamiltonian = reduce(lambda s, curr: s + curr, map(lambda e: QubitOperator(((e[0].id, "Z"), (e[1].id, "Z"))), edges))

expectation = get_expectation(g)
res = minimize(expectation, [1.0, 1.0, 1.0, 1.0], method='COBYLA')

count = Counter([sample_circuit(g, res.x) for _ in range(512)])
print(count["1010"])
print(count["0101"])
