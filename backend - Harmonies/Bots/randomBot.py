from gamestate import GameState
import moves
from Bots.bot import Bot
import random
import config

class RandomBot(Bot):

    def calculate_move(self, game_state: GameState):
        ...

    def place_taken_tokens(self, game_state: GameState):
        pentagon = game_state.pentagon
        current_player = game_state.get_current_player()

        moves.take_token_group(game_state, random.randint(0,4))
        
        while(len(current_player.token_hand.tokens) > 0):
            moves.place_token(game_state, 
                              len(current_player.token_hand.tokens)-1, 
                              random.choice(list(config.TILE_POSITIONS[game_state.board_type])))

    def take_animal(self, game_state):
        animal = random.choice(game_state.animal_display.animals)
        moves.take_animal(game_state, animal.name)