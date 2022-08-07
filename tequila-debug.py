from tequila import QubitWaveFunction, paulis
import numpy as np


H = 1.0 / np.sqrt(2) * (paulis.Z(0) + paulis.X(0))


def my_operator(q: QubitWaveFunction):
    return q.apply_qubitoperator(paulis.X(0)).apply_qubitoperator(H)


def my_operator_dg(q: QubitWaveFunction):
    return q.apply_qubitoperator(H).apply_qubitoperator(paulis.X(0))


if __name__ == '__main__':
    q0 = QubitWaveFunction.from_string('1.0*|0>')
    q1 = my_operator(q0)
    q2 = q1.apply_qubitoperator(paulis.Z(0))
    q3 = my_operator_dg(q2)
    print(q0)
    print(q1)
    print(q2)
    print(q3)
