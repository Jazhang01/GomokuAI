from mcts_node import MCTSNode


class MCTSTree(object):
    def __init__(self, top):
        assert isinstance(top, MCTSNode), "top is not a MCTSNode"
        self.top = top

    @staticmethod
    def expand_node(node):
        assert isinstance(node, MCTSNode)
        state = node.get_state()
        next_states = state.generate_next_states()
        for next_state in next_states:
            child = MCTSNode(state=next_state, parent=node)
            winner = child.run_simulation()
            child.backprop(winner)
            node.add_child(child)

        MCTSTree.update_depth(node, 1)

    @staticmethod
    def get_best_leaf(node):
        assert isinstance(node, MCTSNode)
        if len(node.get_children()) == 0:
            return node
        return MCTSTree.get_best_leaf(node.best_child())

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
        while self.top.get_depth() < depth:
            best_leaf = self.get_best_leaf(self.top)
            self.expand_node(best_leaf)

    def best_move(self, depth=5):
        self.build_tree(depth)
        return self.top.best_child().get_state()