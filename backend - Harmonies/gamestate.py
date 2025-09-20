import config # Assuming you have a config.py file
import objects
import player
import components
from enum import Enum, auto
from typing import Set

class TurnAction(Enum):
    TOKENS_TAKEN = auto()  # Was a token group taken from the pentagon
    TOKENS_PLACED = auto() # Were all three tokens placed from the token-hand
    ANIMAL_TAKEN = auto()

class GameState():
    """
    Represents the entire state of a single game instance, including all
    players, the board components, and game variables.

    Args:
        player_amount (int): The number of players that will participate in the game.
        board_type (str): The type of board to create for each player (e.g., 'yellow').
    """
    def __init__(self, is_bot_list: list[bool] = [], board_type = 'yellow'):
        self.board_type = board_type

        self.pouch = components.Pouch()
        self.pentagon = components.Pentagon(self.pouch.take_out_tokens(15))
        self.animal_stack = components.AnimalStack()
        self.animal_display = components.AnimalDisplay(self.animal_stack.draw_cards(5))

        self.current_player_index = 0
        self.completed_moves_this_turn: Set[TurnAction] = set()

        self.players: list[player.Player] = []
        for i,is_bot in enumerate(is_bot_list):
            board = player.Board(self.board_type)
            self.players.append(player.Player(board,i,is_bot))

    def to_dict(self):
        return {
            'pentagon': self.pentagon.to_dict(),
            'animalStack': self.animal_stack.to_dict(),
            'animalDisplay': self.animal_display.to_dict(),
            'players': [player.to_dict() for player in self.players],
            'currentPlayerIndex': self.current_player_index
        }

    def get_current_player(self) -> player.Player:
        return self.players[self.current_player_index]

    def next_player(self):
        if self.current_player_index >= len(self.players) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def refill_animal_display(self):
        missing_amount = self.animal_display.max_amount-len(self.animal_display.animals)
        animals = self.animal_stack.draw_cards(missing_amount)

        for animal in animals:
            self.animal_display.add_animal(animal)

    def refill_pentagon(self):
        tokens = self.pouch.take_out_tokens(3)
        self.pentagon.add_token_group(tokens)