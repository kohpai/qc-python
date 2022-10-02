from collections import Counter
from collections.abc import Callable
from projectq import MainEngine
from projectq.meta import Compute, Control, Dagger, Uncompute
from projectq.ops import All, CNOT, H, Measure, X, Z
from projectq.types import Qureg, Qubit


def xor(q1: Qubit, q2: Qubit, output: Qubit):
    CNOT | (q1, output)
    CNOT | (q2, output)


def sudoku_oracle(e: MainEngine, inputs: Qureg[Qubit], tmp: Qureg[Qubit], output: Qubit):
    with Compute(e):
        xor(inputs[0], inputs[1], tmp[0])
        xor(inputs[1], inputs[3], tmp[1])
        xor(inputs[0], inputs[2], tmp[2])
        xor(inputs[2], inputs[3], tmp[3])
    with Control(e, tmp):
        X | output
    Uncompute(e)


def reflect_zero(e: MainEngine, inputs: Qureg[Qubit]):
    with Compute(e):
        All(X) | inputs
    with Control(e, inputs[:len(inputs) - 1]):
        Z | inputs[-1]
    Uncompute(e)


def reflect_initial(e: MainEngine, init_op: Callable[[MainEngine, Qureg], None], qubits: Qureg):
    with Compute(e):
        with Dagger(e):
            init_op(e, qubits)

    reflect_zero(e, qubits)
    Uncompute(e)


def grover_circuit():
    eng = MainEngine()

    inputs = eng.allocate_qureg(4)
    tmp = eng.allocate_qureg(4)
    pkb = eng.allocate_qubit()

    def prepare_initial_state(_: MainEngine, qubits: Qureg):
        All(H) | qubits

    prepare_initial_state(eng, inputs)

    X | pkb
    H | pkb

    for _ in range(2):
        sudoku_oracle(eng, inputs, tmp, pkb)
        reflect_initial(eng, prepare_initial_state, inputs)

    All(Measure) | inputs
    # garbage
    All(Measure) | tmp
    Measure | pkb

    eng.flush()

    return map(lambda x: int(x), inputs)


data = Counter([''.join(map(lambda x: str(x), grover_circuit())) for _ in range(512)])
print(data["1001"])
print(data["0110"])
