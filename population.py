from individual import Individual

class population:
    def __init__(self,pop_size):
        """Initialisation"""
        self.pop_size = pop_size
        self.population = [Individual() for _ in range(0,pop_size)]

    