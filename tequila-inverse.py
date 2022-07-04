from tequila import gates, simulate


def my_operator(q: int):
    return gates.X(q) + gates.H(q)


if __name__ == '__main__':
    q = 0
    c = my_operator(q) + gates.Z(q) + my_operator(q).dagger()

    state = simulate(c).state
    print(state)