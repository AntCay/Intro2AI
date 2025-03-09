import time
import numpy as np
from game_engine import TwoPlayerCheckers

game = TwoPlayerCheckers()

start_time = time.time_ns()

game.actions(game.game_state)

print("--- %s ms ---" % ((time.time_ns() - start_time) // 1_000_000))