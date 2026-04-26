"""
Code for creating the GUI.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class GADisplay(QWidget):
    """Widget to display genetic algorithm progress."""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Genetic Algorithm - Best Circuit")
        self.setGeometry(100, 100, 1200, 620)
        self.fitness_history = []
        self.avg_fitness_history = []
        self.worst_fitness_history = []

        self.setStyleSheet("background-color: #f5f5f5; color: #1a1a1a;")

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(16, 12, 16, 0)

        self.iteration_label = QLabel("Generation: 0")
        self.iteration_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #2563eb;"
        )

        self.fitness_label = QLabel("Best Fitness: 0.0")
        self.fitness_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #16a34a;"
        )

        self.avg_fitness_label = QLabel("Avg Fitness: 0.0")
        self.avg_fitness_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #d97706;"
        )

        self.worst_fitness_label = QLabel("Worst Fitness: 0.0")
        self.worst_fitness_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #dc2626;"
        )

        top_bar.addWidget(self.iteration_label)
        top_bar.addStretch()
        top_bar.addWidget(self.avg_fitness_label)
        top_bar.addStretch()
        top_bar.addWidget(self.worst_fitness_label)
        top_bar.addStretch()
        top_bar.addWidget(self.fitness_label)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(16, 8, 16, 16)
        main_layout.setSpacing(16)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        font = QFont("Courier New", 18)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_display.setFont(font)
        self.text_display.setStyleSheet(
            "background-color: #ffffff; color: #1a1a1a;"
            "border: 1px solid #d1d5db; border-radius: 6px; padding: 8px;"
        )
        main_layout.addWidget(self.text_display, 1)

        self.figure = Figure(figsize=(6, 5), facecolor="#f5f5f5")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setStyleSheet("border: 1px solid #d1d5db; border-radius: 6px;")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#ffffff")
        self._style_axes()
        main_layout.addWidget(self.canvas, 1)

        wrapper = QVBoxLayout()
        wrapper.setSpacing(0)
        wrapper.addLayout(top_bar)
        wrapper.addLayout(main_layout)
        self.setLayout(wrapper)
        self.show()

    def _style_axes(self):
        """Apply consistent light-theme styling to the plot axes."""
        self.ax.set_xlabel("Generation", color="#1a1a1a")
        self.ax.set_ylabel("Best Fitness", color="#1a1a1a")
        self.ax.set_title("Best Fitness Over Time", color="#1a1a1a", pad=10)
        self.ax.tick_params(colors="#6b7280")
        self.ax.grid(True, color="#e5e7eb", linestyle="--", linewidth=0.6)
        for spine in self.ax.spines.values():
            spine.set_edgecolor("#d1d5db")

    def update_display(self, iteration, qis_text, state, fitness, avg_fitness, worst_fitness):
        """Update the display with new iteration, qis circuit, and fitness statistics."""
        self.iteration_label.setText(f"Generation: {iteration}")
        self.fitness_label.setText(f"Best Fitness: {fitness:.6f}")
        self.avg_fitness_label.setText(f"Avg Fitness: {avg_fitness:.6f}")
        self.worst_fitness_label.setText(f"Worst Fitness: {worst_fitness:.6f}")
        self.text_display.setPlainText(f"{qis_text}\n{state}")

        self.fitness_history.append(fitness)
        self.avg_fitness_history.append(avg_fitness)
        self.worst_fitness_history.append(worst_fitness)

        x = range(len(self.fitness_history))
        self.ax.clear()
        self.ax.set_facecolor("#ffffff")
        self.ax.plot(x, self.fitness_history, color="#16a34a", linewidth=2, label="Best")
        self.ax.plot(x, self.avg_fitness_history, color="#d97706", linewidth=2, label="Average")
        self.ax.plot(x, self.worst_fitness_history, color="#dc2626", linewidth=2, label="Worst")
        self.ax.legend(loc="lower right", fontsize=9)
        self._style_axes()
        self.figure.tight_layout()
        self.canvas.draw()
        self.app.processEvents()