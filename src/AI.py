import numpy as np

class randomAI:
    def __init__(self, engine):
        self._engine = engine
        
    def move(self):
        possible_moves = self._engine.results(self._engine.actions())
        self._engine.update_state(possible_moves[np.random.choice(len(possible_moves))])


