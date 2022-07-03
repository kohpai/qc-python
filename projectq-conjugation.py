from projectq import MainEngine
from projectq.meta import Compute, Uncompute
from projectq.ops import H, X
from projectq.types import Qubit


def my_operator(q: Qubit):
    X | q
    H | q


if __name__ == '__main__':
    eng = MainEngine()
    q = eng.allocate_qubit()[0]

    with Compute(eng):
        my_operator(q)
    Uncompute(eng)

    eng.flush()

    _, vector = eng.backend.cheat()

    print(vector)
