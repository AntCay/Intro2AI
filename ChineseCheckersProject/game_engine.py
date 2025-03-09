import numpy as np

class TwoPlayerCheckers:
    def __init__(self):
        n, gs = 9, 4 # n is the board size, gs is the number of rows in the starting position
        self.max_turns = 200
        self.turn_count = 0
        self.is_p2_turn = False
        # Initialise starting player positions and player 2 goal mask, where [y, x] is the indexing.
        self.goal_map_p1 = np.zeros((n, n), dtype=np.bool)
        self.goal_map_p1[n-gs:, :gs] = np.tri(gs, dtype=np.bool)
        self._p1_mask = self.goal_map_p1.T
        self._p2_mask = np.copy(self.goal_map_p1)

    #region Properties
    @property
    def p1_mask(self):
        return self._p1_mask

    @property
    def p2_mask(self):
        return self._p2_mask

    @property
    def player_loc(self):
        return self._p1_mask + self._p2_mask

    @property
    def game_state(self):
        game_state = (self._p1_mask, self._p2_mask, self.is_p2_turn)
        return game_state
    #endregion

    def actions(self, state = None):
        if state is None:
            state = self.game_state
        pad_size = 2
        player = state[state[2]]
        player_loc = np.pad(state[0] + state[1], pad_size, constant_values=1)

        n = np.shape(player)[0]
        unit_map = np.swapaxes(np.nonzero(player), 0, 1) # maps unit indexes to their location
        actions = np.zeros((np.sum(player), n + 2 * pad_size, n + 2 * pad_size), dtype=np.bool)
        unsure_jumps = []

        # Initialise helper matrices
        adjacent_moves_index = np.indices((3, 3))[:, ~np.eye(3, dtype=np.bool)[:, ::-1]] - 1 + pad_size
        jump_reach_index = np.array([[1, 0, 1, 0, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 1]])
        jump_reach_index = np.indices((5, 5))[:, jump_reach_index.astype(np.bool)] - 2 + pad_size


        for i, unit in enumerate(unit_map):
            # 1) Iterate over queue of possible jumps for the unit
            unsure_jumps.append(unit)
            while len(unsure_jumps) > 0:
                landing = unsure_jumps.pop()

                y, x = jump_reach_index + np.array(landing)[:, None]
                new_landing_ids = np.array(np.nonzero(~player_loc[y, x] * ~actions[i, y, x]
                        * player_loc[adjacent_moves_index[0] + landing[0], adjacent_moves_index[1] + landing[1]]))[0]

                if new_landing_ids.size:
                    actions[i, y[new_landing_ids], x[new_landing_ids]] = True
                    for new_landing_id in np.swapaxes([y[new_landing_ids] - pad_size, x[new_landing_ids] - pad_size], 0, 1).tolist():
                        unsure_jumps.append(new_landing_id)

            # 2) Then add all adjacent moves
            actions[i, adjacent_moves_index[0] + unit[0], adjacent_moves_index[1] + unit[1]] =\
                ~player_loc[adjacent_moves_index[0] + unit[0], adjacent_moves_index[1]  + unit[1]]

        return actions[:, 2:-2, 2:-2], unit_map

    def results(self, actions, unit_map = None, state = None):
        if state is None:
            state = self.game_state
        if unit_map is None:
            unit_map = actions[1]
            actions = actions[0]

        player = state[state[2]]
        results = []
        for i, unit in enumerate(unit_map):
            for move in np.transpose(np.nonzero(actions[i, :, :])):
                if move.size:
                    result = np.copy(player)
                    result[move[0], move[1]] = True
                    result[unit[0], unit[1]] = False
                    results.append(result)
        return np.array(results)

    # Goal state check, should be used after updating the board. Can use it for the game loop while condition.
    def is_goal(self):
        if np.sum(self.goal_map_p1.T[self.player_loc]) == 10 and np.any(self.goal_map_p1.T[self.p2_mask]):
            print("Player two wins!")
            return True
        elif np.sum(self.goal_map_p1[self.player_loc]) == 10 and np.any(self.goal_map_p1[self.p1_mask]):
            print("Player one wins!")
            return True
        elif self.turn_count >= self.max_turns:
            print("Max turns reached!")
            return True
        return False

    def update_state(self, result):
        if self.is_p2_turn:
            self._p2_mask = result
        else:
            self._p1_mask = result
        self.is_p2_turn = not self.is_p2_turn
        self.turn_count += 1
        return self.is_goal()