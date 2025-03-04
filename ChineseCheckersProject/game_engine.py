import numpy as np

class TwoPlayerCheckers:
    def __init__(self):
        n, gs = 9, 4 # n is the board size, gs is the number of rows in the starting position

        self.is_p1_turn = True
        # Initialise starting player positions and player 2 goal mask, where [y, x] is the indexing.
        self.goal_map_p2 = np.zeros((n, n), dtype=np.bool)
        self.goal_map_p2[n-gs:, :gs] = np.tri(np.ones((gs, gs), dtype=np.bool))
        self._p1_mask = np.copy(self.goal_map_p2)
        self._p2_mask = self.goal_map_p2.T

    #region Properties
    @property
    def p1_mask(self):
        return self._p1_mask

    @property
    def p2_mask(self):
        return self._p2_mask

    @property
    def player_loc(self):
        return self.p1_mask + self.p2_mask
    #endregion

    def actions(self, state):
        pass

    # Goal state check, should be used after updating the board
    def is_goal(self):
        if np.sum(self.goal_map_p2[self.player_loc]) == 10 and np.sum(self.goal_map_p2[self.p2_mask]):
            print("Player two wins!")
            return True
        elif np.sum(self.goal_map_p2.T[self.player_loc]) == 10 and np.sum(self.goal_map_p2.T[self.p1_mask]):
            print("Player one wins!")
            return True
        return False

    def update_state(self, action):
        pass