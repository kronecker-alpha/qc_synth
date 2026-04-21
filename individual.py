"""
Code for individual solutions. Structure of the chromosome, mutation and fitness.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, state_fidelity
import numpy as np
rng = np.random.default_rng()
from circuits import bell_state, ghz_state

#PARAMETERS
from parameters import target
from circuits import gate_methods

class Individual:
    no_qu = 0
    gates = []

    def set_class_vars(no_qu,gates,mut_rate):
        """Sets class variables to match population"""
        Individual.no_qu = no_qu
        Individual.gates = gates
        Individual.mut_rate = mut_rate

    def __init__(self, chrom = None, crossover = False):
        
        if crossover == False:
            """Creates a random solution"""
            self.chromosome = []
            for _ in range(1,rng.integers(2,12)):
                qubit_choice = [i for i in range(0,Individual.no_qu)]
                try:
                    [q1, q2, q3] = rng.choice(qubit_choice, 3, replace=False)
                    gene = [rng.choice(Individual.gates), q1, q2, q3 ,rng.random()*2*np.pi ]
                except: #do nawt keep this, horrible solution #fine, just base it on gate
                    [q1, q2] = rng.choice(qubit_choice, 2, replace=False)
                    gene = [rng.choice(Individual.gates), q1, q2, None ,rng.random()*2*np.pi ]
                self.chromosome.append(gene)
        else:
            """Creates a solution from chrom, created with crossover."""
            self.chromosome = chrom

    def gen_qiskit(self):
        """Generates a Qiskit circuit from the individual's chromosome."""
        self.qis = QuantumCircuit(Individual.no_qu)
        for gene in self.chromosome:
            gate_methods[gene[0]](self.qis,gene[1], gene[2], gene[3], gene[4])

    def mutate(self):
        """Applies mutation to each gene in the chromosome."""
        for i in range(0,len(self.chromosome)):
            for j in range(0,len(self.chromosome[i])):
                if rng.random() <= self.mut_rate: #mutation rate for each gene
                    if j==0: #change gate type
                        self.chromosome[i][j] = rng.choice(Individual.gates) #set unneeded stuff to None
                    elif j==1 or j==2: #target qubit + first control
                        if self.no_qu == 2: #swap target and control
                            self.chromosome[i][1], self.chromosome[i][2] = self.chromosome[i][2], self.chromosome[i][1]
                        else:
                            valid_gates = [k for k in range(0,Individual.no_qu) if (k != self.chromosome[i][1] and k != self.chromosome[i][2])]
                            self.chromosome[i][j] = rng.choice(valid_gates)
                    elif j==3: #second control
                        if self.no_qu == 2: #or unneeded for this gate
                            pass
                        else: #don't even have a second control bit atm
                            self.chromosome[i][j] = rng.integers(0,Individual.no_qu)
                    else: #change parameter by a small amount
                        self.chromosome[i][j] = (self.chromosome[i][j] + rng.normal(0,0.3)) % (2 * np.pi)
    

    def calc_fidelity(self,target2=None):
        """Calculates fidelity."""
        self.gen_qiskit()
        U = Operator(self.qis).data
        initial_state = np.zeros(2**Individual.no_qu)
        initial_state[0] = 1.0

        output_state = np.matmul(U, initial_state)
        if target2 is not None:
            target_state = target2
        else:
            target_state = target(n_qubits=Individual.no_qu)

        return state_fidelity(output_state, target_state)

    def calc_fitness(self,target2=None):
        """calculates fitness"""
        self.gen_qiskit()
        self.fitness = self.calc_fidelity(target2=target2) - self.qis.size() * 0.01



