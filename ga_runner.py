"""
Runs a single genetic algorithm instance.
"""
import heapq
from population import tournament, crossover
from individual import Individual
import optuna

def run_ga(config, iterations, no_qu, gate_set, trial=None, display=None):

    pop_size = config["pop_size"]
    mutation_rate = config["mutation_rate"]
    selection_pressure = config["selection_pressure"]
    elitism = config["elitism"]

    Individual.set_class_vars(no_qu, gate_set, mutation_rate)

    pop = [Individual() for _ in range(pop_size)]

    best_fitness = 0

    for gen in range(iterations):

        # evaluate fitness
        for sol in pop:
            sol.calc_fitness()

        best = max(pop, key=lambda ind: ind.fitness)
        best_fitness = max(best_fitness, best.fitness)

        fitnesses = [ind.fitness for ind in pop]
        avg_fitness = sum(fitnesses) / len(fitnesses)
        worst_fitness = min(fitnesses)

        # report intermediate value for pruning
        if trial is not None:
            trial.report(best_fitness, gen)

            if trial.should_prune():
                raise optuna.exceptions.TrialPruned()

        # GUI display (optional)
        if display:
            from qiskit.quantum_info import Statevector

            best.gen_qiskit()
            state = Statevector.from_instruction(best.qis)
            display.update_display(gen + 1, best.qis, state.data, best.fitness, avg_fitness, worst_fitness)

        # elitism
        elites = int(((pop_size * elitism) // 2) * 2)
        top = heapq.nlargest(elites, pop, key=lambda ind: ind.fitness)

        # crossover
        children = []
        for _ in range(0, pop_size - elites):
            par1 = tournament(pop, selection_pressure)
            par2 = tournament(pop, selection_pressure)

            ch1, ch2 = crossover(par1.chromosome, par2.chromosome)
            children.append(ch1)
            children.append(ch2)

        pop = [Individual(child) for child in children]

        # mutation
        for sol in pop:
            sol.mutate()

        pop = pop + top

    return best_fitness