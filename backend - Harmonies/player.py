from __future__ import annotations
import config # Assuming you have a config.py file
from objects import Token, Animal

class Player():
    """
    Represents a single player in the game, holding their personal board.

    Args:
        board (Board): The specific Board object assigned to this player.
    """
    def __init__(self, board: Board, index, is_bot: bool):
        self.board = board
        self.animals: list[Animal] = []
        self.token_hand = TokenHand()
        self.index = index
        self.is_bot = is_bot

    def to_dict(self):
        player_dict = {
            'board': self.board.to_dict(),
            'animals': [animal.to_dict() for animal in self.animals],
            'tokenHand': self.token_hand.to_dict(),
            'index': self.index,
            'isBot': self.is_bot
        }
        return player_dict
    
    def add_animal(self, animal: Animal):
        self.animals.append(animal)
        return True

class TokenHand():

    def __init__(self):
        self.tokens: list[Token] = []

    def set_token_group(self, token_group):
        self.tokens = token_group

    def take_token(self, index):
        token = self.tokens.pop(index)
        return token

    def to_dict(self):
        return [token.to_dict() if token is not None else None for token in self.tokens]
    
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

        for key, positions in config.TILE_POSITIONS.items():
            if board_type == key:
                self.tiles: list[Tile] = []
                for pos in positions:
                    self.tiles.append(Tile(pos))

    def to_dict(self):
        return [tile.to_dict() for tile in self.tiles]

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
    
    def to_dict(self):
        tile_dict = {
            'tokens': [token.to_dict() for token in self.tokens],
            'position': {
                'x': self.position[0],
                'y': self.position[1]
            },
            'dice': int(self.dice)
        }
        return tile_dict
    
    def check_if_add_token_valid(self, token: Token):
        return True # TODO
    
    def add_token(self, token: Token):
        if self.check_if_add_token_valid(token):
            self.tokens.append(token)
            return True
        return False
