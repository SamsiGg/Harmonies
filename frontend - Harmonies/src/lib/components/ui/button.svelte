<script lang="ts">
    let a = 0;
    // Diese Funktion wird aufgerufen, wenn ein Spieler einen Zug macht
    async function macheSpielzug(feldId: string, spielsteinTyp: string) {
        const zugDaten = {
            feld: feldId,
            stein: spielsteinTyp,
            spielerId: "spieler123" // ID des aktuellen Spielers
        };

        try {
        const response = await fetch('http://localhost:8080/api/spielzug', { // URL deines Backends
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Wichtig: Sagt dem Backend, dass wir JSON senden
            },
            body: JSON.stringify(zugDaten) // Wandelt das JavaScript-Objekt in einen JSON-String um
        });

        if (!response.ok) {
            // Fehlerbehandlung, falls das Backend einen Fehler meldet
            console.error('Der Spielzug war ungültig!');
            return;
        }

        // Optional: Backend könnte den neuen Spielzustand als Antwort senden
        const neuerSpielzustand = await response.json();
        console.log('Zug erfolgreich, neuer Zustand:', neuerSpielzustand);
        // Hier könntest du dein Frontend mit dem neuen Zustand aktualisieren

        } catch (error) {
            console.error('Fehler bei der Verbindung zum Backend:', error);
        }
    }
</script>

<button on:click={() => macheSpielzug('A3','Wald')}>hi</button>