"""
Unit tests for qc_synth.
Run with: 
python -m pytest unit_tests.py -v
"""
#lots fail as i've removed some unneeded gates from circuits.py

import numpy as np
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# circuits.py
# ---------------------------------------------------------------------------

class TestBellState:
    def test_shape(self):
        from circuits import bell_state
        state = bell_state(n_qubits=2)
        assert state.shape == (4,)

    def test_normalised(self):
        from circuits import bell_state
        state = bell_state(n_qubits=2)
        assert pytest.approx(np.linalg.norm(state) ** 2, abs=1e-9) == 1.0

    def test_phi_plus_amplitudes(self):
        from circuits import bell_state
        state = bell_state(n_qubits=2, bell_type="phi_plus")
        expected_amplitude = 1 / np.sqrt(2)
        assert pytest.approx(state[0], abs=1e-9) == expected_amplitude
        assert pytest.approx(state[-1], abs=1e-9) == expected_amplitude
        assert pytest.approx(state[1], abs=1e-9) == 0.0
        assert pytest.approx(state[2], abs=1e-9) == 0.0


class TestGHZState:
    @pytest.mark.parametrize("n_qubits", [2, 3, 4])
    def test_shape(self, n_qubits):
        from circuits import ghz_state
        state = ghz_state(n_qubits=n_qubits)
        assert state.shape == (2**n_qubits,)

    @pytest.mark.parametrize("n_qubits", [2, 3, 4])
    def test_normalised(self, n_qubits):
        from circuits import ghz_state
        state = ghz_state(n_qubits=n_qubits)
        assert pytest.approx(np.linalg.norm(state) ** 2, abs=1e-9) == 1.0

    @pytest.mark.parametrize("n_qubits", [2, 3, 4])
    def test_only_first_and_last_nonzero(self, n_qubits):
        from circuits import ghz_state
        state = ghz_state(n_qubits=n_qubits)
        expected_amplitude = 1 / np.sqrt(2)
        assert pytest.approx(abs(state[0]), abs=1e-9) == expected_amplitude
        assert pytest.approx(abs(state[-1]), abs=1e-9) == expected_amplitude
        assert np.all(state[1:-1] == 0.0)


class TestWState:
    @pytest.mark.parametrize("n_qubits", [2, 3, 4])
    def test_shape(self, n_qubits):
        from circuits import w_state
        state = w_state(n_qubits=n_qubits)
        assert state.shape == (2**n_qubits,)

    @pytest.mark.parametrize("n_qubits", [2, 3, 4])
    def test_normalised(self, n_qubits):
        from circuits import w_state
        state = w_state(n_qubits=n_qubits)
        assert pytest.approx(np.linalg.norm(state) ** 2, abs=1e-9) == 1.0

    @pytest.mark.parametrize("n_qubits", [3, 4])
    def test_exactly_n_nonzero_amplitudes(self, n_qubits):
        from circuits import w_state
        state = w_state(n_qubits=n_qubits)
        nonzero = np.count_nonzero(state)
        assert nonzero == n_qubits

    @pytest.mark.parametrize("n_qubits", [3, 4])
    def test_equal_amplitudes(self, n_qubits):
        from circuits import w_state
        state = w_state(n_qubits=n_qubits)
        nonzero_vals = state[np.nonzero(state)]
        expected = 1 / np.sqrt(n_qubits)
        assert np.allclose(np.abs(nonzero_vals), expected)


class TestGateMethods:
    def test_all_gates_callable(self):
        from circuits import gate_methods
        assert len(gate_methods) > 0
        for name, fn in gate_methods.items():
            assert callable(fn), f"Gate '{name}' is not callable."

    def test_single_qubit_gate_h(self):
        """H gate should execute without error on a valid circuit."""
        from circuits import gate_methods
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(2)
        gate_methods["H"](qc, 0, 1, None, 0.0)
        assert qc.size() == 1

    def test_two_qubit_gate_cx(self):
        from circuits import gate_methods
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(2)
        gate_methods["CX"](qc, 0, 1, None, 0.0)
        assert qc.size() == 1

    def test_parametric_gate_rx(self):
        from circuits import gate_methods
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(2)
        gate_methods["RX"](qc, 0, 1, None, np.pi / 2)
        assert qc.size() == 1


# ---------------------------------------------------------------------------
# individual.py
# ---------------------------------------------------------------------------

def _setup_individual(no_qu=3, gates=None, mut_rate=0.01):
    """Helper: configure Individual class variables before each test."""
    from individual import Individual
    if gates is None:
        gates = ["H", "CX", "T"]
    Individual.set_class_vars(no_qu, gates, mut_rate)
    return Individual


