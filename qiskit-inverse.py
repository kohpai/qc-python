from qiskit import Aer, QuantumCircuit, QuantumRegister, transpile


def my_operator():
    q = QuantumRegister(1)
    c = QuantumCircuit(q)

    c.x(q)
    c.h(q)

    gate = c.to_gate()
    gate.name = "MyOp"
    return gate


if __name__ == '__main__':
    # print(Aer.backends())
    backend = Aer.get_backend('aer_simulator')

    q = QuantumRegister(1)
    c = QuantumCircuit(q)

    c.append(my_operator(), q)
    c.z(q)
    c.append(my_operator().inverse(), q)

    print(c.decompose(['MyOp', 'MyOp_dg']))
    c.save_statevector(label="q")
    result = backend.run(transpile(c, backend)).result()
    print(result.data(0)['q'])
