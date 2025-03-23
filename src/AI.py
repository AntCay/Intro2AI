import numpy as np
from engine import Engine 
import math
import sys

class randomAI:
    def __init__(self, engine):
        self._engine = engine
        
    def move(self):
        possible_moves = self._engine.results(self._engine.actions())
        self._engine.update_state(possible_moves[np.random.choice(len(possible_moves))])

# Heuristic 1 (h1)
"""
[[16. 17. 18. 19. 20. 22. 24. 25. 27.]
 [14. 15. 16. 17. 19. 20. 22. 23. 25.]
 [12. 13. 14. 15. 17. 18. 20. 22. 24.]
 [10. 11. 12. 13. 15. 17. 18. 20. 22.]
 [ 8.  9. 10. 12. 13. 15. 17. 19. 20.]
 [ 6.  7.  8. 10. 12. 13. 15. 17. 19.]
 [ 2.  5.  6.  8. 10. 12. 14. 16. 18.]
 [ 1.  2.  5.  7.  9. 11. 13. 15. 17.]
 [ 0.  1.  2.  6.  8. 10. 12. 14. 16.]]
"""

# Heuristic 2 (h2)
"""
[[ 8  9 10 11 12 13 14 15 16]
 [ 7  8  9 10 11 12 13 14 15]
 [ 6  7  8  9 10 11 12 13 14]
 [ 5  6  7  8  9 10 11 12 13]
 [ 4  5  6  7  8  9 10 11 12]
 [ 3  4  5  6  7  8  9 10 11]
 [ 2  3  4  5  6  7  8  9 10]
 [ 1  2  3  4  5  6  7  8  9]
 [ 0  1  2  3  4  5  6  7  8]]
"""

class ChooseGreedyNodeAI_h1:
    def __init__(self, engine):
        n, gs = 9, 4
        self._engine = engine
        self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
        self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])

    def move(self):
        if self._engine.game_state[2]:
            distance = self.norm_distance_p1.T + self.grid_distance_p1.T
        else:
            distance = self.norm_distance_p1 + self.grid_distance_p1
        possible_moves = self._engine.results(self._engine.actions())
        if self._engine.turn_count % 3 == 0:
            return self._engine.update_state(possible_moves[np.random.choice(len(possible_moves))])
        best_move = possible_moves[np.argmin(np.sum(distance[None] * possible_moves, axis=(1,2)))]
        return self._engine.update_state(best_move)

class ChooseGreedyNodeAI_h2:
    def __init__(self, engine):
        n, gs = 9, 4
        self._engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)

    def move(self):
        if self._engine.game_state[2]:
            distance = self.heuristic.T
        else:
            distance = self.heuristic
        possible_moves = self._engine.results(self._engine.actions())
        if self._engine.turn_count % 3 == 0:
            return self._engine.update_state(possible_moves[np.random.choice(len(possible_moves))])
        best_move = possible_moves[np.argmin(np.sum(distance[None] * possible_moves, axis=(1,2)))]
        return self._engine.update_state(best_move)
    
class AStarAI_h1:
    def  __init__(self, engine):
        n, gs = 9, 4
        self._engine = engine
        self.cost = 0
        self.evaluation = 0
        self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
        self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])
        
    def move(self):
        self.cost += 1
        if self._engine.game_state[2]:
            heuristic = self.norm_distance_p1.T + self.grid_distance_p1.T
        else:
            heuristic = self.norm_distance_p1.T + self.grid_distance_p1
        
        possible_moves = self._engine.results(self._engine.actions())
            
        heuristic_all = np.sum(heuristic * possible_moves, axis=(1,2))
        
        self.evaluation = np.add(heuristic_all, np.full(heuristic_all.shape, self.cost))        
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)

# A* Algorithm with Manhattan Distance as a heuristic function
class AStarAI_h2:
    def  __init__(self, engine):
        n, gs = 9, 4
        self._engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.cost = 0
        self.evaluation = 0
        
    def move(self):
        self.cost += 1
        if self._engine.game_state[2]:
            heuristic = self.heuristic.T
        else:
            heuristic = self.heuristic
        
        possible_moves = self._engine.results(self._engine.actions())
            
        heuristic_all = np.sum(heuristic * possible_moves, axis=(1,2))
        
        self.evaluation = np.add(heuristic_all, np.full(heuristic_all.shape, self.cost))

        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)
    
