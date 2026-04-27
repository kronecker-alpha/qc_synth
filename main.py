"""
Run an instance with the GUI, using parameters, gate set and target from parameters.py
"""
from PySide6.QtWidgets import QApplication
from gui import GADisplay
from parameters import pop_size, mutation_rate, selection_pressure, elitism, no_qu,gate_set
from ga_runner import run_ga

#total evaluation budget
TARGET_EVALS = 1000

def main():
    config = { #config dictionary
        "pop_size": pop_size,
        "mutation_rate": mutation_rate,
        "selection_pressure": selection_pressure,
        "elitism": elitism
    }

    #maintain constant computational budget
    iterations = int(TARGET_EVALS / config["pop_size"])

    app = QApplication([]) #initialises GUI
    display = GADisplay(app)

    #run genetic algorithm
    run_ga(
        config=config,
        iterations=iterations,
        no_qu=no_qu,
        gate_set=gate_set,
        display=display
    )

    #keeps window open
    app.exec()


if __name__ == "__main__":
    main()