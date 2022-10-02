from cirq import Circuit, CNOT, H, inverse, LineQubit, measure, Simulator, X, Z
from cirq.ops import OP_TREE


def xor(q1: LineQubit, q2: LineQubit, output: LineQubit):
    return [CNOT(q1, output),
            CNOT(q2, output)]


def xors(inputs: list[LineQubit], ancilla: list[LineQubit]):
    return [xor(inputs[0], inputs[1], ancilla[0]),
            xor(inputs[1], inputs[3], ancilla[1]),
            xor(inputs[0], inputs[2], ancilla[2]),
            xor(inputs[2], inputs[3], ancilla[3])]


def sudoku_oracle(inputs: list[LineQubit], ancilla: list[LineQubit],
                  output: LineQubit):
    comp = xors(inputs, ancilla)
    return [comp, X.controlled(4).on(*ancilla, output), inverse(comp)]


def reflect_zero(inputs: list[LineQubit]):
    length = len(inputs)

    return [X.on_each(inputs),
            Z.controlled(length - 1).on(*inputs[:length - 1], inputs[-1]),
            inverse(X.on_each(inputs))]


def reflect_initial(init_op: OP_TREE, qubits: list[LineQubit]):
    return [inverse(init_op), reflect_zero(qubits), init_op]


def grover_circuit():
    inputs = [LineQubit(i) for i in range(4)]
    ancilla = [LineQubit(i + 4) for i in range(4)]
    pkb = LineQubit(8)

    c = Circuit()

    prepare_initial_state = H.on_each(inputs)

    c.append(prepare_initial_state)
    c.append([X(pkb), H(pkb)])
    c.concat_ragged()

    for _ in range(2):
        c.append(sudoku_oracle(inputs, ancilla, pkb))
        c.append(reflect_initial(prepare_initial_state, inputs))

    c.append(measure(*inputs, key="result"))

    return c


def bits_to_str(bits: list[int]):
    return ''.join(list(map(lambda i: str(i), bits)))


circuit = grover_circuit()
result = Simulator().run(circuit, repetitions=512)
count = result.histogram(key="result", fold_func=bits_to_str)
print(count["1010"])
print(count["0101"])
