from boardstate import BoardState
import random
import math

class Node(object):
    def __init__(self, board_state, score=0, visited=0, parent=None, children=None):
        assert isinstance(board_state, BoardState), "state is not a BoardState"
        assert parent is None or isinstance(parent, Node), "parent is not a Node"
        self.board_state = board_state
        self.turn = board_state.turn()  # the value of the person who just went
        self.score = score
        self.visited = visited
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children

    def get_board_state(self):
        return self.board_state

    def get_turn(self):
        return self.turn

    def get_score(self):
        return self.score

    def get_visited(self):
        return self.visited

    def get_mean_payout(self):
        return float(self.score) / float(self.visited)

    def increment_score(self):
        self.score += 1

    def increment_visited(self):
        self.visited += 1

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def add_child(self, child):
        assert isinstance(child, Node), "child is not a Node"
        self.children.append(child)

    def ucb1(self, child):
        return child.get_mean_payout() + pow(2 * math.log(self.visited, 2) / child.get_visited(), 1/2)

    def best_child(self):
        assert len(self.children) > 0, "node has no children"
        best_child = self.children[0]
        best_score = self.ucb1(best_child)
        for child in self.children:
            score = self.ucb1(child)
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

    # TODO - make this algorithm more efficient
    # returns the winner of a random simulation
    def run_simulation(self, distance_bound=1):
        node_bs = self.board_state
        while node_bs.get_winner() == 0:
            coordinates = node_bs.filtered_empty(distance_bound)
            # it is a tie
            if len(coordinates) == 0:
                return 0
            y, x = random.choice(coordinates)
            state = node_bs.get_state()
            state[y][x] = node_bs.next_turn()
            node_bs = BoardState(state)
        return node_bs.get_winner()

    def backprop(self, winner):
        self.increment_visited()
        if self.turn == winner:
            self.increment_score()
        if self.parent is not None:
            self.parent.backprop(winner)

    def __str__(self):
        return "[Turn: {0}, Score: {1}, Visited: {2}, Mean Payout: {3}]".format(self.turn, self.score, self.visited, self.get_mean_payout())


class GameTree(object):
    def __init__(self, top_node, distance_bound=1):
        assert isinstance(top_node, Node), "top_node is not a Node"
        self.top_node = top_node
        self.distance_bound = distance_bound

    def expand_node(self, node):
        node_bs = node.get_board_state()
        coordinates = node_bs.filtered_empty(self.distance_bound)
        for y, x in coordinates:
            state = node_bs.get_state()
            state[y][x] = node_bs.next_turn()
            board_state = BoardState(state)
            child = Node(board_state, parent=node)

            winner = child.run_simulation(self.distance_bound)
            child.backprop(winner)
            node.add_child(child)

    @staticmethod
    def get_best_leaf(node):
        if len(node.get_children()) == 0:
            return node
        return GameTree.get_best_leaf(node.best_child())

    @staticmethod
    def get_depth(node):
        if len(node.get_children()) == 0:
            return 1
        child_depth = 0
        for child in node.get_children():
            child_depth = max(child_depth, GameTree.get_depth(child))
        return 1 + child_depth

    def build_tree(self, depth=5):
        self.expand_node(self.top_node)
        while self.get_depth(self.top_node) < depth:
            best_leaf = self.get_best_leaf(self.top_node)
            print(best_leaf.get_board_state())
            self.expand_node(best_leaf)

        print("top node mean payout ", self.top_node.get_mean_payout())
        print(self.top_node.best_child().get_board_state())

    def best_move(self, depth=5):
        self.build_tree(depth)
        return self.top_node.best_child().get_board_state()

    def __str__(self):
        out = ""
        queue = [self.top_node]
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


bs = BoardState(state=[[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [ 0, 0, 0,-1, 1,-1, 0, 0, 0],
                       [ 0, 0, 0,-1, 1,-1, 0, 0, 0],
                       [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0, 0]])

tn = Node(bs)
gt = GameTree(tn, distance_bound=2)

print(gt.best_move(4))


