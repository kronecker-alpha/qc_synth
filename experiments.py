"""
Performs Bayesian Optimisation on either target states and gate sets, or evolutionary hyperparameters.
"""

############PARAMETERS
from circuits import *

TARGET_EVALS = 1000
N_TRIALS = 5


TARGET_OPTIONS: dict[str, tuple[int, object]] = {
    "bell_phi_plus_3q": (3, bell_state(n_qubits=3, bell_type="phi_plus")),
    "ghz_3q":           (3, ghz_state(n_qubits=3)),
    "w_3q":             (3, w_state(n_qubits=3)),

    "cluster_3q":       (3, cluster_state_1d(n_qubits=3)),
    "haar_4q":          (4, haar_random_state(n_qubits=4, seed=1)),

    "qft_3q":           (3, qft_unitary(n_qubits=3)),
    "grover_3q":        (3, grover_diffusion_unitary(n_qubits=3)),
    "adder_3q":         (3, ripple_carry_adder_unitary(n_qubits=3)),
    "diag_phase_3q":    (3, diagonal_phase_unitary(n_qubits=3)),
}

GATE_SET_OPTIONS: dict[str, list[str]] = {
    "minimal_set_1": ["H", "CCNOT"],
    "minimal_set_2": ["H", "T", "CNOT"],

    "additional_set_1": ["H", "S", "T", "CNOT"],
    "additional_set_2": ["H", "S", "T", "CNOT", "SWAP"],
    "additional_set_3": ["X", "Y", "Z", "H", "S", "T", "CNOT"],

    "minimal_parametric_set_1": ["RX", "RY", "CNOT"],
    "minimal_parametric_set_2": ["RZ", "SX", "CNOT"],  

    "additional_parametric_set": ["RX", "RY", "RZ", "CNOT"],

    "all_gates": ["H", "CCNOT", "T", "CNOT", "S", "SWAP",
        "X", "Y", "Z", "RX", "RY", "RZ", "SX"],
}

###########################
import optuna
from tqdm import tqdm
from ga_runner import run_ga
from parameters import no_qu, gate_set,pop_size, mutation_rate, selection_pressure, elitism
from individual import Individual


def objective(trial):
    """Optimise target state and gate set with fixed GA hyperparameters found in parameters.py."""
    rng = np.random.default_rng(trial.number) #sets rng

    target_name = trial.suggest_categorical("target",   list(TARGET_OPTIONS.keys()))
    gate_set_name = trial.suggest_categorical("gate_set", list(GATE_SET_OPTIONS.keys()))

    chosen_no_qu, target_state = TARGET_OPTIONS[target_name]
    chosen_gate_set = GATE_SET_OPTIONS[gate_set_name]

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