class LookAhead_h1:
    def  __init__(self, engine: Engine):
        n, gs = 9, 4
        self._engine: Engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.evaluation = 0
        self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
        self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])
        
    def move(self):
        if self._engine.game_state[2]:
            heuristic = self.norm_distance_p1.T + self.grid_distance_p1.T
        else:
            heuristic = self.norm_distance_p1 + self.grid_distance_p1
        
        possible_moves = self._engine.results(self._engine.actions())
        possible_moves_heuristics = np.sum(heuristic * possible_moves, axis=(1, 2))

        # save current engine state for resetting
        cur_p1_mask = self._engine._p1_mask
        cur_p2_mask = self._engine._p2_mask
        cur_turn = self._engine.is_p2_turn
        cur_turn_count = self._engine.turn_count

        # iterate through possible moves
        for i, move in enumerate(possible_moves):

            # check if move achieves goal state
            if self._engine.update_state(move):
                # if it does, reset effects of update_state and return updated state
                self._engine._p1_mask = cur_p1_mask
                self._engine._p2_mask = cur_p2_mask
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                return self._engine.update_state(move)
            # if not, make the engine think it is our move again and get possible moves
            else:
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                possible_next_moves = self._engine.results(self._engine.actions())
                next_move_heuristics = np.sum(heuristic * possible_next_moves, axis=(1, 2))
                possible_moves_heuristics[i] += np.min(next_move_heuristics)

            # restore state to our original turn
            self._engine._p1_mask = cur_p1_mask
            self._engine._p2_mask = cur_p2_mask
            self._engine.is_p2_turn = cur_turn
            self._engine.turn_count = cur_turn_count

        self.evaluation = possible_moves_heuristics
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)

# Algorithm that looks ahead one more move for each possible move.
class LookAhead_h2:
    def  __init__(self, engine: Engine):
        n, gs = 9, 4
        self._engine: Engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.evaluation = 0
        
    def move(self):
        if self._engine.game_state[2]:
            heuristic = self.heuristic.T
        else:
            heuristic = self.heuristic
        
        possible_moves = self._engine.results(self._engine.actions())
        possible_moves_heuristics = np.sum(heuristic * possible_moves, axis=(1, 2))

        # save current engine state for resetting
        cur_p1_mask = self._engine._p1_mask
        cur_p2_mask = self._engine._p2_mask
        cur_turn = self._engine.is_p2_turn
        cur_turn_count = self._engine.turn_count

        # iterate through possible moves
        for i, move in enumerate(possible_moves):

            # check if move achieves goal state
            if self._engine.update_state(move):
                # if it does, reset effects of update_state and return updated state
                self._engine._p1_mask = cur_p1_mask
                self._engine._p2_mask = cur_p2_mask
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                return self._engine.update_state(move)
            # if not, make the engine think it is our move again and get possible moves
            else:
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                possible_next_moves = self._engine.results(self._engine.actions())
                next_move_heuristics = np.sum(heuristic * possible_next_moves, axis=(1, 2))
                possible_moves_heuristics[i] += np.min(next_move_heuristics)

            # restore state to our original turn
            self._engine._p1_mask = cur_p1_mask
            self._engine._p2_mask = cur_p2_mask
            self._engine.is_p2_turn = cur_turn
            self._engine.turn_count = cur_turn_count

        self.evaluation = possible_moves_heuristics
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)

