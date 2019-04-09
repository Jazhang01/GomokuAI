import math
from gamestate import GameState

"""
A MCTSNode contains a GameState
Contains info for MCTS
"""
class MCTSNode(object):
    """
    Takes:
    state: a GameState
    parent: the parent MCTSNode of self. If this node is the top, the parent is None
    children: list of children MCTSNodes
    score: the number of wins by the player who made the last move
    visited: the number of times this node was visited
    """
    def __init__(self, state, parent=None, children=None, score=0, visited=0, depth=0):
        assert isinstance(state, GameState)
        assert isinstance(parent, MCTSNode) or parent is None
        # internal variables
        self.state = state
        self.score = score
        self.visited = visited
        self.depth = depth
        # connects to other nodes
        self.parent = parent
        self.children = children if children is not None else []

    def get_score(self):
        return self.score

    def get_visited(self):
        return self.visited

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_depth(self):
        return self.depth

    def set_depth(self, depth):
        self.depth = depth

    def add_child(self, child):
        assert isinstance(child, MCTSNode), "child is not a MCTSNode"
        self.children.append(child)

    """
    returns the mean payout of this node
    the mean payout is the score divided by the number of times it was visited
    """
    def mean_payout(self):
        return float(self.score) / float(self.visited)

    """
    Upper confidence bound 1. Used to choose the best child.
    """
    def ucb1(self, child):
        return child.mean_payout() + pow(2 * math.log(self.visited, 2) / child.get_visited(), 1/2)

    """
    returns child with greatest mean payout
    """
    def best_child(self):
        assert len(self.children) > 0, "node had no children"
        best_child = self.children[0]
        best_score = best_child.mean_payout()
        for child in self.children:
            score = child.mean_payout()
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

    """
    returns the child with the greatest UCB1
    """
    def best_ucb1_child(self):
        assert len(self.children) > 0, "node has no children"
        best_ucb1_child = self.children[0]
        best_score = self.ucb1(best_ucb1_child)
        for child in self.children:
            score = self.ucb1(child)
            if score > best_score:
                best_ucb1_child = child
                best_score = score
        return best_ucb1_child

    """
    returns the winner of a random simulation
    """
    def run_simulation(self):
        state = self.state
        while state.get_winner() == 0:
            state = state.random_next_state()
            # it is a tie
            if state is None:
                return 0
        return state.get_winner()

    """
    Back-propagation of the results of a simulation
    Takes:
        winner: the player who won in the simulation
    This node, and all nodes to this node, have their visited incremented by 1
    If the player of this node won, the score is incremented by 1
    """
    def backprop(self, winner):
        self.visited += 1
        if self.state.get_turn() == winner:
            self.score += 1
        if self.parent is not None:
            self.parent.backprop(winner)

    def __str__(self):
        return "\n[Depth: {0}, Turn: {1}, Score: {2}, Visited: {3}, Mean Payout: {4}]".format(
                   self.depth, self.state.get_turn(), self.score, self.visited, self.mean_payout())
