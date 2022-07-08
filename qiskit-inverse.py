from qiskit import Aer, QuantumCircuit, QuantumRegister, transpile


def my_operator():
    q = QuantumRegister(1)
    c = QuantumCircuit(q)

    c.x(q)
    c.h(q)

    return c.to_gate()


if __name__ == '__main__':
    # print(Aer.backends())
    backend = Aer.get_backend('aer_simulator')

    q = QuantumRegister(1)
    c = QuantumCircuit(q)

    c.append(my_operator(), q)
    c.z(q)
    c.append(my_operator().inverse(), q)

    print(c.decompose())
    c.save_statevector(label="q")
    result = backend.run(transpile(c, backend)).result()
    print(result.data(0)['q'])
