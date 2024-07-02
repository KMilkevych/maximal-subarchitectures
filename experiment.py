# Import qmap
from mqt import qmap

# Import graph libraries ( :)
# import networkx as nx
# import rustworkx as rx

# Import
import qiskit

# Import miscellaneous helper functions
from misc.timing import time_it
from misc.random_qc import random_circuit
from misc.graph_to_arch import graph_to_architecture, normalize_graph, edge_view

# Import algorithmic and architecture functions
import lib.architectures as arch
import lib.algorithm as alg

# Import csv for saving measured data
import csv


# Run using Q-synth
def q_synth(architecture_name, circuitfile, platform_size, filename, qsynth_dir, full=True):

    # Import module for calling q_synth and io for string printing
    import subprocess
    import io
    import os

    print(f"Starting testing for {circuitfile}")
    print(f"Starting to compute maximal subarchitectures for {architecture_name} with {platform_size} qubits")

    # Compute platform sub-architectures
    architecture = arch.architecture[architecture_name]()
    platform_size = int(platform_size)
    subarchitectures = alg.size_k_optimal_subgraphs_slow(architecture, platform_size)
    if full is not None:
        full = full.strip().tolower() == 'true'
    else:
        full = True

    print(f"Computed {len(subarchitectures)} maximal subarchitectures")

    working_dir = os.getcwd()

    # Read all outputs
    outlines = []


    # Map to each sub-architecture
    for sarcht in subarchitectures:

        sarch = edge_view(sarcht, bidirectional=False)

        # Get subarchitecture as edge list string in "edges"
        el = list(sarch)
        buf = io.StringIO()
        print(el, file=buf, end="")
        edges = buf.getvalue()
        buf.close()

        # Pass to Q-synth
        args = [
            ".venv/bin/python3.11",
            "q-synth.py",
            "-b1",  # bidirectional
            "-a0",  # no ancillaries
            "-m",
            "sat",  # use sat solving
            "-p",
            "test",  # Specify that the platform is provided
            f"--coupling_graph={edges}",  # provide coupling graph
            "-v0",  # high verbosity
            "-s",
            "cd15",  # cd15 solver
            circuitfile
        ]

        print()
        print(args)
        print()

        # Run Q-Synth
        os.chdir(qsynth_dir)
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        outlines.append(proc.stdout)
        os.chdir(working_dir)

        print("="*60)


    # Perform mapping to full platform
    # Get subarchitecture as edge list string in "edges"
    el = list(architecture.edges())
    buf = io.StringIO()
    print(el, file=buf, end="")
    edges = buf.getvalue()
    buf.close()

    # Pass to Q-synth
    args = [
        ".venv/bin/python3.11",
        "q-synth.py",
        "-b1",  # bidirectional
        "-a0",  # no ancillaries
        "-m",
        "sat",  # use sat solving
        "-p",
        "test",  # Specify that the platform is provided
        f"--coupling_graph={edges}",  # provide coupling graph
        "-v0",  # high verbosity
        "-s",
        "cd15",  # cd15 solver
        circuitfile
    ]


    if full:
        print()
        print(args)
        print()

        # Run Q-Synth
        os.chdir(qsynth_dir)
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        outlines.append(proc.stdout)
        os.chdir(working_dir)


    # Print results and write to file
    with open(filename, "a+") as f:
        f.writelines(["="*60+"\n"])
        f.writelines(outlines)
        f.writelines(["="*60+"\n"])

    for line in outlines:
        print(line)


