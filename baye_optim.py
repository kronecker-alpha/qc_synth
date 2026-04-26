"""
Performs Bayesian Optimisation on the hyperparameters of the genetic program using Optuna.
"""
############PARAMETERS

TARGET_EVALS = 10000
N_TRIALS = 5

############
import optuna
from tqdm import tqdm
from ga_runner import run_ga
from parameters import no_qu, gate_set

  
def objective(trial):

    config = { #hyperparameter value ranges
        "pop_size": trial.suggest_int("pop_size", 50, 500),
        "mutation_rate": trial.suggest_float("mutation_rate", 0.001, 0.05),
        "selection_pressure": trial.suggest_int("selection_pressure", 2, 20),
        "elitism": trial.suggest_float("elitism", 0.02, 0.2),
    }

    iterations = int(TARGET_EVALS / config["pop_size"]) #ensure consistant computational useage

    fitness = run_ga(
        config=config,
        iterations=iterations,
        no_qu=no_qu,
        gate_set=gate_set,
        trial=trial
    )

    return fitness

sampler = optuna.samplers.TPESampler() #using bayesian optimisation

#Optuna study
study = optuna.create_study(
    direction="maximize", #maximise the fitness
    sampler=sampler
)

with tqdm(total=N_TRIALS) as pbar: 
    def callback(study, trial): #needed to force update the progress bar
        pbar.update(1)
    study.optimize(objective, n_trials=N_TRIALS, callbacks=[callback])

#print results
print(f"\nBest parameters: {study.best_params}")
print(f"\nBest fitness: {study.best_value}")