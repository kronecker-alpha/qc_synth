"""
Contains the circuits that are synthesised and defines the gate dictionary from string to qiskit gate.
"""
import numpy as np
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

gate_methods = {
    #Single-qubit gates
    'H': lambda qc, qb1, qb2, qb3, p: qc.h(qb1),
    'X': lambda qc, qb1, qb2, qb3, p: qc.x(qb1),
    'Y': lambda qc, qb1, qb2, qb3, p: qc.y(qb1),
    'Z': lambda qc, qb1, qb2, qb3, p: qc.z(qb1),
    'S': lambda qc, qb1, qb2, qb3, p: qc.s(qb1),
    'T': lambda qc, qb1, qb2, qb3, p: qc.t(qb1),
    'SX': lambda qc, qb1, qb2, qb3, p: qc.sx(qb1),

    #Parametric gates
    'RX': lambda qc, qb1, qb2, qb3, p: qc.rx(p, qb1),
    'RY': lambda qc, qb1, qb2, qb3, p: qc.ry(p, qb1),
    'RZ': lambda qc, qb1, qb2, qb3, p: qc.rz(p, qb1),

    #Two-qubit gates 
    'CNOT': lambda qc, qb1, qb2, qb3, p: qc.cx(qb1, qb2),
    'SWAP': lambda qc, qb1, qb2, qb3, p: qc.swap(qb1, qb2),

    #Three-qubit gates
    'CCNOT': lambda qc, qb1, qb2, qb3, p: qc.ccx(qb1, qb2, qb3),
}

def bell_state(n_qubits=2, bell_type='phi_plus'):
    """
    Returns Bell state as a statevector.
    """
    dim = 2**n_qubits
    state = np.zeros(dim, dtype=complex)
    
    if bell_type == 'phi_plus':
        state[0] = 1 / np.sqrt(2)           
        state[-1] = 1 / np.sqrt(2)

    return state

def ghz_state(n_qubits=2):
    """
    Returns the GHZ state as a statevector.
    """
    dim = 2**n_qubits
    state = np.zeros(dim, dtype=complex)
    state[0] = 1 / np.sqrt(2)
    state[-1] = 1 / np.sqrt(2)
    return state

def w_state(n_qubits=3):
    """
    Returns the W state as a statevector.
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
    "Returns the GFT unitary."
    return Operator(QFT(num_qubits=n_qubits)).data

def cluster_state_1d(n_qubits=3):
    """
    Returns a 1D cluster state as a statevector.
    """
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
    Returns the Grover diffusion operator.
    """
    import numpy as np

    dim = 2**n_qubits
    s = np.ones(dim, dtype=complex) / np.sqrt(dim)
    
    return 2 * np.outer(s, np.conjugate(s)) - np.eye(dim)

def ripple_carry_adder_unitary(n_qubits=3):
    """
    Returns a ripple-carry style adder.
    """
    if n_qubits != 3:
        raise ValueError("n_qubits must be == 3")
    
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator

    qc = QuantumCircuit(3)
    
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.ccx(0, 1, 2)
    
    return Operator(qc).data

def diagonal_phase_unitary(n_qubits=3, theta=np.pi/4):
    """
    Returns a diagonal unitary.
    """
    import numpy as np

    dim = 2**n_qubits
    phases = np.exp(1j * theta * np.arange(dim))
    
    return np.diag(phases)


TARGET_OPTIONS: dict[str, tuple[int, object]] = {
    "bell_phi_plus_3q": (3, bell_state(n_qubits=3, bell_type="phi_plus")),
    "ghz_3q":           (3, ghz_state(n_qubits=3)),
    "w_3q":             (3, w_state(n_qubits=3)),

    "cluster_3q":       (3, cluster_state_1d(n_qubits=3)),
    "haar_4q":          (3, haar_random_state(n_qubits=3, seed=1)),

    "qft_3q":           (3, qft_unitary(n_qubits=3)),
    "grover_3q":        (3, grover_diffusion_unitary(n_qubits=3)),
    "adder_3q":         (3, ripple_carry_adder_unitary(n_qubits=3)),
    "diag_phase_3q":    (3, diagonal_phase_unitary(n_qubits=3)),
}

GATE_SET_OPTIONS: dict[str, list[str]] = {
    "minimal_set_1": ["H", "CCNOT"],
    "minimal_set_2": ["H", "T", "CNOT"],

    "additional_set_1": ["H", "S", "T", "CNOT"],
    "additional_set_2": ["H", "S", "T", "CNOT", "SWAP"],
    "additional_set_3": ["X", "Y", "Z", "H", "S", "T", "CNOT"],

    "minimal_parametric_set_1": ["RX", "RY", "CNOT"],
    "minimal_parametric_set_2": ["RZ", "SX", "CNOT"],  

    "additional_parametric_set": ["RX", "RY", "RZ", "CNOT"],

    "all_gates": ["H", "CCNOT", "T", "CNOT", "S", "SWAP",
        "X", "Y", "Z", "RX", "RY", "RZ", "SX"],
}