# Specific circuit from qasm file
def opt_qasm(architecture_name, circuitfile, filename, ancillaries=None):

    # Parse arguments
    architecture = arch.architecture[architecture_name]()
    qc = qiskit.QuantumCircuit.from_qasm_file(circuitfile)
    circuit_size = len(qc.qubits)
    qmap_architecture = graph_to_architecture(architecture)

    if ancillaries is None:
        ancillaries = 0
    else:
        ancillaries = int(ancillaries)

    subarchitecture_size = circuit_size + ancillaries

    # Helper functions for some stuff
    def comp_opt_subarch():
        return alg.size_k_optimal_subgraphs_slow(architecture, subarchitecture_size)

    def comp_subarch_order():
        return qmap.SubarchitectureOrder.from_qmap_architecture(qmap_architecture)

    def comp_opt_cov(order, size):
        def fun():
            return order.covering(circuit_size, size)
        return fun

    def comp_opt_mapping(qc, arch):
        def fun():
            comp = qmap.compile(qc, arch, method="exact", post_mapping_optimizations=False)
            return comp[1].json()["statistics"]
        return fun

    print(f"Testing fixed fixed circuit {circuitfile} on {architecture_name} with {circuit_size} qubits in circuit and {subarchitecture_size} qubits on architecture")

    # Time and compute subarchitecture order
    order, order_t = time_it(comp_subarch_order)

    print(f"Computed subarchitecture order: {order_t}s")

    # Time and compute optimal subarchitectures
    optsubarch, optsubarch_t = time_it(comp_opt_subarch)

    print(f"Computed optimal subarchitectures: {len(optsubarch)} in {optsubarch_t}s")

    # Time and compute coverings of various sizes
    coverings = []
    coverings_t = []
    for size in range(1, len(optsubarch) + 1):
        cov, cov_t = time_it(comp_opt_cov(order, size))
        coverings.append(cov)
        coverings_t.append(cov_t)

        print(f"Computed covering of size {size} in {cov_t}s")

    # Map circuit to our subarchitectures first
    sub = None
    sub_t = 0.0
    for subarch in optsubarch:
        archt = graph_to_architecture(subarch)
        mp, mp_t = time_it(comp_opt_mapping(qc, archt))
        sub_t += mp_t
        if sub is None or mp["additional_gates"] < sub:
            sub = mp["additional_gates"]

    print(f"Mapped to all subarchitectures with {sub} in {sub_t}s")

    # Map circuit to each covering of each size
    coveringmp = []
    coveringmp_t = []
    for size, covering in enumerate(coverings, start=1):

        print(f"Starting mapping to size {size} covering")

        # Map circuit to each subarchitecture in covering
        cov = None
        cov_t = 0.0
        for subarch in covering:
            archt = qmap.Architecture(len(subarch.nodes()), set(subarch.edge_list()))
            mp, mp_t = time_it(comp_opt_mapping(qc, archt))
            cov_t += mp_t
            if cov is None or mp["additional_gates"] < cov:
                cov = mp["additional_gates"]

        # Save these data
        print(f"Mapped to size {size} covering with {cov} in {cov_t}s")

        coveringmp.append(cov)
        coveringmp_t.append(cov_t)

    # Write results to file
    with open(filename, "a+", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=" ")

        # Write header
        header_1 = [
            "Architecture",
            "Circuit",
            "Circuit size",
            "Ancillaries used",
            "Order compute time",
            "Subarchitecture compute time",
            "Subarchitecure number",
        ]
        header_2 = []
        for size in range(1, len(optsubarch) + 1):
            header_2 += [f"Covering size {size} compute time"]
        header_3 = ["Subarchitecture swaps", "Subarchitecture map time"]
        for size in range(1, len(optsubarch) + 1):
            header_3 += [f"Covering size {size} swaps", f"Covering size {size} map time"]
        writer.writerow(header_1 + header_2 + header_3)

        # Write results
        row_1 = [
            architecture_name,
            circuitfile,
            circuit_size,
            ancillaries,
            order_t,
            optsubarch_t,
            len(optsubarch),
        ]
        row_2 = coverings_t[:]
        row_3 = [sub, sub_t]
        for idx in range(len(coveringmp)):
            row_3 += [coveringmp[idx], coveringmp_t[idx]]
        writer.writerow(row_1 + row_2 + row_3)


