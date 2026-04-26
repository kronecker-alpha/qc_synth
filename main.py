"""
Main code with GUI. Run directly from here.
"""

from PySide6.QtWidgets import QApplication

from parameters import (
    pop_size,
    mutation_rate,
    selection_pressure,
    elitism,
    no_qu,
    gate_set
)

from ga_runner import run_ga

# total evaluation budget
TARGET_EVALS = 100000


def main():

    # configuration dictionary
    config = {
        "pop_size": pop_size,
        "mutation_rate": mutation_rate,
        "selection_pressure": selection_pressure,
        "elitism": elitism
    }

    # maintain constant evaluation budget
    iterations = int(TARGET_EVALS / config["pop_size"])

    # initialise GUI
    app = QApplication([])

    from gui import GADisplay
    display = GADisplay(app)

    # run genetic algorithm
    run_ga(
        config=config,
        iterations=iterations,
        no_qu=no_qu,
        gate_set=gate_set,
        display=display
    )

    # keep window open
    app.exec()


if __name__ == "__main__":
    main()