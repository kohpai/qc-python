import copy
import tequila as tq
from tequila import gates


def xor(q1: int, q2: int, output: int):
    return gates.CNOT(q1, output) + gates.CNOT(q2, output)


def xors(inputs: list[int], ancilla: list[int]):
    return xor(inputs[0], inputs[1], ancilla[0]) + \
           xor(inputs[1], inputs[3], ancilla[1]) + \
           xor(inputs[0], inputs[2], ancilla[2]) + \
           xor(inputs[2], inputs[3], ancilla[3])


def sudoku_oracle(inputs: list[int], ancilla: list[int], output: int):
    circuit = xors(inputs, ancilla)
    circuit_t = copy.deepcopy(circuit)
    return circuit + gates.X(output, ancilla) + circuit_t


def reflect_zero(inputs: list[int]):
    return gates.X(inputs) + \
           gates.Z(inputs[-1], inputs[:len(inputs) - 1]) + \
           gates.X(inputs)


def reflect_initial(init_op: tq.QCircuit, inputs: list[int]):
    return init_op.dagger() + reflect_zero(inputs) + init_op


def grover_circuit():
    inputs = [i for i in range(4)]
    ancilla = [i + 4 for i in range(4)]
    pkb = 8

    prepare_initial_state = gates.H(inputs)

    circuit = prepare_initial_state + gates.X(pkb) + gates.H(pkb)

    for _ in range(2):
        circuit += sudoku_oracle(inputs, ancilla, pkb)
        circuit += reflect_initial(prepare_initial_state, inputs)

    return circuit


measurements = tq.simulate(
    grover_circuit(),
    samples=512,
    read_out_qubits=list(range(4))
    )
print(measurements)
