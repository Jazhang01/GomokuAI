from tkinter import *
from mcts_node import MCTSNode
import time

class MCTSTree(object):
    def __init__(self, top):
        assert isinstance(top, MCTSNode), "top is not a MCTSNode"
        self.top = top

    @staticmethod
    def expand_node(node):
        assert isinstance(node, MCTSNode)
        assert node.get_state().get_winner() == 0, "cannot expand end state"
        #print("Expanding...\n" + node.get_state().__str__())
        state = node.get_state()
        next_states = state.generate_next_states()
        for next_state in next_states:
            #print("child state: \n" + next_state.__str__())
            child = MCTSNode(state=next_state, parent=node)

            start = time.time()
            #winner = child.run_simulation() # TODO - instead of expanding all children, choose best one
            end = time.time()
            #print("rollout time: ", end - start)

            #print("winner: ", winner, "\n---")
            #child.backprop(winner) # TODO - instead of expanding all children, choose best one
            node.add_child(child)

        best_child = node.best_ucb1_child()
        print(best_child.get_state())
        winner = best_child.run_simulation()
        best_child.backprop(winner)

    @staticmethod
    def get_best_leaf(node):
        assert isinstance(node, MCTSNode)
        if len(node.get_children()) == 0:
            return node
        return MCTSTree.get_best_leaf(node.best_ucb1_child())

    def build_tree(self, time_cutoff=60):
        self.expand_node(self.top)
        start_time = time.time()
        end_time = time.time()
        while end_time - start_time < time_cutoff:
            best_leaf = self.get_best_leaf(self.top)
            # if best leaf is an end state
            if best_leaf.get_state().get_winner() != 0:
                winner = best_leaf.get_state().get_winner()
                best_leaf.backprop(winner)
                continue
            self.expand_node(best_leaf)
            end_time = time.time()
            print(end_time - start_time)

    def best_move(self, time_cutoff=60):
        self.build_tree(time_cutoff)
        return self.top.best_child().get_state()

    def __str__(self):
        out = ""
        queue = [self.top]
        while len(queue) > 0:
            node = queue[0]
            queue.pop(0)
            if len(node.get_children()) == 0:
                continue
            out += node.__str__() + "\n"
            for child in node.get_children():
                queue.append(child)
                out += "\t" + child.__str__() + "\n"
        return out

