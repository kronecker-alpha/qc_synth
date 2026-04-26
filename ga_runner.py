"""
Runs a single genetic algorithm instance.
"""
import heapq
from population import tournament, crossover
from individual import Individual
import optuna
import json
from parameters import target
from time import perf_counter
import numpy as np
import math
import copy

default_rng = np.random.default_rng()

def run_ga(config, iterations, no_qu, gate_set, trial=None, display=None,target2=None, rng = default_rng):
    start = perf_counter()

    pop_size = config["pop_size"]
    mutation_rate = config["mutation_rate"]
    selection_pressure = config["selection_pressure"]
    elitism = config["elitism"]

    Individual.set_class_vars(no_qu, gate_set, mutation_rate)

    pop = [Individual(rng=rng) for _ in range(pop_size)]

    best_fitness = 0
    metrics = {"generations": []}

    for gen in range(iterations):

        #evaluate fitness
        for sol in pop:
            sol.calc_fitness(target2=target2)

        #get metrics
        best = max(pop, key=lambda ind: ind.fitness)
        best_fitness = max(best_fitness, best.fitness)

        fitnesses = [ind.fitness for ind in pop]
        avg_fitness = sum(fitnesses) / len(fitnesses)
        worst_fitness = min(fitnesses)

        metrics["generations"].append({ #save metrics
            "generation": gen,
            "best_fitness": best.fitness,
            "worst_fitness": worst_fitness,
            "average_fitness": avg_fitness
        })

        #GUI display (optional)
        if display:
            from qiskit.quantum_info import Statevector

            best.gen_qiskit()
            state = Statevector.from_instruction(best.qis)
            display.update_display(gen + 1, best.qis, state.data, best.fitness, avg_fitness, worst_fitness)

        #elitism
        elites = math.ceil(pop_size * elitism) #number of circuits that are carried forward
        top = heapq.nlargest(elites, pop, key=lambda ind: ind.fitness)
        top = copy.deepcopy(top) #copy to prevent being overwritten

        #crossover
        children = []
        for _ in range(0, math.ceil(((pop_size - elites) / 2) * 0.6)):
            par1 = tournament(pop, selection_pressure, rng=rng)
            par2 = tournament(pop, selection_pressure, rng=rng)

            ch1, ch2 = crossover(par1.chromosome, par2.chromosome, rng=rng)
            children.append(ch1)
            children.append(ch2)

        #carry forward some of pop without crossover
        for _ in range(0, math.ceil(((pop_size - elites) / 2) * 0.4)):
            c1 = tournament(pop, selection_pressure, rng=rng)
            c2 = tournament(pop, selection_pressure, rng=rng)
            children.append(copy.deepcopy(c1.chromosome))
            children.append(copy.deepcopy(c2.chromosome))

        pop = [Individual(chrom=child, crossover=True) for child in children]

        #mutation
        for sol in pop:
            sol.mutate(rng=rng)

        pop = pop + top #add back elitism

    end = perf_counter()

    #metric calculations
    metrics["time"] = end - start
    metrics["circuit"] = [ #needs converting from np for json
        [str(x) if isinstance(x, np.str_) else
        int(x) if isinstance(x, np.integer) else
        float(x) if isinstance(x, np.floating) else x
        for x in row]
        for row in best.chromosome
    ]
    metrics["ffidelity"] = best.calc_fidelity()

    print(best.chromosome)

    with open(fr"results/{no_qu}_{gate_set}_{target}.json","w") as f:
        json.dump(metrics, f)

    return best_fitness #for optimisation