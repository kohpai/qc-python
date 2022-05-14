import cirq


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def hello_cirq():
    # Pick a qubit.
    qubit = cirq.GridQubit(0, 0)

    # Create a circuit
    circuit = cirq.Circuit(
        cirq.X(qubit)**0.5,  # Square root of NOT.
        cirq.measure(qubit, key='m')  # Measurement.
    )
    print("Circuit:")
    print(circuit)

    # Simulate the circuit several times.
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    print("Results:")
    print(result)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    hello_cirq()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
