# qc_synth

A genetic algorithm (GA) framework for quantum circuit synthesis. Given a target quantum state, `qc_synth` evolves a population of candidate circuits — represented as variable-length chromosomes of quantum gates — to maximise state fidelity against the target.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Running with GUI](#running-with-gui)
  - [Running without GUI](#running-without-gui)
  - [Bayesian Hyperparameter Optimisation](#bayesian-hyperparameter-optimisation)
  - [Analysing Results](#analysing-results)
- [Configuration](#configuration)
  - [GA Parameters](#ga-parameters)
  - [Gate Sets](#gate-sets)
  - [Target States](#target-states)
- [Algorithm Details](#algorithm-details)
- [Output Format](#output-format)
- [Testing](#testing)

---

## Overview

`qc_synth` frames quantum circuit synthesis as an optimisation problem. Each individual in the population encodes a quantum circuit as an ordered list of gates (a chromosome). Fitness is defined as state fidelity minus a gate-count penalty, which biases the search towards shorter circuits that still achieve high fidelity.

The framework supports:

- Configurable gate sets, including single-qubit, two-qubit, three-qubit, and parametric gates.
- Multiple target states: Bell states, GHZ states, and W states.
- Optional real-time visualisation of the best circuit and fitness trajectory via a PySide6 GUI.
- Bayesian hyperparameter optimisation via Optuna to tune GA parameters or circuit configurations.

---

## Project Structure

```
qc_synth/
│
├── main.py            # Entry point; launches the GA with the GUI
├── ga_runner.py       # Core GA loop; runs a single GA instance
├── individual.py      # Individual class: chromosome structure, mutation, fitness
├── population.py      # Population-level operators: tournament selection, crossover
├── circuits.py        # Gate method registry and target state definitions
├── parameters.py      # Central configuration file
├── baye_optim.py      # Bayesian optimisation over GA/circuit hyperparameters
├── metrics.py         # Post-hoc analysis of saved results
├── gui.py             # PySide6 real-time display widget
├── unit_tests.py      # Unit tests
└── results/           # JSON output files (created at runtime)
```

---

## Installation

Python 3.10+ is recommended.

```bash
pip install qiskit qiskit-aer numpy optuna tqdm PySide6 matplotlib
```

---

## Usage

### Running with GUI

```bash
python main.py
```

This launches a window showing the best circuit (as a Qiskit circuit diagram), the statevector, and a live fitness plot for the best, average, and worst individuals.

### Running without GUI

Call `run_ga` directly from `ga_runner.py`:

```python
from ga_runner import run_ga
from parameters import pop_size, mutation_rate, selection_pressure, elitism, no_qu, gate_set

config = {
    "pop_size": pop_size,
    "mutation_rate": mutation_rate,
    "selection_pressure": selection_pressure,
    "elitism": elitism,
}

best_fitness = run_ga(
    config=config,
    iterations=250,
    no_qu=no_qu,
    gate_set=gate_set,
)
print(f"Best fitness: {best_fitness:.6f}")
```

Results are written to `results/{no_qu}_{gate_set}_{target}.json`.

### Bayesian Hyperparameter Optimisation

```bash
python baye_optim.py
```

Set `CIRCUIT = False` in `baye_optim.py` to optimise GA hyperparameters (`pop_size`, `mutation_rate`, `selection_pressure`, `elitism`). Set `CIRCUIT = True` to instead search over target states and gate sets with fixed hyperparameters.

The number of trials is controlled by `N_TRIALS` and the total evaluation budget by `TARGET_EVALS`.

### Analysing Results

```bash
python metrics.py
```

Edit the `root` path in `metrics.py` to point to your `results/` directory. For each saved run, the script reports:

- Final fidelity and fitness
- Circuit depth and gate count
- Generations required to reach 90% of final fitness
- Wall-clock runtime

---

## Configuration

All primary parameters are set in `parameters.py`.

### GA Parameters

| Parameter              | Description                                                      | Default   |
| ---------------------- | ---------------------------------------------------------------- | --------- |
| `pop_size`           | Number of individuals in the population                          | `400`   |
| `mutation_rate`      | Per-gene mutation probability                                    | `0.001` |
| `selection_pressure` | Tournament size (number of candidates compared per selection)    | `10`    |
| `elitism`            | Fraction of the population preserved as elites each generation   | `0.01`  |
| `iterations`         | Number of generations (derived from `TARGET_EVALS / pop_size`) | —        |

### Gate Sets

The gate registry in `circuits.py` contains all supported gates. Specify the active gate set as a list of keys in `parameters.py`:

```python
gate_set = ['H', 'CX', 'T', 'P']
```

Predefined named sets are available in `baye_optim.py`:

| Name           | Gates                                                              |
| -------------- | ------------------------------------------------------------------ |
| `minimal`    | `H`, `CX`                                                      |
| `clifford`   | `H`, `X`, `Y`, `Z`, `S`, `T`, `CX`, `CZ`, `SWAP` |
| `parametric` | `H`, `X`, `RX`, `RY`, `RZ`, `CX`, `CRX`, `CRY`     |
| `full`       | All gates in `gate_methods`                                      |

### Target States

Target states are defined in `circuits.py` and set in `parameters.py`:

```python
import circuits
target = circuits.bell_state  # or ghz_state, w_state
```

| Function       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| `bell_state` | 2-qubit Bell state (Φ⁺ by default)                       |
| `ghz_state`  | n-qubit GHZ state: `(                                      |
| `w_state`    | n-qubit W state: equal superposition of single-excitations |

---

## Algorithm Details

**Representation:** Each chromosome is a variable-length list of genes. Each gene is a 5-element list `[gate_name, qubit_1, qubit_2, qubit_3, parameter]`. Unused fields (e.g. the parameter for a non-parametric gate) are carried but ignored during circuit construction.

**Fitness:** `fitness = state_fidelity(output_state, target_state) − 0.01 × gate_count`

**Selection:** Tournament selection with configurable tournament size.

**Crossover:** Single-point crossover on two parent chromosomes, producing two children.

**Mutation:** Per-gene stochastic mutation. Depending on the gene index:

- Gate type: replaced with a randomly sampled gate from the gate set.
- Qubit indices: reassigned to a valid (distinct) qubit.
- Parameter: perturbed by Gaussian noise (`σ = 0.3`), modulo `2π`.

**Elitism:** The top `elitism × pop_size` individuals are copied directly to the next generation without modification.

---

## Output Format

Each run writes a JSON file to `results/` with the following schema:

```json
{
  "generations": [
    {
      "generation": 0,
      "best_fitness": 0.85,
      "worst_fitness": 0.12,
      "average_fitness": 0.45
    }
  ],
  "time": 12.34,
  "circuit": [["H", 0, 1, 2, 1.57], ["CX", 0, 1, 2, 0.0]],
  "ffidelity": 0.998
}
```

---

## Testing

```bash
python -m pytest unit_tests.py -v
```

Tests cover state vector correctness, individual initialisation and mutation, crossover validity, tournament selection, and a smoke-test of the full GA loop.
