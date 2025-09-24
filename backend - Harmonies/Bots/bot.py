from abc import ABC, abstractmethod
from gamestate import GameState
import moves

class Bot(ABC):

    def __init__(self):
        super().__init__()

    def make_turn(self, game_state: GameState):
        self.place_taken_tokens(game_state)
        self.take_animal(game_state)
        for tile in game_state.get_current_player().board.tiles:
            moves.place_die(game_state, tile.position)
        moves.finish_move(game_state)

    @abstractmethod
    def place_taken_tokens(self):
        pass

    @abstractmethod
    def take_animal(self):
        pass