from mcts_node import MCTSNode


class MCTSTree(object):
    def __init__(self, top):
        assert isinstance(top, MCTSNode), "top is not a MCTSNode"
        self.top = top

    @staticmethod
    def expand_node(node):
        assert isinstance(node, MCTSNode)
        assert node.get_state().get_winner() == 0, "cannot expand end state"
        print("Expanding...\n" + node.get_state().__str__())
        state = node.get_state()
        next_states = state.generate_next_states()
        for next_state in next_states:
            print("child state: \n" + next_state.__str__())
            child = MCTSNode(state=next_state, parent=node, depth=node.depth+1)
            winner = child.run_simulation()
            print("winner: ", winner, "\n---")
            child.backprop(winner)
            node.add_child(child)

        MCTSTree.update_depth(node, 1)

    @staticmethod
    def get_best_leaf(node):
        assert isinstance(node, MCTSNode)
        if len(node.get_children()) == 0:
            return node
        return MCTSTree.get_best_leaf(node.best_ucb1_child())

    @staticmethod
    def update_depth(node, depth):
        assert isinstance(node, MCTSNode)
        if node.get_depth() < depth:
            node.set_depth(depth)
            parent = node.get_parent()
            if parent is not None:
                MCTSTree.update_depth(parent, node.get_depth())

    def build_tree(self, depth=5):
        self.expand_node(self.top)
        tree_depth = self.top.get_depth()
        while tree_depth < depth:
            print("tree depth: ", tree_depth, " depth: ", depth)
            best_leaf = self.get_best_leaf(self.top)
            # if best leaf is an end state
            if best_leaf.get_state().get_winner() != 0:
                winner = best_leaf.get_state().get_winner()
                best_leaf.backprop(winner)
                continue
            self.expand_node(best_leaf)
            tree_depth = max(tree_depth, best_leaf.get_depth())

    def best_move(self, depth=5):
        self.build_tree(depth)
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

