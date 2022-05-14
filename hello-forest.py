from pyquil import get_qc, Program
from pyquil.gates import CNOT, H, MEASURE

if __name__ == '__main__':
    qvm = get_qc('2q-qvm')

    p = Program()
    p += H(0)
    p += CNOT(0, 1)
    ro = p.declare('ro', 'BIT', 2)
    p += MEASURE(0, ro[0])
    p += MEASURE(1, ro[1])
    p.wrap_in_numshots_loop(8)

    print(qvm.run(p).readout_data['ro'].tolist())
