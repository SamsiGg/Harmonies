import config # Assuming you have a config.py file

class Player():
    """
    Represents a single player in the game, holding their personal board.

    Args:
        board (Board): The specific Board object assigned to this player.
    """
    def __init__(self, board):
        self.board = board
        self.animals = []
        self.token_hand = TokenHand()

class TokenHand():

    def __init__(self):
        self.tokens = []

    def get_token_group(self, token_group):
        self.tokens = token_group
    
class Board():
    """
    Represents a player's personal hexagonal game board, composed of
    individual Tile objects.

    Args:
        board_type (str): A string identifier for the board layout, which
                          determines its dimensions from the config file.
    """
    def __init__(self, board_type):
        if board_type not in config.ALLOWED_BOARD_TYPES:
            raise ValueError(f'Board was given the wrong board type: "{board_type}"')

        for key, positions in config.BOARD_POSITIONS.items():
            if board_type == key:
                self.tiles = []
                for pos in positions:
                    self.tiles.append(Tile(pos))

class Tile():
    """
    Represents a single hexagonal tile on a player's board. It has a
    position and can hold tokens.

    Args:
        position (tuple): The (x, y) coordinates of the tile on the board.
    """
    def __init__(self, position: tuple):
        self.tokens = []
        self.position = position
        self.dice = False

    def __repr__(self):
        if len(self.tokens) == 0:
            return '<Tile: empty>'
        return f'Tile: "{self.tokens}"'
    
class AnimalDisplay():

    def __init__(self):
        self.animals = []
