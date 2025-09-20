from flask import Flask, jsonify, request
from flask_cors import CORS
import gamestate
import gameengine
from Bots.randomBot import RandomBot

app = Flask(__name__)
CORS(app)

players = [None, RandomBot(),RandomBot(),RandomBot()]
is_bot_list = [1 if player is not None else 0 for player in players]
game_state = gamestate.GameState(is_bot_list) 
game_engine = gameengine.GameEngine(game_state, players)

                                    
@app.route("/api/spielzustand", methods=["GET"])
def get_spielzustand():
    """
    It sends the actual gamestate periodically to the browser
    """
    game_state_dict = game_state.to_dict()
    
    # Wandel das Dictionary in eine JSON-Antwort um und sende sie
    return jsonify(game_state_dict)

@app.route("/api/spielzug", methods=["POST"])
def mache_spielzug():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No Data received"}), 400

    action = data.get('action')
    payload = data.get('payload')

    move_successful = game_engine.apply_move(action, payload)

    if move_successful:
        return jsonify({
            "message": "success",
            "state": game_state.to_dict()
        })
    else:
        return jsonify({
            "message": "fail",
            "state": game_state.to_dict()
        })

# Starte die App (für die Entwicklung)
if __name__ == '__main__':
    app.run(debug=True , port=8080)