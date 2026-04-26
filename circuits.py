"""
Contains the circuits to synthesise and gate to use.
"""

import numpy as np
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Operator

gate_methods = {
    # Single-qubit gates
    'H': lambda qc, qb1, qb2, qb3, p: qc.h(qb1),
    'X': lambda qc, qb1, qb2, qb3, p: qc.x(qb1),
    'Y': lambda qc, qb1, qb2, qb3, p: qc.y(qb1),
    'Z': lambda qc, qb1, qb2, qb3, p: qc.z(qb1),
    'S': lambda qc, qb1, qb2, qb3, p: qc.s(qb1),
    'T': lambda qc, qb1, qb2, qb3, p: qc.t(qb1),
    'SX': lambda qc, qb1, qb2, qb3, p: qc.sx(qb1),

    # Parametric single-qubit gates
    'RX': lambda qc, qb1, qb2, qb3, p: qc.rx(p, qb1),
    'RY': lambda qc, qb1, qb2, qb3, p: qc.ry(p, qb1),
    'RZ': lambda qc, qb1, qb2, qb3, p: qc.rz(p, qb1),

    # Two-qubit gates (renamed)
    'CNOT': lambda qc, qb1, qb2, qb3, p: qc.cx(qb1, qb2),
    'SWAP': lambda qc, qb1, qb2, qb3, p: qc.swap(qb1, qb2),

    # Three-qubit gates (renamed)
    'CCNOT': lambda qc, qb1, qb2, qb3, p: qc.ccx(qb1, qb2, qb3),
}

def bell_state(n_qubits=2, bell_type='phi_plus'):
    """
    Returns the target Bell state as a statevector.
    """
    dim = 2**n_qubits
    state = np.zeros(dim, dtype=complex)
    
    if bell_type == 'phi_plus':
        state[0] = 1 / np.sqrt(2)           
        state[-1] = 1 / np.sqrt(2)

    return state

def ghz_state(n_qubits=2):
    """
    Returns the GHZ (Greenberger-Horne-Zeilinger) state for n qubits.
    |GHZ⟩ = (|00...0⟩ + |11...1⟩) / √2
    """
    dim = 2**n_qubits
    state = np.zeros(dim, dtype=complex)
    state[0] = 1 / np.sqrt(2)
    state[-1] = 1 / np.sqrt(2)
    return state

def w_state(n_qubits=3):
    """
    Returns the n-qubit W state.
    W state: (|100...0⟩ + |010...0⟩ + ... + |00...01⟩) / √n
    """
    dim = 2**n_qubits
    state = np.zeros(dim, dtype=complex)
    normalization = 1 / np.sqrt(n_qubits)
    
    for i in range(n_qubits):
        # Set bit at position i (counting from right)
        index = 2**(n_qubits - 1 - i)
        state[index] = normalization
    
    return state


def qft_unitary(n_qubits=3):
    return Operator(QFT(num_qubits=n_qubits)).data

def cluster_state_1d(n_qubits=3):
    """
    Returns a 1D cluster state on n qubits.
    Constructed by applying CZ gates between neighbours on |+>^n.
    """
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    qc = QuantumCircuit(n_qubits)
    
    # Prepare |+>^n
    for i in range(n_qubits):
        qc.h(i)
    
    # Apply CZ between neighbours
    for i in range(n_qubits - 1):
        qc.cz(i, i + 1)
    
    return Statevector.from_instruction(qc).data

def haar_random_state(n_qubits=3, seed=None):
    """
    Returns a Haar-random statevector.
    """
    import numpy as np

    rng = np.random.default_rng(seed)
    dim = 2**n_qubits
    
    real = rng.normal(size=dim)
    imag = rng.normal(size=dim)
    state = real + 1j * imag
    
    # Normalize
    state /= np.linalg.norm(state)
    
    return state

def grover_diffusion_unitary(n_qubits=3):
    """
    Returns the Grover diffusion operator:
    D = 2|s><s| - I
    where |s> is the uniform superposition state.
    """
    import numpy as np

    dim = 2**n_qubits
    s = np.ones(dim, dtype=complex) / np.sqrt(dim)
    
    return 2 * np.outer(s, np.conjugate(s)) - np.eye(dim)

def ripple_carry_adder_unitary(n_qubits=3):
    """
    Returns a 3-qubit ripple-carry style adder (toy example).
    Adds qubit 0 and 1 into qubit 2 (mod 2 with carry-like structure).
    """

    if n_qubits != 3:
        raise ValueError("n_qubits must be == 3")
    
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator

    qc = QuantumCircuit(3)
    
    # Simple reversible logic (not full adder, but structured non-Clifford)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.ccx(0, 1, 2)
    
    return Operator(qc).data

def diagonal_phase_unitary(n_qubits=3, theta=np.pi/4):
    """
    Returns a diagonal unitary with phases depending on basis index.
    U = diag(exp(i * theta * k)) for k in [0, ..., 2^n - 1]
    """
    import numpy as np

    dim = 2**n_qubits
    phases = np.exp(1j * theta * np.arange(dim))
    
    return np.diag(phases)