from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from gamestate import GameState
from gameengine import GameEngine
from Bots.randomBot import RandomBot
from Bots.greedyBot import GreedyBot

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

players = [GreedyBot(), None, None ,None]
is_bot_list = [1 if player is not None else 0 for player in players]
game_state = GameState(is_bot_list) 

def send_update_to_clients(new_game_state):
    print(f"SERVER: Sende Update an Clients.")
    socketio.emit('update_game_state', new_game_state)

game_engine = GameEngine(
    game_state=game_state,
    players=players,
    on_state_change=send_update_to_clients,
    socketio=socketio
)
 
@socketio.on('player_move')
def handle_player_move(data):
    action = data.get('action')
    payload = data.get('payload')
    
    move_successful= game_engine.apply_move(action, payload)
    
    if not move_successful:
        socketio.emit('move_failed','fail', to=request.sid)

@socketio.on('connect')
def handle_connect():
    print(f"Ein Spieler hat sich verbunden! Sende initialen Spielzustand.")
    
    initial_game_state = game_engine.game_state.to_dict()

    socketio.emit('update_game_state', initial_game_state)

@socketio.on('disconnect')
def handle_disconnect():
    print('Ein Spieler hat die Verbindung getrennt.')

if __name__ == '__main__':
    socketio.run(app, port=8080, debug=True)