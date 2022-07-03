from cirq import LineQubit, X, H, Circuit, inverse, Simulator, Z
import numpy as np


# class MyGate(Gate):
#     def __init__(self):
#         super(MyGate, self)
#
#     def _num_qubits_(self):
#         return 1
#
#     def _unitary_(self):
#         return np.array([
#             [1.0,  1.0],
#             [-1.0, 1.0]
#         ]) / np.sqrt(2)
#
#     def _circuit_diagram_info_(self, args):
#         return "G"
#
#     def __pow__(self, power, modulo=None):
#         return NotImplemented if power != -1 else MyGateInverse()
#
#
# class MyGateInverse(Gate):
#     def __init__(self):
#         super(MyGateInverse, self)
#
#     def _num_qubits_(self):
#         return 1
#
#     def _unitary_(self):
#         return np.array([
#             [1.0,  -1.0],
#             [1.0, 1.0]
#         ]) / np.sqrt(2)
#
#     def _circuit_diagram_info_(self, args):
#         return "G'"
#
#     def __pow__(self, power, modulo=None):
#         return NotImplemented if power != -1 else MyGate()


def my_operator(q: LineQubit):
    # my_gate = MyGate()
    return [X(q),
            H(q)]


if __name__ == '__main__':
    q = LineQubit(0)
    ops1 = my_operator(q)
    ops2 = inverse(ops1)
    c = Circuit(ops1, Z(q), ops2)

    simulator = Simulator()
    result = simulator.simulate(c)
    print(np.around(result.final_state_vector, 3))