# Random circuit optimality
def opt_random(architecture_name, circuit_size, subarchitecture_size, filename, reps=1):

    architecture = arch.architecture[architecture_name]()
    circuit_size = int(circuit_size)
    subarchitecture_size = int(subarchitecture_size)
    reps = int(reps)

    # Also map the original architecture
    qmap_architecture = graph_to_architecture(architecture)

    # Generate a single random circuit (but allow for more?)
    circuits = [random_circuit(circuit_size, 4).decompose() for _ in range(reps)]

    # Helper functions for some stuff
    def comp_opt_subarch():
        return alg.size_k_optimal_subgraphs_slow(architecture, subarchitecture_size)

    def comp_subarch_order():
        return qmap.SubarchitectureOrder.from_qmap_architecture(qmap_architecture)

    def comp_opt_cov(order, size):
        def fun():
            return order.covering(circuit_size, size)
        return fun

    def comp_opt_mapping(qc, arch):
        def fun():
            comp = qmap.compile(qc, arch, method="exact", post_mapping_optimizations=False)
            #return comp[1].json()["statistics"]
            return comp[1]
        return fun

    print(f"Testing {reps} random circuits on {architecture_name} with {circuit_size} qubits in circuit and {subarchitecture_size} qubits on architecture")

    # Time and compute subarchitecture order
    order, order_t = time_it(comp_subarch_order)

    print(f"Computed subarchitecture order: {order_t}s")

    # Time and compute optimal subarchitectures
    optsubarch, optsubarch_t = time_it(comp_opt_subarch)

    print(f"Computed optimal subarchitectures: {len(optsubarch)} in {optsubarch_t}s")

    # Time and compute coverings of various sizes
    coverings = []
    coverings_t = []
    for size in range(1, len(optsubarch) + 1):
        cov, cov_t = time_it(comp_opt_cov(order, size))
        coverings.append(cov)
        coverings_t.append(cov_t)

        print(f"Computed covering of size {size} in {cov_t}s")

    # Time and compute for each random circuit
    # Each row will be:
    # sub_mp, sub_mp_t, cov_1, cov_1_t, cov_2, cov_2_t, ...
    mapping = [[] for _ in circuits]
    mapping_t = [[] for _ in circuits]
    for idx, qc in enumerate(circuits):

        print("Starting mapping to subarchitectures")
        
        # Map circuit to our subarchitectures first
        sub = None
        sub_t = 0.0
        for subarch in optsubarch:
            archt = graph_to_architecture(subarch)
            mp, mp_t = time_it(comp_opt_mapping(qc, archt))
            mp = mp.json()["statistics"]
            sub_t += mp_t
            if sub is None or mp["additional_gates"] < sub:
                sub = mp["additional_gates"]

        mapping[idx] += [sub]
        mapping_t[idx] += [sub_t]

        print(f"Mapped to all subarchitectures with {sub} in {sub_t}s")

        # Map circuit to each covering of each size
        for size, covering in enumerate(coverings, start=1):

            print(f"Starting mapping to size {size} covering")

            # Map circuit to each subarchitecture in covering
            cov = None
            cov_t = 0.0
            for subarch in covering:
                archt = qmap.Architecture(len(subarch.nodes()), set(subarch.edge_list()))
                mp, mp_t = time_it(comp_opt_mapping(qc, archt))
                mp = mp.json()["statistics"]
                cov_t += mp_t
                if cov is None or mp["additional_gates"] < cov:
                    cov = mp["additional_gates"]

            # Save these data
            mapping[idx] += [cov]
            mapping_t[idx] += [cov_t]

            print(f"Mapped to size {size} covering with {cov} in {cov_t}s")

    # Write to csv file to save results
    with open(filename, "a+", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=" ")

        # Write header
        header_1 = [
            "Architecture",
            "Circuit size",
            "Subarchitecture size",
            "Order compute time",
            "Subarchitecture compute time",
            "Subarchitecure number",
        ]
        header_2 = []
        for size in range(1, len(optsubarch) + 1):
            header_2 += [f"Covering size {size} compute time"]
        header_3 = ["Subarchitecture swaps", "Subarchitecture map time"]
        for size in range(1, len(optsubarch) + 1):
            header_3 += [f"Covering size {size} swaps", f"Covering size {size} map time"]
        writer.writerow(header_1 + header_2 + header_3)

        # Write results
        for cidx in range(len(circuits)):
            row_1 = [
                architecture_name,
                circuit_size,
                subarchitecture_size,
                order_t,
                optsubarch_t,
                len(optsubarch),
            ]
            row_2 = coverings_t[:]
            row_3 = []
            for idx in range(len(mapping[cidx])):
                row_3 += [mapping[cidx][idx], mapping_t[cidx][idx]]
            writer.writerow(row_1 + row_2 + row_3)


