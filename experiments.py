"""
Performs grid search on the gate sets and target states defined in circuits.py with fixed hyperparameters
"""

############PARAMETERS

TARGET_EVALS = 1000
N_TRIALS = 5

#############
from circuits import *
import optuna
from tqdm import tqdm
from ga_runner import run_ga
from parameters import pop_size, mutation_rate, selection_pressure, elitism


def objective(trial):
    rng = np.random.default_rng(trial.number) #sets rng

    #target and gate set options
    target_name = trial.suggest_categorical("target",   list(TARGET_OPTIONS.keys()))
    gate_set_name = trial.suggest_categorical("gate_set", list(GATE_SET_OPTIONS.keys()))

    chosen_no_qu, target_state = TARGET_OPTIONS[target_name] #fetches value from key
    chosen_gate_set = GATE_SET_OPTIONS[gate_set_name]

    config = { #from parameters.py
        "pop_size":           pop_size,
        "mutation_rate":      mutation_rate,
        "selection_pressure": selection_pressure,
        "elitism":            elitism,
    }

    iterations = int(TARGET_EVALS / config["pop_size"])

    fitness = run_ga(
        config=config,
        iterations=iterations,
        no_qu=chosen_no_qu,
        gate_set=chosen_gate_set,
        trial=trial,
        target2 = target_state,
        rng = rng
    )

    return fitness

search_space = {
    "target": list(TARGET_OPTIONS.keys()),
    "gate_set": list(GATE_SET_OPTIONS.keys()),
}

sampler = optuna.samplers.GridSampler(search_space)

study = optuna.create_study(
    direction="maximize",
    sampler=sampler
)

total_trials = len(search_space["target"]) * len(search_space["gate_set"])

with tqdm(total=total_trials) as pbar:
    def callback(study, trial):
        pbar.update(1)

    study.optimize(objective, callbacks=[callback])
    
#print results
print(f"\nBest parameters: {study.best_params}")
print(f"\nBest fitness: {study.best_value}")