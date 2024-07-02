# Generates a random quantum circuit consisting of selected gates
# code copied from:
# https://github.com/Qiskit/qiskit/blob/stable/0.14/qiskit/circuit/random/utils.py#
def random_circuit(
    num_qubits,
    depth,
    seed=None,
):
    import numpy as np
    from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
    from qiskit.circuit import Reset
    from qiskit.circuit.library.standard_gates import (
        IGate,
        U1Gate,
        U2Gate,
        U3Gate,
        XGate,
        YGate,
        ZGate,
        HGate,
        SGate,
        SdgGate,
        TGate,
        TdgGate,
        RXGate,
        RYGate,
        RZGate,
        CXGate,
        CYGate,
        CZGate,
        CHGate,
        CRZGate,
        CU1Gate,
        CU3Gate,
        SwapGate,
        RZZGate,
        CCXGate,
        CSwapGate,
    )
    from qiskit.circuit.exceptions import CircuitError

    one_q_ops = [
        # IGate,
        # U1Gate,
        # U2Gate,
        U3Gate,
        # XGate,
        # YGate,
        # ZGate,
        # HGate,
        # SGate,
        # SdgGate,
        # TGate,
        # TdgGate,
        # RXGate,
        # RYGate,
        # RZGate,
    ]
    one_param = [U1Gate, RXGate, RYGate, RZGate, RZZGate, CU1Gate, CRZGate]
    two_param = [U2Gate]
    three_param = [U3Gate, CU3Gate]
    two_q_ops = [
        CXGate,
        # CYGate,
        # CZGate,
        # CHGate,
        # CRZGate,
        # CU1Gate,
        # CU3Gate,
        # SwapGate,
        # RZZGate,
    ]

    qr = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(num_qubits)

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # apply arbitrary random operations at every depth
    for _ in range(depth):

        # choose only between 1 and 2 qubit gates
        remaining_qubits = list(range(num_qubits))
        while remaining_qubits:

            max_possible_operands = min(len(remaining_qubits), 2)
            num_operands = rng.choice(range(max_possible_operands)) + 1
            rng.shuffle(remaining_qubits)
            operands = remaining_qubits[:num_operands]
            remaining_qubits = [q for q in remaining_qubits if q not in operands]

            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                operation = rng.choice(two_q_ops)

            if operation in one_param:
                num_angles = 1
            elif operation in two_param:
                num_angles = 2
            elif operation in three_param:
                num_angles = 3
            else:
                num_angles = 0

            angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
            register_operands = [qr[i] for i in operands]
            op = operation(*angles)

            qc.append(op, register_operands)

    return qc