# minimax h1
class MiniMax_h1:
    def  __init__(self, engine: Engine):
        n, gs = 9, 4
        self._engine: Engine = engine
        self.evaluation = 0
        self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
        self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])
        
    def move(self):
        if self._engine.game_state[2]:
            heuristic = self.norm_distance_p1.T + self.grid_distance_p1.T
        else:
            heuristic = self.norm_distance_p1 + self.grid_distance_p1
        
        possible_moves = self._engine.results(self._engine.actions())
        possible_moves_heuristics = np.sum(heuristic * possible_moves, axis=(1, 2))

        # save current engine state for resetting
        cur_p1_mask = self._engine._p1_mask
        cur_p2_mask = self._engine._p2_mask
        cur_turn = self._engine.is_p2_turn
        cur_turn_count = self._engine.turn_count

        # iterate through possible moves
        for i, move in enumerate(possible_moves):

            # check if move achieves goal state
            if self._engine.update_state(move):
                # if it does, reset effects of update_state and return updated state
                self._engine._p1_mask = cur_p1_mask
                self._engine._p2_mask = cur_p2_mask
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                return self._engine.update_state(move)
            # if not, get the best move for the other player, update the state, and then add our next best move heuristic to the heuristic list
            else:
                # make best move for other player
                other_player_moves = self._engine.results(self._engine.actions())
                other_player_heuristic = heuristic.T
                other_player_move_heuristic = np.sum(other_player_heuristic * other_player_moves, axis=(1,2))
                other_player_best_move_index = np.where(other_player_move_heuristic == np.min(other_player_move_heuristic))
                other_player_best_move = other_player_moves[np.random.choice(other_player_best_move_index[0])]
                self._engine.update_state(other_player_best_move)

                # get heuristic for our next best move
                possible_next_moves = self._engine.results(self._engine.actions())
                next_move_heuristics = np.sum(heuristic * possible_next_moves, axis=(1, 2))
                possible_moves_heuristics[i] += np.min(next_move_heuristics)

            # restore state to our original turn
            self._engine._p1_mask = cur_p1_mask
            self._engine._p2_mask = cur_p2_mask
            self._engine.is_p2_turn = cur_turn
            self._engine.turn_count = cur_turn_count

        self.evaluation = possible_moves_heuristics
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)

# minimax h2
class MiniMax_h2:
    def  __init__(self, engine: Engine):
        n, gs = 9, 4
        self._engine: Engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.evaluation = 0
        
    def move(self):
        # set heuristic based on turn
        if self._engine.game_state[2]:
            heuristic = self.heuristic.T
        else:
            heuristic = self.heuristic
        
        possible_moves = self._engine.results(self._engine.actions())
        possible_moves_heuristics = np.sum(heuristic * possible_moves, axis=(1, 2))

        # save current engine state for resetting
        cur_p1_mask = self._engine._p1_mask
        cur_p2_mask = self._engine._p2_mask
        cur_turn = self._engine.is_p2_turn
        cur_turn_count = self._engine.turn_count

        # iterate through possible moves
        for i, move in enumerate(possible_moves):

            # check if move achieves goal state
            if self._engine.update_state(move):
                # if it does, reset effects of update_state and return updated state
                self._engine._p1_mask = cur_p1_mask
                self._engine._p2_mask = cur_p2_mask
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                return self._engine.update_state(move)
            # if not, get the best move for the other player, update the state, and then add our next best move heuristic to the heuristic list
            else:
                # make best move for other player
                other_player_moves = self._engine.results(self._engine.actions())
                other_player_heuristic = heuristic.T
                other_player_move_heuristic = np.sum(other_player_heuristic * other_player_moves, axis=(1,2))
                other_player_best_move_index = np.where(other_player_move_heuristic == np.min(other_player_move_heuristic))
                other_player_best_move = other_player_moves[np.random.choice(other_player_best_move_index[0])]
                self._engine.update_state(other_player_best_move)

                # get heuristic for our next best move
                possible_next_moves = self._engine.results(self._engine.actions())
                next_move_heuristics = np.sum(heuristic * possible_next_moves, axis=(1, 2))
                possible_moves_heuristics[i] += np.min(next_move_heuristics)

            # restore state to our original turn
            self._engine._p1_mask = cur_p1_mask
            self._engine._p2_mask = cur_p2_mask
            self._engine.is_p2_turn = cur_turn
            self._engine.turn_count = cur_turn_count

        self.evaluation = possible_moves_heuristics
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)