class TestIndividualInit:
    def test_random_chromosome_not_empty(self):
        Individual = _setup_individual()
        ind = Individual()
        assert len(ind.chromosome) > 0

    def test_gene_structure(self):
        """Each gene must have 5 elements: [gate, q1, q2, q3, param]."""
        Individual = _setup_individual()
        ind = Individual()
        for gene in ind.chromosome:
            assert len(gene) == 5

    def test_gate_names_in_gate_set(self):
        Individual = _setup_individual(gates=["H", "CX"])
        ind = Individual()
        for gene in ind.chromosome:
            assert gene[0] in ["H", "CX"]

    def test_qubit_indices_in_range(self):
        no_qu = 3
        Individual = _setup_individual(no_qu=no_qu)
        ind = Individual()
        for gene in ind.chromosome:
            for q in [gene[1], gene[2]]:
                assert 0 <= q < no_qu

    def test_chromosome_provided(self):
        Individual = _setup_individual()
        chrom = [["H", 0, 1, 2, 0.5], ["CX", 0, 1, 2, 0.0]]
        ind = Individual(chrom, crossover=True)
        assert ind.chromosome == chrom


class TestIndividualGenQiskit:
    def test_returns_quantum_circuit(self):
        from qiskit import QuantumCircuit
        Individual = _setup_individual(no_qu=2, gates=["H", "CX"])
        ind = Individual([["H", 0, 1, None, 0.0], ["CX", 0, 1, None, 0.0]])
        ind.gen_qiskit()
        assert isinstance(ind.qis, QuantumCircuit)

    def test_circuit_has_correct_gate_count(self):
        Individual = _setup_individual(no_qu=2, gates=["H", "CX"])
        chrom = [["H", 0, 1, None, 0.0], ["H", 1, 0, None, 0.0]]
        ind = Individual(chrom,crossover=True)
        ind.gen_qiskit()
        assert ind.qis.size() == 2


class TestIndividualFitness:
    def test_fitness_in_range(self):
        """Fitness should be <= 1.0 (fidelity is at most 1, penalty is non-negative)."""
        Individual = _setup_individual(no_qu=2, gates=["H", "CX"])
        ind = Individual()
        ind.calc_fitness()
        assert ind.fitness <= 1.0

    def test_fitness_is_float(self):
        Individual = _setup_individual(no_qu=2, gates=["H", "CX"])
        ind = Individual()
        ind.calc_fitness()
        assert isinstance(ind.fitness, float)

    def test_fidelity_between_zero_and_one(self):
        Individual = _setup_individual(no_qu=2, gates=["H", "CX"])
        ind = Individual()
        fidelity = ind.calc_fidelity()
        assert 0.0 <= fidelity <= 1.0 + 1e-9


class TestIndividualMutate:
    def test_mutate_does_not_change_chromosome_length(self):
        """Mutation must not alter the number of genes."""
        Individual = _setup_individual(mut_rate=1.0)  # force all mutations
        ind = Individual()
        original_length = len(ind.chromosome)
        ind.mutate()
        assert len(ind.chromosome) == original_length

    def test_mutate_gate_types_remain_valid(self):
        gate_set = ["H", "CX", "T"]
        Individual = _setup_individual(gates=gate_set, mut_rate=1.0)
        ind = Individual()
        ind.mutate()
        for gene in ind.chromosome:
            assert gene[0] in gate_set

    def test_mutate_qubit_indices_remain_in_range(self):
        no_qu = 3
        Individual = _setup_individual(no_qu=no_qu, mut_rate=1.0)
        ind = Individual()
        ind.mutate()
        for gene in ind.chromosome:
            for q in [gene[1], gene[2]]:
                assert 0 <= q < no_qu

    def test_mutate_parameter_remains_in_range(self):
        Individual = _setup_individual(mut_rate=1.0)
        ind = Individual()
        ind.mutate()
        for gene in ind.chromosome:
            assert 0.0 <= gene[4] <= 2 * np.pi + 1e-9


# ---------------------------------------------------------------------------
# population.py
# ---------------------------------------------------------------------------

def _make_population(size=10, no_qu=2, gates=None):
    """Helper: create a population of evaluated individuals."""
    from individual import Individual
    if gates is None:
        gates = ["H", "CX"]
    Individual.set_class_vars(no_qu, gates, 0.01)
    pop = [Individual() for _ in range(size)]
    for ind in pop:
        ind.calc_fitness()
    return pop


class TestTournamentSelection:
    def test_returns_individual(self):
        from population import tournament
        from individual import Individual
        pop = _make_population()
        result = tournament(pop, selection_pressure=3)
        assert isinstance(result, Individual)

    def test_winner_is_in_population(self):
        from population import tournament
        pop = _make_population()
        winner = tournament(pop, selection_pressure=3)
        assert winner in pop

    def test_pressure_one_returns_random_individual(self):
        """With pressure=1, any individual can win."""
        from population import tournament
        pop = _make_population(size=20)
        winners = {id(tournament(pop, selection_pressure=1)) for _ in range(50)}
        assert len(winners) > 1  # should see multiple different winners

    def test_high_pressure_tends_to_best(self):
        """With maximum pressure, winner should frequently be the best individual."""
        from population import tournament
        pop = _make_population(size=20)
        best = max(pop, key=lambda ind: ind.fitness)
        wins = sum(
            1 for _ in range(100)
            if tournament(pop, selection_pressure=len(pop)) is best
        )
        assert wins > 50


