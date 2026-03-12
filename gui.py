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
        self.setGeometry(100, 100, 1200, 600)
        
        # Store fitness history
        self.fitness_history = []
        
        # Create main layout
        main_layout = QHBoxLayout()
        
        # Left side: Circuit display
        left_layout = QVBoxLayout()
        
        # Iteration label
        self.iteration_label = QLabel("Iteration: 0")
        left_layout.addWidget(self.iteration_label)
        
        # Text display for best.qis
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        
        # Set monospace font for proper circuit alignment
        font = QFont("Courier New", 20)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_display.setFont(font)
        
        left_layout.addWidget(self.text_display)
        
        # Right side: Fitness graph
        right_layout = QVBoxLayout()
        
        # Fitness label
        self.fitness_label = QLabel("Best Fitness: 0.0")
        right_layout.addWidget(self.fitness_label)
        
        # Matplotlib canvas
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Iteration')
        self.ax.set_ylabel('Best Fitness')
        self.ax.set_title('Best Fitness Over Time')
        self.ax.grid(True)
        
        right_layout.addWidget(self.canvas)
        
        # Add both sides to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)
        
        self.setLayout(main_layout)
        self.show()
    
    def update_display(self, iteration, qis_text, state, fitness):
        """Update the display with new iteration, qis circuit, and fitness."""
        self.iteration_label.setText(f"Iteration: {iteration}")
        self.fitness_label.setText(f"Best Fitness: {fitness:.6f}")
        output = f"{str(qis_text)}\n{state}"
        self.text_display.setPlainText(output)
        
        # Update fitness history
        self.fitness_history.append(fitness)
        
        # Update plot
        self.ax.clear()
        self.ax.plot(range(len(self.fitness_history)), self.fitness_history, 'b-', linewidth=2)
        self.ax.set_xlabel('Iteration')
        self.ax.set_ylabel('Best Fitness')
        self.ax.set_title('Best Fitness Over Time')
        self.ax.grid(True)
        self.figure.tight_layout()
        self.canvas.draw()
        
        self.app.processEvents()  # Process GUI events to update display
    