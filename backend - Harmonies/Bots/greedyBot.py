import os
from gamestate import GameState
import moves
from Bots.bot import Bot
import random
import config
from itertools import permutations
import time
from score_calculator import ScoreCalculator

class GreedyBot(Bot):

    def calculate_move(self, game_state: GameState):
        highest_score = -1
        game_state_copy: GameState = game_state.copy()
        score_calculator = ScoreCalculator()
        starttime = time.time()

        for animal in game_state.animal_display.animals:
            moves.take_animal(game_state_copy, animal.name)
            for token_group_index, token_group in enumerate(game_state.pentagon.token_groups):
                moves.take_token_group(game_state_copy,token_group_index)
                #for position0 in config.TILE_POSITIONS['yellow']:
                    #for position1 in config.TILE_POSITIONS['yellow']:
                position0 = (0,0)
                position1 = (0,1)

                for position2 in config.TILE_POSITIONS['yellow']:

                    positions = [position0, position1, position2]
                    token_orders = permutations([0,1,2])

                    for token_order in token_orders:

                        game_state_copy.get_current_player().token_hand.sort_tokens(token_order)
                        
                        moves.place_token(game_state_copy, 0, positions[0])
                        moves.place_token(game_state_copy, 0, positions[1])
                        moves.place_token(game_state_copy, 0, positions[2])
                        
                        for tile in game_state_copy.get_current_player().board.tiles:
                            moves.place_die(game_state_copy, tile.position)

                        game_state_copy.get_current_player().score = score_calculator.calculate_total_score(game_state_copy.get_current_player())
                        
                        if (game_state_copy.get_current_player().score > highest_score
                            and len(game_state_copy.get_current_player().token_hand.tokens) == 0):
                            highest_score = game_state_copy.get_current_player().score
                            print(highest_score)
                            print(positions)
                            print(token_order)
                            self.best_move = {
                                'token_group_index': token_group_index,
                                'tile_positions': positions,
                                'token_order': token_order,
                                'animal_name': animal.name
                            }

                        game_state_copy.undo_dice_placing()
                        game_state_copy.undo_token_placing()

            print('Zeit pro Tier: ' + str(time.time() - starttime))

    def place_taken_tokens(self, game_state: GameState):

        current_player = game_state.get_current_player()

        moves.take_token_group(game_state, self.best_move['token_group_index'])
        
        if len(current_player.token_hand.tokens) == 3:
            token_order = self.best_move['token_order']
            print(token_order) #HIER WEITERMACHEN ------------------ TROTZ RICHTIGER TOKENOERDER WERDEN DIE TOKENS NUR IN (0,1,2) ORDER GESETZT
            game_state.get_current_player().token_hand.sort_tokens(token_order)
            for i in range(3):
                tile_position = self.best_move['tile_positions'][i]
                moves.place_token(game_state, 0, tile_position)

    def take_animal(self, game_state):
        moves.take_animal(game_state, self.best_move['animal_name'])