class TestCrossover:
    def test_returns_two_children(self):
        from population import crossover
        p1 = [["H", 0, 1, 2, 0.0], ["CX", 0, 1, 2, 0.0], ["T", 0, 1, 2, 0.0]]
        p2 = [["X", 0, 1, 2, 0.0], ["CX", 1, 0, 2, 0.0]]
        c1, c2 = crossover(p1, p2)
        assert isinstance(c1, list)
        assert isinstance(c2, list)

    def test_children_are_non_empty(self):
        from population import crossover
        p1 = [["H", 0, 1, 2, 0.0], ["CX", 0, 1, 2, 0.0]]
        p2 = [["X", 0, 1, 2, 0.0], ["T", 0, 1, 2, 0.0]]
        c1, c2 = crossover(p1, p2)
        assert len(c1) > 0
        assert len(c2) > 0

    def test_children_genes_originate_from_parents(self):
        """Every gene in a child must have come from one of the two parents."""
        from population import crossover
        p1 = [["H", 0, 1, 2, 0.1], ["CX", 0, 1, 2, 0.2], ["T", 0, 1, 2, 0.3]]
        p2 = [["X", 0, 1, 2, 0.4], ["Y", 0, 1, 2, 0.5], ["Z", 0, 1, 2, 0.6]]
        all_genes = {tuple(g) for g in p1 + p2}
        c1, c2 = crossover(p1, p2)
        for gene in c1 + c2:
            assert tuple(gene) in all_genes

    def test_parents_not_mutated(self):
        from population import crossover
        p1 = [["H", 0, 1, 2, 0.0], ["CX", 0, 1, 2, 0.0]]
        p2 = [["X", 0, 1, 2, 0.0], ["T", 0, 1, 2, 0.0]]
        p1_copy = [g[:] for g in p1]
        p2_copy = [g[:] for g in p2]
        crossover(p1, p2)
        assert p1 == p1_copy
        assert p2 == p2_copy

    def test_single_gene_parents(self):
        """Crossover of single-gene chromosomes should not raise an error."""
        from population import crossover
        p1 = [["H", 0, 1, 2, 0.0]]
        p2 = [["X", 0, 1, 2, 0.0]]
        c1, c2 = crossover(p1, p2)
        assert isinstance(c1, list)
        assert isinstance(c2, list)


# ---------------------------------------------------------------------------
# ga_runner.py  (smoke test)
# ---------------------------------------------------------------------------

class TestRunGA:
    def test_returns_float(self, tmp_path, monkeypatch):
        """run_ga must return a numeric fitness value."""
        from ga_runner import run_ga
        monkeypatch.chdir(tmp_path)
        (tmp_path / "results").mkdir()

        config = {
            "pop_size": 10,
            "mutation_rate": 0.01,
            "selection_pressure": 3,
            "elitism": 0.1,
        }
        result = run_ga(
            config=config,
            iterations=3,
            no_qu=2,
            gate_set=["H", "CX"],
        )
        assert isinstance(result, float)

    def test_fitness_in_valid_range(self, tmp_path, monkeypatch):
        from ga_runner import run_ga
        monkeypatch.chdir(tmp_path)
        (tmp_path / "results").mkdir()

        config = {
            "pop_size": 10,
            "mutation_rate": 0.01,
            "selection_pressure": 3,
            "elitism": 0.1,
        }
        result = run_ga(
            config=config,
            iterations=3,
            no_qu=2,
            gate_set=["H", "CX"],
        )
        assert result <= 1.0

    def test_writes_results_file(self, tmp_path, monkeypatch):
        from ga_runner import run_ga
        import os
        monkeypatch.chdir(tmp_path)
        (tmp_path / "results").mkdir()

        config = {
            "pop_size": 10,
            "mutation_rate": 0.01,
            "selection_pressure": 3,
            "elitism": 0.1,
        }
        run_ga(
            config=config,
            iterations=2,
            no_qu=2,
            gate_set=["H", "CX"],
        )
        files = os.listdir(tmp_path / "results")
        assert len(files) == 1
        assert files[0].endswith(".json")

    def test_metrics_keys_present(self, tmp_path, monkeypatch):
        from ga_runner import run_ga
        import json, os
        monkeypatch.chdir(tmp_path)
        (tmp_path / "results").mkdir()

        config = {
            "pop_size": 10,
            "mutation_rate": 0.01,
            "selection_pressure": 3,
            "elitism": 0.1,
        }
        run_ga(
            config=config,
            iterations=2,
            no_qu=2,
            gate_set=["H", "CX"],
        )
        file_path = os.path.join(tmp_path / "results", os.listdir(tmp_path / "results")[0])
        with open(file_path) as f:
            metrics = json.load(f)

        assert "generations" in metrics
        assert "time" in metrics
        assert "circuit" in metrics
        assert "ffidelity" in metrics
