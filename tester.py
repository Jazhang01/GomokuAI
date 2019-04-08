from gomoku_state import BoardState
from mcts_node import MCTSNode
from mcts_tree import MCTSTree

nineteen = [[0 for i in range(19)] for j in range(19)]
nineteen[8][8] = 1

bs = BoardState(grid=[[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [ 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                turn=1, recent_move=(4, 4), search_breadth=1)

bs2 = BoardState(grid=nineteen, turn=1, recent_move=(8, 8), search_breadth=2)

n = MCTSNode(bs2)
t = MCTSTree(n)

print("Best Move: \n", t.best_move(3))
