"""
Main code. Run directly from here.
"""
from PySide6.QtWidgets import QApplication, QWidget
from qiskit.quantum_info import Statevector
from population import tournament, crossover
from individual import Individual
from tqdm import tqdm
import heapq
from math import floor

#PARAMETERS
from parameters import pop_size, iterations, mutation_rate, selection_pressure, no_qu, gate_set,elitism

#Initialise Population
Individual.set_class_vars(no_qu,gate_set,mutation_rate)
pop = [Individual() for _ in range(0,pop_size)]

# Create QApplication and GUI display
app = QApplication([])
from gui import GADisplay
display = GADisplay(app)

#For x iterations
for i in tqdm(range(iterations)):

    #Evaluate fitness of each individual
    for sol in pop:
            sol.calc_fitness()

    best = max(pop, key=lambda ind: ind.fitness)
    best.gen_qiskit()
    state = Statevector.from_instruction(best.qis)
    
    display.update_display(i+1, best.qis, state.data, best.fitness) # Update GUI display

    #Eltilism
    elites = int(((pop_size * elitism) // 2) * 2)
    top = heapq.nlargest(elites, pop, key=lambda ind: ind.fitness)

    #Select parents for crossover
    children = []
    for i in range(0,pop_size - elites):
        par1 = tournament(pop, selection_pressure)
        par2 = tournament(pop, selection_pressure)

        #Create children with crossover and mutation
        ch1, ch2 = crossover(par1.chromosome, par2.chromosome)
        children.append(ch1)
        children.append(ch2)

    #Replace population
    pop = [Individual(child) for child in children]

    #mutation
    for sol in pop:
            sol.mutate()

    pop = pop + top

app.exec() # Keep window open


#TO DO
#clean code
#write readme
#upload to github
#research optimisation methods e.g. grid search, reinforcement learnings
#assess how easy/complex each would be
#