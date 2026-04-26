"""
Functions for editing the entire population.
"""

from individual import Individual
import numpy as np
default_rng = np.random.default_rng()
import copy


def tournament(pop, selection_pressure, rng=default_rng):
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

def crossover(par1, par2, rng=default_rng):
    """Segment-based crossover for variable-length quantum circuits."""

    if len(par1) < 2 or len(par2) < 2:
        return copy.deepcopy(par1), copy.deepcopy(par2)

    # independent cut points
    cut1 = rng.integers(1, len(par1))
    cut2 = rng.integers(1, len(par2))

    # build offspring
    child1 = par1[:cut1] + par2[cut2:]
    child2 = par2[:cut2] + par1[cut1:]

    return child1, child2



