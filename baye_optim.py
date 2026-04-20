"""
Performs Bayesian Optimisation on the evolution parameters.
"""
import optuna
from tqdm import tqdm
from ga_runner import run_ga
from parameters import no_qu, gate_set,pop_size, mutation_rate, selection_pressure, elitism

from circuits import gate_methods, bell_state, ghz_state, w_state
from individual import Individual

TARGET_OPTIONS: dict[str, tuple[int, object]] = {
    "bell_phi_plus_2q": (2, bell_state(n_qubits=2, bell_type="phi_plus")),
    "ghz_2q":           (2, ghz_state(n_qubits=2)),
    "ghz_3q":           (3, ghz_state(n_qubits=3)),
    "w_3q":             (3, w_state(n_qubits=3)),
}
 
GATE_SET_OPTIONS: dict[str, list[str]] = {
    "minimal":    ["H", "CX"],
    "clifford":   ["H", "X", "Y", "Z", "S", "T", "CX", "CZ", "SWAP"],
    "parametric": ["H", "X", "RX", "RY", "RZ", "CX", "CRX", "CRY"],
    "full":       list(gate_methods.keys()),
}

TARGET_EVALS = 1000
N_TRIALS = 50

CIRCUIT = False

if CIRCUIT:
    def objective(trial):
        """Optimise target state and gate set with fixed GA hyperparameters."""
        target_name    = trial.suggest_categorical("target",   list(TARGET_OPTIONS.keys()))
        gate_set_name  = trial.suggest_categorical("gate_set", list(GATE_SET_OPTIONS.keys()))
    
        chosen_no_qu, target_state = TARGET_OPTIONS[target_name]
        chosen_gate_set             = GATE_SET_OPTIONS[gate_set_name]
    
        Individual.target = target_state #means nothing
    
        config = {
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
        )
    
        return fitness
else:    
    def objective(trial):

        config = {
            "pop_size": trial.suggest_int("pop_size", 50, 500),
            "mutation_rate": trial.suggest_float("mutation_rate", 0.001, 0.05),
            "selection_pressure": trial.suggest_int("selection_pressure", 2, 20),
            "elitism": trial.suggest_float("elitism", 0.02, 0.3),
        }

        iterations = int(TARGET_EVALS / config["pop_size"])

        fitness = run_ga(
            config=config,
            iterations=iterations,
            no_qu=no_qu,
            gate_set=gate_set,
            trial=trial
        )

        return fitness


# Optuna study with pruning
study = optuna.create_study(
    direction="maximize",
    pruner=optuna.pruners.MedianPruner(
        n_startup_trials=5,
        n_warmup_steps=50
    )
)

with tqdm(total=N_TRIALS, desc="Bayesian optimisation") as pbar:

    def callback(study, trial):
        pbar.set_postfix(best=study.best_value)
        pbar.update(1)

    study.optimize(objective, n_trials=N_TRIALS, callbacks=[callback])


print("\nBest parameters:")
print(study.best_params)

print("\nBest fitness:")
print(study.best_value)