# minimax h1 AND h2
class MiniMax_h1_h2:
    def  __init__(self, engine: Engine):
        n, gs = 9, 4
        self._engine: Engine = engine
        self.evaluation = 0
        self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
        self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])
        
    def move(self):
        if self._engine.game_state[2]:
            if self._engine.turn_count < 50:
                heuristic = self.norm_distance_p1.T + self.grid_distance_p1.T
            else:
                heuristic = self.grid_distance_p1.T

        else:
            if self._engine.turn_count < 50:
                heuristic = self.norm_distance_p1 + self.grid_distance_p1
            else:
                heuristic = self.grid_distance_p1
        
        possible_moves = self._engine.results(self._engine.actions())
        possible_moves_heuristics = np.sum(heuristic * possible_moves, axis=(1, 2))

        # save current engine state for resetting
        cur_p1_mask = self._engine._p1_mask
        cur_p2_mask = self._engine._p2_mask
        cur_turn = self._engine.is_p2_turn
        cur_turn_count = self._engine.turn_count

        # iterate through possible moves
        for i, move in enumerate(possible_moves):

            # check if move achieves goal state
            if self._engine.update_state(move):
                # if it does, reset effects of update_state and return updated state
                self._engine._p1_mask = cur_p1_mask
                self._engine._p2_mask = cur_p2_mask
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                return self._engine.update_state(move)
            # if not, get the best move for the other player, update the state, and then add our next best move heuristic to the heuristic list
            else:
                # make best move for other player
                other_player_moves = self._engine.results(self._engine.actions())
                other_player_heuristic = heuristic.T
                other_player_move_heuristic = np.sum(other_player_heuristic * other_player_moves, axis=(1,2))
                other_player_best_move_index = np.where(other_player_move_heuristic == np.min(other_player_move_heuristic))
                other_player_best_move = other_player_moves[np.random.choice(other_player_best_move_index[0])]
                self._engine.update_state(other_player_best_move)

                # get heuristic for our next best move
                possible_next_moves = self._engine.results(self._engine.actions())
                next_move_heuristics = np.sum(heuristic * possible_next_moves, axis=(1, 2))
                possible_moves_heuristics[i] += np.min(next_move_heuristics)

            # restore state to our original turn
            self._engine._p1_mask = cur_p1_mask
            self._engine._p2_mask = cur_p2_mask
            self._engine.is_p2_turn = cur_turn
            self._engine.turn_count = cur_turn_count

        self.evaluation = possible_moves_heuristics
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)
    
# minimax norm then grid
class MiniMax_norm_grid:
    def  __init__(self, engine: Engine):
        n, gs = 9, 4
        self._engine: Engine = engine
        self.evaluation = 0
        self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
        self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])
        
    def move(self):
        if self._engine.game_state[2]:
            if self._engine.turn_count < 50:
                heuristic = self.norm_distance_p1.T
            else:
                heuristic = self.grid_distance_p1.T

        else:
            if self._engine.turn_count < 50:
                heuristic = self.norm_distance_p1
            else:
                heuristic = self.grid_distance_p1
        
        possible_moves = self._engine.results(self._engine.actions())
        possible_moves_heuristics = np.sum(heuristic * possible_moves, axis=(1, 2))

        # save current engine state for resetting
        cur_p1_mask = self._engine._p1_mask
        cur_p2_mask = self._engine._p2_mask
        cur_turn = self._engine.is_p2_turn
        cur_turn_count = self._engine.turn_count

        # iterate through possible moves
        for i, move in enumerate(possible_moves):

            # check if move achieves goal state
            if self._engine.update_state(move):
                # if it does, reset effects of update_state and return updated state
                self._engine._p1_mask = cur_p1_mask
                self._engine._p2_mask = cur_p2_mask
                self._engine.is_p2_turn = cur_turn
                self._engine.turn_count = cur_turn_count
                return self._engine.update_state(move)
            # if not, get the best move for the other player, update the state, and then add our next best move heuristic to the heuristic list
            else:
                # make best move for other player
                other_player_moves = self._engine.results(self._engine.actions())
                other_player_heuristic = heuristic.T
                other_player_move_heuristic = np.sum(other_player_heuristic * other_player_moves, axis=(1,2))
                other_player_best_move_index = np.where(other_player_move_heuristic == np.min(other_player_move_heuristic))
                other_player_best_move = other_player_moves[np.random.choice(other_player_best_move_index[0])]
                self._engine.update_state(other_player_best_move)

                # get heuristic for our next best move
                possible_next_moves = self._engine.results(self._engine.actions())
                next_move_heuristics = np.sum(heuristic * possible_next_moves, axis=(1, 2))
                possible_moves_heuristics[i] += np.min(next_move_heuristics)

            # restore state to our original turn
            self._engine._p1_mask = cur_p1_mask
            self._engine._p2_mask = cur_p2_mask
            self._engine.is_p2_turn = cur_turn
            self._engine.turn_count = cur_turn_count

        self.evaluation = possible_moves_heuristics
        best_moves_index = np.where(self.evaluation == np.min(self.evaluation))
        best_move = possible_moves[np.random.choice(best_moves_index[0])] # Pick random move from best moves if it more than 1
        return self._engine.update_state(best_move)
    
