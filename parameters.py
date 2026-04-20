"""
File where parameters are stored and can be edited.
"""

#MAIN
pop_size = 400
mutation_rate = 0.001
selection_pressure = 10
elitism = 0.01
iterations = 100000/pop_size #tune so experiments are an appropriate length


#OPERATORS
#chose which mutation or crossover operators to use?
#no extensive trials, just a few to ensure they work okay


#GATES/CIRCUIT
no_qu = 3 #depends on target/determines size of target
gate_set = ['H', 'CX','T','P']

import circuits
target = circuits.bell_state


