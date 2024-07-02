class Logger:
    def __init__(self, architecture, qubits):
        self.arch = architecture
        self.qubits = qubits
        print()

    def __arch_str(self) -> str:
        return f"{self.arch}-{self.qubits}qubits"

    def pre_start_induced_connected_subgraphs(self):
        print()
        print(self.__arch_str(), "precomputing induced connected subgraphs")

    def start_induced_connected_subgraphs(self, combinations_num):
        self.combinations_num = combinations_num
        print(self.__arch_str(), "computing", combinations_num, "subgraphs")

    def update_induced_connected_subgraphs(self, current_num):
        self.current_num = current_num
        print(
            self.__arch_str(),
            "computing induced subgraph",
            current_num,
            "of",
            self.combinations_num,
        )

    def start_isomorphism_elimination(self, graphs_num):
        self.graphs_num = graphs_num
        print(self.__arch_str(), "eliminating isomorphism from", graphs_num, "graphs")

    def start_connected_subgraphs(self, subgraph_num):
        self.subgraph_num = subgraph_num
        print()
        print(
            self.__arch_str(),
            "computing all connected subgraphs of",
            subgraph_num,
            "subgraphs",
        )

    def update_connected_subgraphs(self, current_num):
        self.current_num = current_num
        print(
            self.__arch_str(),
            "computing edge reduction of subgraph",
            current_num,
            "out of",
            self.subgraph_num,
        )

    def start_optimal_subgraphs(self, cand_num):
        self.cand_num = cand_num
        print()
        print(
            self.__arch_str(), "computing optimal subgraphs of", cand_num, "candidates"
        )

    def update_optimal_subgraphs(self, current_num):
        self.current_num = current_num
        print(
            self.__arch_str(),
            "checking subgraphism of candidate",
            current_num,
            "of",
            self.cand_num,
        )

    def finish(self, optimal_count):
        self.optimal_count = optimal_count
        print()
        print(self.__arch_str(), "Finished.")
        print("Computed", optimal_count, "subgraphs out of")
        print(self.cand_num, "candidates")
        print(self.subgraph_num, "connected subgraphs")
        print(self.combinations_num, "induced subgraphs")


class DummyLogger:
    def __init__(self, architecture=None, qubits=None):
        pass

    def pre_start_induced_connected_subgraphs(self):
        pass

    def start_induced_connected_subgraphs(self, combinations_num):
        pass

    def update_induced_connected_subgraphs(self, current_num):
        pass

    def start_connected_subgraphs(self, subgraph_num):
        pass

    def update_connected_subgraphs(self, current_num):
        pass

    def start_optimal_subgraphs(self, cand_num):
        pass

    def update_optimal_subgraphs(self, current_num):
        pass

    def start_isomorphism_elimination(self, graphs_num):
        pass

    def finish(self, optimal_count):
        pass
