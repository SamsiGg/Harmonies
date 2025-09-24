import time
import moves
from gamestate import GameState, TurnAction
from Bots.bot import Bot
from score_calculator import ScoreCalculator

class GameEngine():

    def __init__(self, game_state: GameState, players: list[Bot], on_state_change=None, socketio=None):

        self.game_state = game_state
        self.players = players
        self.on_state_change = on_state_change
        self.socketio = socketio

    def _trigger_update(self):
        if self.on_state_change:
            print('update')
            self.on_state_change(self.game_state.to_dict())

    def get_valid_moves(self):
        exit

    def apply_move(self, action, payload):

        move_successful = False

        if (not self.game_state.get_current_player().is_bot):

            if (action == 'TokenGroupClick'):
                move_successful = moves.take_token_group(self.game_state, payload.get('index'))
                
            if (action == 'DragDropToken' and payload.get('player_index') == self.game_state.current_player_index):
                draggedItem = payload.get('draggedItem')
                dropItem = payload.get('dropItem')

                if(draggedItem.get('type') == 'token_hand_token'):
                    move_successful = moves.place_token(self.game_state, 
                                                        draggedItem.get('id'),
                                                        dropItem.get('position'))

                if(draggedItem.get('type') == 'tile_token'):
                    move_successful = moves.reposition_token(self.game_state)
                
            if (action == 'PlayerDisplayImageClick'):
                move_successful = moves.take_animal(self.game_state, payload.get('name'))
                
            if (action == 'FinishMove' and payload.get('player_index') == self.game_state.current_player_index):
                move_successful = moves.finish_move(self.game_state)

                self.run_bot_turn_if_needed()

            if (action == 'PlaceDie'):
                position = payload.get('position')
                x = position.get('x')
                y = position.get('y')
                move_successful = moves.place_die(self.game_state, (x,y))

        if (action == 'StartGame'):
            print('alskjdflöasf')
            self.run_bot_turn_if_needed()
            move_successful = True

        self._trigger_update()
        return move_successful
    
    def run_bot_turn_if_needed(self):
        current_player_index = self.game_state.current_player_index

        if self.players[current_player_index] is None:
            return
        
        self.players[current_player_index].make_turn(self.game_state)
        self._trigger_update()

        self.socketio.sleep(0.5)

        if not self.game_state.winner:
            self.run_bot_turn_if_needed()