class  MCTSAI: 
    def  __init__(self, engine, explorationWeight=1.4, iterations=500):
        n, gs = 9, 4
        self._engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.cost = 0
        self.evaluation = 0
        self.explorationWeight = explorationWeight
        self.iterations = iterations
    
    class Node:
        def __init__(self, state, parent=None):
            self.initial_state = state
            self.state = state
            self.parent = parent
            self.player = self.state[2]
            self.children = {}
            self.visits = 0
            self.reward = 0
            self.e = Engine()
            self.e.p1_mask = self.state[0]
            self.e.p2_mask = self.state[1]
            self.e.is_p2_turn = self.state[2]
            n, gs = 9, 4
            self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)

        def isFullyExpanded(self):
            return len(self.children) == len(self.getBestLegalMoves())
        
        def isGoal(self):
            return self.e.is_goal()
        
        def getLegalMoves(self):
            return self.e.results(self.e.actions())
        
        def getBestLegalMoves(self):
            heuristic = np.sum(self.heuristic * self.getLegalMoves(), axis=(1,2))    
            best_moves_index = np.where(heuristic == np.min(heuristic))[0]
            best_moves = np.empty((0,) + self.getLegalMoves().shape[1:], dtype=self.getLegalMoves().dtype)
            for x in best_moves_index:
                best_moves = np.append(best_moves, [self.getLegalMoves()[x]], axis=0)
            return best_moves
        
        def updateState(self, move):
            self.e.update_state(move)
            self.state = self.e.game_state
            self.player = self.state[2]
        
        def setToInitialState(self):
            self.e.p1_mask = self.initial_state[0]
            self.e.p2_mask = self.initial_state[1]
            self.e.is_p2_turn = self.initial_state[2]
            self.state = self.e.game_state
    
    def move(self):
        e = Engine()
        e.p1_mask = self._engine.p1_mask
        e.p2_mask = self._engine.p2_mask
        e.is_p2_turn = self._engine.is_p2_turn
        root_node = self.Node(e.game_state)
        # start MCTS Algorithm
        self.mcts(root_node)
        best_move = max(
            root_node.children.items(),
            key=lambda item: (item[1].reward / item[1].visits if item[1].visits != 0 else -float('inf'))
        )[0] # Choose the best move of children that has highest average reward
        return self._engine.update_state(np.array(best_move))  
    
    def mcts(self, root_node):
        for _ in range(self.iterations):
            selected_node = self.select(root_node)  # Select the best child of the selected node
            if selected_node.isGoal():  
                if root_node.player != selected_node.player:
                    reward = 1
                else:
                    reward = 0
            else:
                reward = self.simulate(root_node, selected_node)    # Simulate the game until terminate state and get reward
            self.backpropagate(root_node,selected_node, reward)     # Backpropagate the reward to the selected node
        
    def select(self, node):
        while not node.isGoal():
            if not node.isFullyExpanded():
                return self.expand(node)    # Expand the node if it is not fully expanded
            else:
                node = self.bestChild(node) # Select the best child of the selected node
        return node

    def expand(self, node):
        legal_moves = node.getBestLegalMoves()
        for move in legal_moves:
            move_tuple = tuple(map(tuple, move))  # Convert numpy.ndarray to tuple
            if move_tuple not in node.children:
                node.updateState(move)
                child_node = self.Node(node.state, parent=node)
                node.children[move_tuple] = child_node
                node.setToInitialState()
                return child_node
        return None

    def bestChild(self, node):  # calculate the best child of the selected node by using UCT
        max_uct = -float('inf')
        best = None
        for child in node.children.values():
            if child.visits == 0:
                uct = float('inf')
            else:
                exploitation = child.reward / child.visits
                exploration = self.explorationWeight * math.sqrt(math.log(node.visits) / child.visits)
                uct = exploitation + exploration
            if uct > max_uct:
                max_uct = uct
                best = child
        return best
    
    def simulate(self, root_node, selected_node, max_depth=100): # Simulate the game until terminate state and get reward
        depth = 0
        while not selected_node.isGoal():
            if selected_node.player:
                heuristic = self.heuristic.T
            else:
                heuristic = self.heuristic
                
            if depth >= max_depth:  # If the depth is greater than the maximum depth, estimate reward from that state
                if root_node.player:
                    player_dist = np.sum(heuristic[None] * selected_node.state[1])
                    opponent_dist = np.sum(heuristic[None]  * selected_node.state[0])
                    return 1 if player_dist < opponent_dist else 0
                else:
                    player_dist = np.sum(heuristic[None] * selected_node.state[0])
                    opponent_dist = np.sum(heuristic[None]  * selected_node.state[1])
                    return 1 if player_dist < opponent_dist else 0
            
            legal_moves = selected_node.getLegalMoves()
      
            heuristic_all = np.sum(heuristic * legal_moves, axis=(1,2))
            best_moves_index = np.where(heuristic_all == np.min(heuristic_all))
            move = legal_moves[np.random.choice(best_moves_index[0])] 
            selected_node.updateState(move)
            depth = depth + 1
            
        if root_node.player != selected_node.player:
            return 1
        else:
            return 0

    def backpropagate(self, root_node, selected_node, reward):  # Backpropagate the reward from the selected node to the root node
        while selected_node is not None:
            selected_node.visits += 1
            selected_node.reward += reward
            selected_node = selected_node.parent


    

