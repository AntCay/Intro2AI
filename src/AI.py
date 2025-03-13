import numpy as np
import math

class randomAI:
    def __init__(self, engine):
        self._engine = engine
        
    def move(self):
        possible_moves = self._engine.results(self._engine.actions())
        self._engine.update_state(possible_moves[np.random.choice(len(possible_moves))])

class ChooseGreedyNodeAI:
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

# A* Algorithm with Manhattan Distance as a heuristic function
class AStarAI:
    def  __init__(self, engine):
        n, gs = 9, 4
        self._engine = engine
        self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
        self.cost = 0
        self.evaluation = 0
        
    def move(self):
        if self._engine.game_state[2]:
            heuristic = self.heuristic.T
        else:
            heuristic = self.heuristic
        
        possible_moves = self._engine.results(self._engine.actions())
            
        heuristic_all = np.sum(heuristic * possible_moves, axis=(1,2))
        if self._engine.game_state[2]:
            print(heuristic_all)
            print(heuristic * possible_moves)
        self.evaluation = np.add(heuristic_all, np.full(heuristic_all.shape, self.cost))
        best_move = possible_moves[np.argmin(self.evaluation)]
        
        return self._engine.update_state(best_move)

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
