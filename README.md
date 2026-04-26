# GSS

A genetic program (GP) framework for quantum circuit synthesis.

### Installation

```bash
pip install qiskit qiskit-aer numpy optuna tqdm PySide6 matplotlib
```

### Running with GUI

```bash
python main.py
```

Results are written to `results/{no_qu}_{gate_set}_{target}.json`.

### Bayesian Hyperparameter Optimisation

```bash
python baye_optim.py
```

### Run gate set study

```bash
python experiments.py
```

### Analysing Results

```bash
python metrics.py
```

You will need to edit the root path to point to your results directory.

### Output Format

Each run writes a JSON file to `results/` with the following structure:

```json
{
  "generations": [
    {
      "generation": x,
      "best_fitness": x,
      "worst_fitness": x,
      "average_fitness": x
    }
  ],
  "time": x,
  "circuit": [["H", 0, 1, 2, 1.57], ["CX", 0, 1, 2, 0.0]],
  "ffidelity": x
}
```

### Testing

```bash
python -m pytest unit_tests.py -v
```
