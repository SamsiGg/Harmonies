from flask import Flask, jsonify, request
from flask_cors import CORS
import gamestate

# --- HIER DEINE SPIEL-LOGIK IMPORTIEREN ---
# Angenommen, du hast eine Klasse Game in einer Datei game_logic.py
# from game_logic import Game

# Initialisiere die Flask-App
app = Flask(__name__)

# Richte CORS ein, damit dein Frontend mit dem Backend sprechen darf
CORS(app)

# --- HIER DEIN SPIEL-OBJEKT INITIALISIEREN ---
# Erstelle eine globale Instanz deines Spiels.
# Für ein echtes Spiel mit mehreren Partien würdest du hier eine
# komplexere Verwaltung brauchen (z.B. ein Dictionary von Spielen).
game = gamestate.GameState(4) 

@app.route("/api/spielzustand", methods=["GET"])
def get_spielzustand():
    """
    Diese Funktion wird aufgerufen, wenn das Frontend
    eine GET-Anfrage an /api/spielzustand sendet.
    """
    # Greife auf dein globales Spiel-Objekt zu und hole den Zustand
    game_state_dict = game.to_dict()
    
    # Wandel das Dictionary in eine JSON-Antwort um und sende sie
    return jsonify(game_state_dict)

@app.route("/api/spielzug", methods=["POST"])
def mache_spielzug():
    """
    Diese Funktion wird aufgerufen, wenn das Frontend
    einen Spielzug per POST an /api/spielzug sendet.
    """
    # 1. Hole die JSON-Daten aus der Anfrage
    data = request.get_json()

    if not data:
        return jsonify({"error": "Keine Daten erhalten"}), 400

    # 2. Extrahiere die Informationen aus den Daten
    feld_id = data.get("feld")
    stein_typ = data.get("stein")
    spieler_id = data.get("spielerId")

    # 3. Führe deine Spiellogik aus (greife auf deine Klassen zu)
    # angenommen, du hast eine Methode, die den Zug validiert und ausführt
    # zug_war_erfolgreich = game.platziere_stein(spieler_id, feld_id, stein_typ)

    zug_war_erfolgreich = True # Platzhalter

    # 4. Sende eine Antwort basierend auf dem Ergebnis
    if zug_war_erfolgreich:
        # ✅ Erfolgsfall: Sende eine Erfolgsnachricht und den neuen Spielzustand
        return jsonify({
            "message": "Zug erfolgreich ausgeführt!",
            "newState": game.to_dict() # Sende den aktualisierten Zustand zurück
        })
    else:
        # ❌ Fehlerfall: Sende eine Fehlermeldung
        return jsonify({
            "error": "Dieser Zug ist ungültig."
        }), 400 # Der HTTP-Status 400 bedeutet "Bad Request"

# Starte die App (für die Entwicklung)
if __name__ == '__main__':
    app.run(debug=True , port=8080)