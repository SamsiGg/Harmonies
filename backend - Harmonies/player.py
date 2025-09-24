from __future__ import annotations
import config
from objects import Token, Animal
from typing import TYPE_CHECKING


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

        from score_calculator import ScoreCalculator
        self.score_calculator = ScoreCalculator()
        self.score = 0

    def to_dict(self):
        self.score = self.score_calculator.calculate_total_score(self)
        player_dict = {
            'board': self.board.to_dict(),
            'animals': [animal.to_dict() for animal in self.animals],
            'tokenHand': self.token_hand.to_dict(),
            'index': self.index,
            'isBot': self.is_bot,
            'score': self.score
        }
        return player_dict
    
    def add_animal(self, animal: Animal):
        self.animals.append(animal)
        return True
    
    def place_die(self, position: tuple):
        for tile in self.board.tiles:
            if(tile.position == position):
                clicked_tile = tile
                break
        
        for animal in self.animals:
            placeable = animal.die_placeable(position, self.board)
            if placeable and animal.dice_amount > 0:
                animal.take_die()
                clicked_tile.set_die()
                return True

        return False
    
    def two_empty_tiles(self):
        amount_empty = 0
        for tile in self.board.tiles:
            if len(tile.tokens) == 0:
                amount_empty += 1

        if amount_empty <= 2:
            return True
        
        return False
        

class TokenHand():

    def __init__(self):
        self.tokens: list[Token] = []

    def set_token_group(self, token_group):
        self.tokens = token_group

    def delete_token(self, index):
        self.tokens.pop(index)
    
    def read_token(self, index):
        return self.tokens[index]

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
        self.tokens: list[Token] = []
        self.position = position
        self.has_die = False

    def __repr__(self):
        if len(self.tokens) == 0:
            return '<Tile: empty>'
        return f'Tile: "{self.position}"'
    
    def to_dict(self):
        tile_dict = {
            'tokens': [token.to_dict() for token in self.tokens],
            'position': {
                'x': self.position[0],
                'y': self.position[1]
            },
            'die': self.has_die
        }
        return tile_dict
    
    def check_if_add_token_valid(self, token: Token):

        if self.has_die:
            return False

        #Free Tile: valid
        if len(self.tokens) == 0:
            return True
        
        #Already three high: invalid
        if len(self.tokens) >= 3:
            return False
        
        new_color = token.type
        old_color = self.tokens[-1].type
        
        #No three-stack of brown allowed
        if len(self.tokens) == 2 and old_color == 'brown' and new_color == 'brown':
                return False
        
        #Red is only allowed to be placed at position 0 and 1
        if new_color == 'red' and len(self.tokens) == 2:
            return False

        #check if color underneath allows placement
        allowed_colors_underneath = config.ALLOWED_STACKS.get(new_color, set())
        
        return old_color in allowed_colors_underneath
    
    def add_token(self, token: Token):
        if self.check_if_add_token_valid(token):
            self.tokens.append(token)
            return True
        return False
    
    def set_die(self):
        self.has_die = True
