from gamestate import GameState, TurnAction

def take_token_group(game_state: GameState, index):

    if (TurnAction.TOKENS_TAKEN not in game_state.completed_moves_this_turn):  
        
        tokens = game_state.pentagon.take_token_group(index)

        if tokens == None:
            return False
        
        game_state.get_current_player().token_hand.set_token_group(tokens)
        
        game_state.completed_moves_this_turn.add(TurnAction.TOKENS_TAKEN)
        return tokens
    
def place_token(game_state: GameState, token_index, tile_position):

    move_successful = False

    if(TurnAction.TOKENS_PLACED not in game_state.completed_moves_this_turn
       and len(game_state.get_current_player().token_hand.tokens) > 0):

        token = game_state.get_current_player().token_hand.read_token(token_index)
        
        for tile in game_state.get_current_player().board.tiles:
            if tile.position[0] == tile_position[0] and tile.position[1] == tile_position[1]:
                move_successful = tile.add_token(token)
                break

        if move_successful:
            game_state.get_current_player().token_hand.delete_token(token_index)
            game_state.current_move['tile_token_placed'].append(tile)
            
        if len(game_state.get_current_player().token_hand.tokens) == 0:
            game_state.completed_moves_this_turn.add(TurnAction.TOKENS_PLACED)
    
    return move_successful

def reposition_token(game_state: GameState):
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
    return False

def place_die(game_state: GameState, position: tuple):
    current_player = game_state.get_current_player()

    move_successful = current_player.place_die(position)

    if move_successful:
        game_state.current_move['dice_positions'].append(position)
        return True

    return False

