namespace MaxCut {
    open Microsoft.Quantum.Arrays as Arrays;
    open Microsoft.Quantum.Canon as Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement as Measurement;

    newtype Graph = (Nodes: Qubit[], Edges: (Qubit, Qubit)[]);
    newtype DrawParams = (G: Graph, Theta: Double[]);

    operation Mixer(nodes: Qubit[], beta: Double) : Unit {
        for qubit in nodes {
            Rx(2.0 * beta, qubit);
        }
    }

    operation Problem(edges: (Qubit, Qubit)[], gamma: Double) : Unit {
        for (q1, q2) in edges {
            Exp([PauliZ, PauliZ], gamma, [q1, q2]);
        }
    }

    operation DrawAnsatz(p: DrawParams) : String {
        let theta = p::Theta;
        let mid = Length(theta) / 2;
        let betas = theta[...mid-1];
        let gammas = theta[mid...];
        let graph = p::G;
        let nodes = graph::Nodes;

        Canon.ApplyToEach(H, graph::Nodes);

        for i in 0..mid-1 {
            Problem(graph::Edges, gammas[i]);
            Mixer(nodes, betas[i]);
        }

        let result = Arrays.Fold((a, b) -> a + b, "", Arrays.Mapped(x -> x == Zero ? "0" | "1", Measurement.MultiM(nodes)));
        ResetAll(nodes);

        return result;
    }

    operation PrepareAnsatzes(theta: Double[], shots: Int) : String[] {
        use nodes = Qubit[4];
        let edges = [(nodes[0], nodes[1]), (nodes[1], nodes[2]), (nodes[2], nodes[3]), (nodes[3], nodes[0])];

        return Arrays.DrawMany(DrawAnsatz, shots, DrawParams(Graph(nodes, edges), theta));
    }
}
