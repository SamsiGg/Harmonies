import config # Assuming you have a config.py file
import objects
import player
from player import Player
import components
from enum import Enum, auto
from typing import Set
import copy
import os

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

        self.last_round = False

        self.winner: Player = None

        self.players: list[player.Player] = []
        for i,is_bot in enumerate(is_bot_list):
            board = player.Board(self.board_type)
            self.players.append(player.Player(board,i,is_bot))

        self.current_move = {
            'token_group_index': 0,
            'tile_token_placed': [],
            'token_order': [],
            'dice_positions': [],
            'animal_name': ''
        }

    def empty_move(self):
        self.current_move = {
            'token_group_index': 0,
            'tile_token_placed': [],
            'token_order': [],
            'dice_positions': [],
            'animal_name': ''
        }

    def copy(self):
        return copy.deepcopy(self)
    
    def undo_token_placing(self):
        """
        Undoes placing the tokens, done on this gamestate.
        """
        token_hand = self.get_current_player().token_hand.tokens
        for tile in self.current_move['tile_token_placed']:
            token_hand.insert(0, tile.take_top_token())

        self.current_move['tile_token_placed'] = []

        if TurnAction.TOKENS_PLACED in self.completed_moves_this_turn:
            self.completed_moves_this_turn.remove(TurnAction.TOKENS_PLACED)


    def undo_dice_placing(self):
        """
        Undoes placing any amount of dice
        """
        for die_position in self.current_move['dice_positions']:
            for tile in self.get_current_player().board.tiles:
                if tile.position is die_position:
                    print(die_position)
                    print(tile.has_die)
                    tile.has_die = False
        self.current_move['dice_positions'] = []


    def to_dict(self):
        return {
            'pentagon': self.pentagon.to_dict(),
            'animalStack': self.animal_stack.to_dict(),
            'animalDisplay': self.animal_display.to_dict(),
            'players': [player.to_dict() for player in self.players],
            'currentPlayerIndex': self.current_player_index,
            'winner': '' if self.winner == None else self.winner.index
        }

    def get_current_player(self) -> player.Player:
        return self.players[self.current_player_index]

    def next_player(self):
        if self.current_player_index >= len(self.players) - 1:
            if self.last_round:
                self._determine_winner()
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def _determine_winner(self):
        for player in self.players:
            if not self.winner:
                self.winner = player

            if player.score > self.winner.score:
                self.winner = player

            if player.score == self.winner.score:
                player_dice = 0
                winner_dice = 0

                for tile in player.board.tiles:
                    if tile.has_die:
                        player_dice += 1
                
                for tile in self.winner.board.tiles:
                    if tile.has_die:
                        winner_dice += 1

                if player_dice > winner_dice:
                    self.winner = player


    def refill_animal_display(self):
        missing_amount = self.animal_display.max_amount-len(self.animal_display.animals)
        animals = self.animal_stack.draw_cards(missing_amount)

        for animal in animals:
            self.animal_display.add_animal(animal)

    def refill_pentagon(self):
        tokens = self.pouch.take_out_tokens(3)
        self.pentagon.add_token_group(tokens)

    def finish_move(self):

        if (TurnAction.TOKENS_PLACED in self.completed_moves_this_turn):
            if self._check_end_condition():
                self.last_round = True
            self.completed_moves_this_turn.clear()
            self.next_player()
            self.refill_animal_display()
            self.refill_pentagon()
            self.empty_move()
            if self.winner:
                print('There is a winner: Player' + str(self.winner.index) + ' with ' + str(self.winner.score) + ' points!')
            return True

        return False
    
    def _check_end_condition(self):
        for player in self.players:
            if player.two_empty_tiles():
                return True
            
        if len(self.pouch.tokens) <= 2:
            return True
        
        return False