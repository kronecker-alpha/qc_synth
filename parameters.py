"""
File where parameters are stored and can be edited.
"""

#MAIN
pop_size = 200
iterations = 300
mutation_rate = 0.01
selection_pressure = 10
elitism = 0.1


#OPERATORS
#chose which mutation or crossover operators to use?


#GATES/CIRCUIT
no_qu = 5
gate_set = ['H', 'CX','T','P']

import circuits
target = circuits.w_state


