"""
An abstract class for 2 player games
A GameState describes a single instance in time of some game
"""
class GameState:

    """
    Takes:
        turn: the player who made the most recent move
        recent_move: the most recent move. This is useful for identifying a winner

    """
    def __init__(self, turn, recent_move):
        self.turn = turn
        self.recent_move = recent_move

    """
    Returns the player who made the most recent move
    """
    def get_turn(self):
        return self.turn

    """
    Returns an iterable of next GameStates
    Takes:
        
    """
    def generate_next_states(self):
        raise NotImplementedError

    """
    Returns the winner if there is a winner
    Returns 0 if there is no winner
    """
    def get_winner(self):
        raise NotImplementedError

    """
    An immutable object that represents the GameState
    Should be able to differentiate between GameStates
    """
    def get_all_features(self):
        raise NotImplementedError

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.get_all_features() == other.get_all_features())