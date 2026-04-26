"""
File where parameters are stored and can be edited.
"""
import circuits


#MAIN
pop_size = 1000
mutation_rate = 0.03
selection_pressure = 3
elitism = 0.005
iterations = 100000/pop_size #tune so experiments are an appropriate length


#GATES
gate_set = ["H", "S", "T", "CNOT"]


#TARGET
no_qu = 3 #determines size of target
target = circuits.w_state


