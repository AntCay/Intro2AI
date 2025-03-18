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
    
# class  MCTSAI: # To Do
#     def  __init__(self, engine, explorationWeight=0.5, iterations=500):
#         n, gs = 9, 4
#         self._engine = engine
#         self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
#         self.cost = 0
#         self.evaluation = 0
#         self.explorationWeight = explorationWeight
#         self.iterations = iterations
#         self.heuristic = np.sum(np.mgrid[0:n, 0:n][:, ::-1, :],axis=0)
    
#     class Node:
#         def __init__(self, state, parent=None):
#             self.initial_state = state
#             self.state = state
#             self.parent = parent
#             self.player = self.state[2]
#             self.children = {}
#             self.visits = 0
#             self.reward = 0
#             self.e = Engine()
#             self.e.p1_mask = self.state[0]
#             self.e.p2_mask = self.state[1]
#             self.e.is_p2_turn = self.state[2]

#         def isFullyExpanded(self):
#             return len(self.children) == len(self.e.results(self.e.actions()))
        
#         def isGoal(self):
#             return self.e.is_goal()
        
#         def getLegalMoves(self):
#             return self.e.results(self.e.actions())
        
#         def updateState(self, move):
#             self.e.update_state(move)
#             self.state = self.e.game_state
#             self.player = self.state[2]
        
#         def setToInitialState(self):
#             self.e.p1_mask = self.initial_state[0]
#             self.e.p2_mask = self.initial_state[1]
#             self.e.is_p2_turn = self.initial_state[2]
#             self.state = self.e.game_state
    
#     def move(self):
#         e = Engine()
#         e.p1_mask = self._engine.p1_mask
#         e.p2_mask = self._engine.p2_mask
#         e.is_p2_turn = self._engine.is_p2_turn
#         root_node = self.Node(e.game_state)
#         self.mcts(root_node)
#         i = 0
#         for child in root_node.children.values():
#             print(f"{i}: visits: {child.visits} reward: {child.reward}")
#             i += 1
#             # print(f"winrate: {child.reward / child.visits}")
#         # sys.exit()
#         best_move = max(root_node.children.items(), key=lambda item: item[1].reward)[0]
#         # best_move = max(
#         #     root_node.children.items(),
#         #     key=lambda item: (item[1].reward / item[1].visits if item[1].visits != 0 else -float('inf'))
#         # )[0]
#         print(f"best move: {best_move}")
#         return self._engine.update_state(np.array(best_move))
    
#     def mcts(self, root_node):
#         for _ in range(self.iterations):
#             selected_node = self.select(root_node)
            
#             if selected_node.isGoal():
#                 if root_node.player != selected_node.player:
#                     reward = 1
#                 else:
#                     reward = 0
#             else:
#                 reward = self.simulate(root_node, selected_node)
#                 # print(f"reward: {reward}")
#             self.backpropagate(root_node,selected_node, reward)
#             # print(f"iteration {_}, reward: {root_node.reward}")
#         # sys.exit()
        
#     def select(self, node):
#         while not node.isGoal():
#             if not node.isFullyExpanded():
#                 return self.expand(node)
#             else:
#                 node = self.bestChild(node)
#         return node

#     def expand(self, node):
#         legal_moves = node.getLegalMoves()
#         for move in legal_moves:
#             move_tuple = tuple(map(tuple, move))  # Convert numpy.ndarray to tuple
#             if move_tuple not in node.children:
#                 node.updateState(move)
#                 child_node = self.Node(node.state, parent=node)
#                 node.children[move_tuple] = child_node
#                 node.setToInitialState()
#                 # sys.exit()
#                 return child_node
#         return None

#     def bestChild(self, node):
#         max_uct = -float('inf')
#         best = None
#         for child in node.children.values():
#             if child.visits == 0:
#                 uct = float('inf')
#             else:
#                 exploitation = child.reward / child.visits
#                 exploration = self.explorationWeight * math.sqrt(math.log(node.visits) / child.visits)
#                 uct = exploitation + exploration
#             if uct > max_uct:
#                 max_uct = uct
#                 best = child
#         return best
    
#     def simulate(self, root_node, selected_node, max_depth=100):
#         depth = 0
#         while not selected_node.isGoal():
#             if selected_node.player:
#                 heuristic = self.heuristic.T
#             else:
#                 heuristic = self.heuristic
                
#             if depth >= max_depth:
#                 # print("Max Depth Reached")
#                 if root_node.player:
#                     player_dist = np.sum(heuristic[None] * selected_node.state[1])
#                     opponent_dist = np.sum(heuristic[None]  * selected_node.state[0])
#                     return 1 if player_dist < opponent_dist else 0
#                 else:
#                     player_dist = np.sum(heuristic[None] * selected_node.state[0])
#                     opponent_dist = np.sum(heuristic[None]  * selected_node.state[1])
#                     return 1 if player_dist < opponent_dist else 0
            
#             legal_moves = selected_node.getLegalMoves()
      
#             heuristic_all = np.sum(heuristic * legal_moves, axis=(1,2))
#             best_moves_index = np.where(heuristic_all == np.min(heuristic_all))
#             move = legal_moves[np.random.choice(best_moves_index[0])] 
#             selected_node.updateState(move)
#             depth = depth + 1
#             # print()
#             # print(f"depth {depth} of selected_node")
#             # print(selected_node.state[0])
#             # print(selected_node.state[1])
#             # print(selected_node.state[2])
            
#         if root_node.player != selected_node.player:
#             # print("P2 Wins")
#             return 1
#         else:
#             # print("P1 Wins")
#             return 0

#     def backpropagate(self, root_node, selected_node, reward):
#         while selected_node is not None:
#             selected_node.visits += 1
#             selected_node.reward += reward
#             selected_node = selected_node.parent
    

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
