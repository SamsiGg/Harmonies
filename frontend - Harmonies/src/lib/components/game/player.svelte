<script lang="ts">
    import type { Anwser, Player } from "../../types";
    import Tokenhand from "./tokenhand.svelte";
    import Board from "./board.svelte";
    import { setContext } from "svelte";
    import { DND_CONTEXT_KEY } from "../../dragDropContext";
    import { implementGameState } from "../../gameState";
    
    let {
        player,
        currentPlayerIndex,
    }: {
        player: Player,
        currentPlayerIndex: number
    } = $props();

    type DragItem = {
        type: string,
        id: number
    }
    type DropItem = {
        type: string,
        position: [number, number]
    }
    let draggedItem = $state<DragItem>();
    let dropItem =  $state<DropItem>();

    function handleDragStart(item: DragItem){
        draggedItem = item;
    }

    function handleDrop(item: DropItem){
        dropItem = item;
        handleDragDropPost()
    }

    setContext(DND_CONTEXT_KEY, {
        handleDragStart,
        handleDrop
    });

    async function handleDragDropPost() {

        try {
            const response = await fetch('http://localhost:8080/api/spielzug', { // Dein API-Endpunkt
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'DragDropToken',
                    payload: {
                        player_index: player.index,
                        draggedItem,
                        dropItem
                    }
                    })
            });

            if (!response.ok) {
                console.error('Server-Error:', response.statusText);
                return;
            }

            const result = await response.json() as Anwser;
            console.log('Antwort vom Server:', result);
            
            implementGameState(result.state)

        } catch (error) {
            console.error('Network-Error:', error);
        }
    }

    async function handleFinishMove() {

        try {
            const response = await fetch('http://localhost:8080/api/spielzug', { // Dein API-Endpunkt
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'FinishMove',
                    payload: {
                        player_index: player.index
                    }
                    })
            });

            if (!response.ok) {
                console.error('Server-Error:', response.statusText);
                return;
            }

            const result = await response.json() as Anwser;
            console.log('Antwort vom Server:', result);
            
            implementGameState(result.state)

        } catch (error) {
            console.error('Network-Error:', error);
        }
    }

</script>

<div 
    class="player player-{player.index}"
    class:active={player.index === currentPlayerIndex}
>
    <div class='animals'>
        {#each player.animals as animal}
            <img src={`/animals/${animal.name}.jpg`} alt={animal.name} class="bild-box">
        {/each}
    </div>
    <Board 
        tiles = {player.board}
    />
    {#if !player.isBot}
        <Tokenhand 
        tokens = {player.tokenHand.filter(token => token !== null).map(token => token.type)}
        />
        <button class = 'finishMove' onclick={() => handleFinishMove()}>
            Finish Move
        </button>
    {/if}
</div>

<style>
    /* Allgemeine Stile für alle Spieler-Container */
    .player {
        position: fixed;
        width: 550px;
        height: 300px; 
        
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        
        background-color: rgba(240, 240, 240, 0.95);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        
        transform-origin: center;

        border: 4px solid transparent;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .player.active {
        border-color: #007bff;
        box-shadow: 0 0 25px rgba(0, 123, 255, 0.5);
    }


    /* --- Positionierung & Rotation für jeden Spieler --- */

    .player-0 {
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
    }

    .player-1 { /* HINWEIS: Hier stand vorher player-3, habe es zu 1 korrigiert, damit es zur Logik passt */
        top: 50%;
        left: -130px;
        transform: translateY(-50%) rotate(90deg);
    }
    
    .player-2 {
        top: 10px;
        left: 50%;
        transform: translateX(-50%) rotate(180deg);
    }
    
    .player-3 { /* HINWEIS: Hier stand vorher player-1, habe es zu 3 korrigiert */
        top: 50%;
        right: -130px;
        transform: translateY(-50%) rotate(-90deg);
    }


    /* --- Stile für die inneren Elemente --- */
    .animals {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        justify-content: center;
        align-content: center;
        gap: 5px;
        width: 140px;
        height: 250px;
        background-color: #e0f7fa;
        border-radius: 8px;
        padding: 5px;
    }
    .bild-box {
        width: 65px;
        height: 115px;
        object-fit: cover;
        border: 2px solid transparent;
        border-radius: 4px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .bild-box:hover {
        border-color: #007bff;
        transform: scale(2);
    }

    .finishMove {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer; 
        transition: background-color 0.2s ease, transform 0.1s ease;
    }

    .finishMove:hover {
        background-color: #0056b3;
    }

    .finishMove:active {
        background-color: #004494;
        transform: scale(0.98);
    }

    .finishMove:focus {
        outline: 2px solid #0056b3;
        outline-offset: 2px;
    }
</style>