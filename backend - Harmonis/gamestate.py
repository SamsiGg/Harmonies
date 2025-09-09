import config # Assuming you have a config.py file
import objects
import player
import components
from enum import Enum, auto

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
    def __init__(self, player_amount = 4, board_type = 'yellow'):
        self.pouch = components.Pouch()
        self.pentagon = components.Pentagon(self.pouch.take_out_tokens(15))
        self.animal_stack = components.AnimalStack()
        self.animal_display = components.AnimalDisplay(self.animal_stack.draw_cards(1))

        self.current_player_index = 0
        self.completed_moves_this_turn = set()

        self.players = [] # Add all the players and give them their board
        for _ in range(player_amount):
            board = player.Board(board_type)
            self.players.append(player.Player(board))

    def to_dict(self): # TODO
        # Diese Methode wandelt deinen Spielzustand in ein Dictionary um
        return {
            "board": [
                [{"type": "forest"}, {"type": "water"}],
                [{"type": "mountain"}, {"type": "grass"}]
            ],
            "currentPlayer": "Anna",
            "scores": {"Anna": 10, "Ben": 12}
        }

    def get_current_player(self) -> player.Player:
        return self.players[self.current_player_index]
    
    def player_takes_tokens_from_pentagon(self, token_group_index):
        token_group = self.pentagon.token_groups[token_group_index]
        player = self.get_current_player()

        player.token_hand.get_token_group(token_group)
        self.completed_actions_this_turn.add(TurnAction.TOKENS_TAKEN)
    
    def player_places_token_on_board(self, tile_position):
        ... # TODO
        

if __name__ == "__main__":
    t = objects.Token('green')
    g = GameState(4, 'yellow')
    g.pentagon.token_groups[0][1] = t

    print('Anwser: ' + str(g.animal_stack.animals[0].rotate_next((2*config.C,2),60,15)))