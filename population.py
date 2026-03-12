"""
Functions for editing the entire population.
"""

from individual import Individual
import numpy as np
rng = np.random.default_rng()


def tournament(pop, selection_pressure):
    bestfit = -1
    bestsol = None
    #compares s random solutions, returns solution with the best fitness
    for _ in range(selection_pressure):
        i = rng.integers(0, len(pop)) #chooses random index to pick solution
        cand = pop[i]
        fit = cand.fitness
        if fit >= bestfit: #records solution currently the tournament winner 
            bestfit = fit
            bestsol = cand
    return bestsol

def crossover(par1, par2): #two chromosomes as inputs
        """Peforms single point crossover."""
        min_len = min(len(par1), len(par2))
        crossover_point = rng.integers(1, max(2, min_len))

        c1 = par1[:crossover_point] + par2[crossover_point:]
        c2 = par2[:crossover_point] + par1[crossover_point:]

        return c1, c2 #returns the chromosome



