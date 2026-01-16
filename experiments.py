"""
need: (fixed no. of qubits)
gate type
target qubit
control qubit (opt)
control qubit (opt)
parameters (opt). 

extras:
fixed or var length
gates as strings i think..

ensuring validity? - make valid function? 
OR everything can have control qubit etc, just ignore when processing
three qubit gates - multiple control qubits
"""
from qiskit import QuantumCircuit
import numpy as np
rng = np.random.default_rng()

qubits = 6
gates = ['H', 'CX']
gate_methods = {'H': lambda qc, qb1, qb2, qb3, p: qc.h(qb1),
                'CX': lambda qc, qb1, qb2, qb3, p: qc.cx(qb1,qb2)} #prototype for gate to function dictionary
#pass all information in, but extra parameters just get ignored

#gen random circuit
ran_c = []
for i in range(1,rng.integers(2,12)):
    qubit_choice = [i for i in range(0,qubits)]
    [q1, q2, q3] = rng.choice(qubit_choice, 3, replace=False)
    gene = [rng.choice(gates), q1, q2, q3 ,rng.random()*np.pi ]
    ran_c.append(gene)

print(ran_c)

ran_c_q = QuantumCircuit(qubits)
for g in ran_c:
    gate_methods[g[0]](ran_c_q,g[1], g[2], g[3], g[4])

print(ran_c_q.draw())


