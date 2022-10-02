from functools import reduce
from networkx import Graph
from qiskit import Aer, QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit import Parameter
from scipy.optimize import minimize


def mixer(g: Graph, beta: Parameter):
    qubits = QuantumRegister(g.number_of_nodes())

    qc = QuantumCircuit(qubits)
    for q in qubits:
        qc.rx(2 * beta, q)
    return qc


def problem(g: Graph, gamma: Parameter):
    qc = QuantumCircuit(g.number_of_nodes())

    for i, j in g.edges():  # pairs of nodes
        qc.rzz(2 * gamma, i, j)
    return qc


def maxcut_obj(x: str, g: Graph):
    return reduce(lambda obj, e : obj - (1 if x[e[0]] != x[e[1]] else 0), g.edges(), 0)


def compute_expectation(counts, g: Graph):
    avg, sum_count = reduce(lambda t, c: (t[0] + (maxcut_obj(c[0], g) * c[1]), t[1] + c[1]), counts.items(), (0, 0))
    return avg/sum_count


def create_qaoa_circ(g: Graph, theta: list[Parameter]):
    mid = len(theta) // 2
    betas = theta[:mid]
    gammas = theta[mid:]
    qubits = QuantumRegister(g.number_of_nodes())
    qc = QuantumCircuit(qubits)

    # initial_state
    qc.h(qubits)

    for i in range(mid):
        qc.append(problem(g, gammas[i]), qubits)
        qc.append(mixer(g, betas[i]), qubits)

    qc.measure_all()

    return qc


def get_expectation(g: Graph, nparams: int, shots=512):
    backend = Aer.get_backend('aer_simulator')
    mid = nparams // 2
    betas = [Parameter(f"$\\beta_{i}$") for i in range(mid)]
    gammas = [Parameter(f"$\\gamma_{i}$") for i in range(mid)]
    theta = betas + gammas
    qc = create_qaoa_circ(g, theta)

    def execute_circ(params: list[float]):
        binding = {theta[i]: params[i] for i in range(len(params))}
        counts = backend.run(transpile(qc.bind_parameters(binding), backend), shots=512).result().get_counts()
        return compute_expectation(counts, g)

    return execute_circ


g = Graph()
g.add_nodes_from([0, 1, 2, 3])
g.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

init_params = [1.0, 1.0, 1.0, 1.0]
expectation = get_expectation(g, len(init_params))
res = minimize(expectation, init_params, method='COBYLA')

backend = Aer.get_backend('aer_simulator')

betas = [Parameter("$\\beta_0$"), Parameter("$\\beta_1$")]
gammas = [Parameter("$\\gamma_0$"), Parameter("$\\gamma_1$")]
theta = betas + gammas
binding = {theta[i]: res.x[i] for i in range(4)}
qc_res = create_qaoa_circ(g, theta).bind_parameters(binding)

count = backend.run(transpile(qc_res, backend), shots=512).result().get_counts()
print(count["1010"])
print(count["0101"])