# class SortaGreedyTreeSearchAI: # WIP
#     def __init__(self, engine, depth=1):
#         n, gs = 9, 4
#         self._engine = engine
#         self.grid_distance_p1 = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
#         self.norm_distance_p1 = np.floor(np.linalg.norm(np.mgrid[0:9, 0:9][:, ::-1, :], axis=0))
#         self.norm_distance_p1[n - gs:, :gs] = np.triu(self.norm_distance_p1[n - gs:, :gs])
#         self.depth = depth
#
#     def move(self):
#         if self._engine.game_state[2]:
#             distance = self.norm_distance_p1.T + self.grid_distance_p1.T
#         else:
#             distance = self.norm_distance_p1 + self.grid_distance_p1
#
#         possible_moves = self._engine.results(self._engine.actions())
#         possible_move_rating = np.sum(distance[None] * possible_moves, axis=(1,2))
#         frontier_me = [possible_moves]
#
#
#         for i in range(self.depth):
#             # Expand current best node
#             np.argmin(possible_move_rating)
#             # We simulate opponent max-ing
#
#             # Then we simulate us min-ing
#
#             frontier_sorted_ids = np.argsort(np.sum(distance[None] * frontier, axis=(1, 2)), axis=0)
#             frontier = frontier[frontier_sorted_ids]
#             frontier_turns = frontier_turns[frontier_sorted_ids]
#             cs = (frontier[0, 0], frontier[0, 1], frontier_turns[0])
#             ct= frontier[0]
#             frontier = frontier[1:]
#             frontier_turns = frontier_turns[1:]
#
#             if cs not in expanded_nodes:
#                 if self._engine.is_goal(cs):
#                     return cs
#                 frontier = np.append(frontier, self._engine.results(self._engine.actions(cs), state=cs))
#                 frontier_turns = np.append(frontier_turns, np.full(frontier_turns.shape[0], not ct, dtype=np.bool))
#                 expanded_nodes.append(cs)
#         best = np.max(np.sum(distance[None] * frontier, axis=(1, 2)), axis=0)
#         return frontier[0]