# Subarchitecture counting
def count_subarch(architecture_name, circuit_size, filename, max_size=None, brute_force='true'):

    architecture = arch.architecture[architecture_name]()
    circuit_size = int(circuit_size)
    brute_force = brute_force.strip().lower() == 'true'

    if max_size is None:
        max_size = circuit_size
    else:
        max_size = int(max_size)

    # Count all non-isomorphic, optimal as well as brute force solution
    def totarch(sz):
        def fun():
            return alg.count_size_k_induced_connected_subgraphs_tree(architecture, sz)
        return fun

    def nonisoarch(sz):
        def fun():
            return alg.size_k_induced_connected_subgraphs_ram(architecture, sz)
        return fun

    def optarch(sz):
        def fun():
            return alg.size_k_optimal_subgraphs_slow(architecture, sz)
        return fun

    def bftotarch(sz):
        def fun():
            return alg.count_size_k_induced_connected_subgraphs_bf(architecture, sz)
        return fun


    measurements = []

    for cz in range(circuit_size, max_size+1):
        print(f"Counting subarchitectures on {architecture_name} with {cz} qubits")

        # Count total number of sub-architectures
        totsubarch, totsubarch_t = time_it(totarch(cz))

        print(f"Total number of subarchitectures {totsubarch} in {totsubarch_t}s")

        nonisosubarch, nonisosubarch_t = time_it(nonisoarch(cz))

        print(f"Non-isomorphic subarchitectures {len(nonisosubarch)} in {nonisosubarch_t}s")

        optsubarch, optsubarch_t = time_it(optarch(cz))

        print(f"Optimal sub-architectures {len(optsubarch)} in {optsubarch_t}s")


        if brute_force:
            bftotsubarch, bftotsubarch_t = time_it(bftotarch(cz))
        else:
            bftotsubarch = 0
            bftotsubarch_t = ""

            print(f"Brute-force subarch in {bftotsubarch_t}s")

        # Save all measurements to list
        measurements.append([totsubarch, len(nonisosubarch), len(optsubarch), totsubarch_t, bftotsubarch_t, optsubarch_t])

    # Save all the measured data to the specified csv file
    with open(filename, "a+", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=" ")
        header = [
            "Architecture",
            "Circuit size",
            "Total subarchitectures",
            "Non-isomorphic subarchitectures",
            "Optimal sub-architectures",
            "Connected Subgraphs Tree-compute (s)",
            "Connected Subgraphs BruteForce-compute (s)",
            "Optimal Subarchitectures compute (s)"
        ]
        writer.writerow(header)

        # Write resutls
        results = []
        for cz in range(circuit_size, max_size + 1):
            results.append([
                architecture_name,
                cz,
            ] + measurements[cz - circuit_size])
        writer.writerows(results)


# Main function to launch experiments
def main():
    import sys

    if len(sys.argv) == 1:
        print("Please specify at least 1 command-line argument")
        sys.exit(0)

    # Extract arguments
    pg = sys.argv[1]
    args = sys.argv[2:]

    # Match based on program name
    if pg == "subarchcount":
        count_subarch(*args)
    if pg == "randomcircuit":
        opt_random(*args)
    if pg == "fixedcircuit":
        opt_qasm(*args)
    if pg == "qsynth":
        q_synth(*args)


if __name__ == "__main__":
    main()
