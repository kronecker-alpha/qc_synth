"""
Contains the circuits to synthesise and gate to use.
"""

import numpy as np

gate_methods = {
    # Single-qubit gates
    'H': lambda qc, qb1, qb2, qb3, p: qc.h(qb1),
    'X': lambda qc, qb1, qb2, qb3, p: qc.x(qb1),
    'Y': lambda qc, qb1, qb2, qb3, p: qc.y(qb1),
    'Z': lambda qc, qb1, qb2, qb3, p: qc.z(qb1),
    'S': lambda qc, qb1, qb2, qb3, p: qc.s(qb1),
    'SDG': lambda qc, qb1, qb2, qb3, p: qc.sdg(qb1),
    'T': lambda qc, qb1, qb2, qb3, p: qc.t(qb1),
    'TDG': lambda qc, qb1, qb2, qb3, p: qc.tdg(qb1),
    'SX': lambda qc, qb1, qb2, qb3, p: qc.sx(qb1),
    'SXDG': lambda qc, qb1, qb2, qb3, p: qc.sxdg(qb1),
    'I': lambda qc, qb1, qb2, qb3, p: qc.id(qb1),
    
    # Parametric single-qubit gates
    'RX': lambda qc, qb1, qb2, qb3, p: qc.rx(p, qb1),
    'RY': lambda qc, qb1, qb2, qb3, p: qc.ry(p, qb1),
    'RZ': lambda qc, qb1, qb2, qb3, p: qc.rz(p, qb1),
    'P': lambda qc, qb1, qb2, qb3, p: qc.p(p, qb1),
    
    # Two-qubit gates
    'CX': lambda qc, qb1, qb2, qb3, p: qc.cx(qb1, qb2),
    'CY': lambda qc, qb1, qb2, qb3, p: qc.cy(qb1, qb2),
    'CZ': lambda qc, qb1, qb2, qb3, p: qc.cz(qb1, qb2),
    'CH': lambda qc, qb1, qb2, qb3, p: qc.ch(qb1, qb2),
    'SWAP': lambda qc, qb1, qb2, qb3, p: qc.swap(qb1, qb2),
    'ISWAP': lambda qc, qb1, qb2, qb3, p: qc.iswap(qb1, qb2),
    'ECR': lambda qc, qb1, qb2, qb3, p: qc.ecr(qb1, qb2),
    'DCX': lambda qc, qb1, qb2, qb3, p: qc.dcx(qb1, qb2),
    
    # Parametric two-qubit gates
    'CRX': lambda qc, qb1, qb2, qb3, p: qc.crx(p, qb1, qb2),
    'CRY': lambda qc, qb1, qb2, qb3, p: qc.cry(p, qb1, qb2),
    'CRZ': lambda qc, qb1, qb2, qb3, p: qc.crz(p, qb1, qb2),
    'CP': lambda qc, qb1, qb2, qb3, p: qc.cp(p, qb1, qb2),
    'RXX': lambda qc, qb1, qb2, qb3, p: qc.rxx(p, qb1, qb2),
    'RYY': lambda qc, qb1, qb2, qb3, p: qc.ryy(p, qb1, qb2),
    'RZZ': lambda qc, qb1, qb2, qb3, p: qc.rzz(p, qb1, qb2),
    'RZX': lambda qc, qb1, qb2, qb3, p: qc.rzx(p, qb1, qb2),
    #'XX_MINUS_YY': lambda qc, qb1, qb2, qb3, p: qc.xx_minus_yy(p[0], p[1], qb1, qb2),
    #'XX_PLUS_YY': lambda qc, qb1, qb2, qb3, p: qc.xx_plus_yy(p[0], p[1], qb1, qb2),
    
    # Three-qubit gates
    'CCX': lambda qc, qb1, qb2, qb3, p: qc.ccx(qb1, qb2, qb3),
    'CSWAP': lambda qc, qb1, qb2, qb3, p: qc.cswap(qb1, qb2, qb3),
    'CCZ': lambda qc, qb1, qb2, qb3, p: qc.ccz(qb1, qb2, qb3),
    'RCCX': lambda qc, qb1, qb2, qb3, p: qc.rccx(qb1, qb2, qb3),
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