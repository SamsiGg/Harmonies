from gamestate import GameState, TurnAction

def take_token_group(game_state: GameState, index):

    if (TurnAction.TOKENS_TAKEN not in game_state.completed_moves_this_turn):  
        
        tokens = game_state.pentagon.take_token_group(index)
        
        game_state.get_current_player().token_hand.set_token_group(tokens)

        if tokens == None:
            return False
        
        game_state.completed_moves_this_turn.add(TurnAction.TOKENS_TAKEN)
        return tokens
    
def place_token(game_state: GameState, token_id, tile_position):

    if(TurnAction.TOKENS_PLACED not in game_state.completed_moves_this_turn):

        token = game_state.get_current_player().token_hand.take_token(token_id)
        if token is None:
            return False
        
        if len(game_state.get_current_player().token_hand.tokens) == 0:
            game_state.completed_moves_this_turn.add(TurnAction.TOKENS_PLACED)

        for tile in game_state.get_current_player().board.tiles:
            if tile.position[0] == tile_position[0] and tile.position[1] == tile_position[1]:
                return tile.add_token(token)
    
    return False

def reposition_token(self, game_state: GameState):
    ... # TODO

def take_animal(game_state: GameState, animal_name):
    if(TurnAction.ANIMAL_TAKEN not in game_state.completed_moves_this_turn
       and len(game_state.get_current_player().animals) < 4):
    
        animal = game_state.animal_display.get_animal(animal_name)
        if(animal is None):
            return False
    
        if game_state.get_current_player().add_animal(animal):
            game_state.completed_moves_this_turn.add(TurnAction.ANIMAL_TAKEN)
            return True
        
        return False

def finish_move(game_state: GameState):

    if (TurnAction.TOKENS_PLACED in game_state.completed_moves_this_turn):
        game_state.completed_moves_this_turn.clear()
        game_state.next_player()
        game_state.refill_animal_display()
        game_state.refill_pentagon()
        return True

    return False

    

