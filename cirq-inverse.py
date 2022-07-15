from cirq import LineQubit, X, H, Circuit, inverse, Simulator, Z


def my_operator(q: LineQubit):
    return [X(q),
            H(q)]


if __name__ == '__main__':
    q = LineQubit(0)
    ops1 = my_operator(q)
    ops2 = inverse(ops1)
    c = Circuit(ops1, Z(q), ops2)

    print(c)
    # print(decompose(c))
    simulator = Simulator()
    for i, step in enumerate(simulator.simulate_moment_steps(c)):
        print('state at step %d: %s' % (i, step.state_vector(copy=True)))
