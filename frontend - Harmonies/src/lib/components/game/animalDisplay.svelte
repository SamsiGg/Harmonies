<script lang="ts">
    import { implementGameState } from "../../gameState";
    import { socket } from "../../socketStore";
    import type { AnimalDisplay,Animal, Anwser } from "../../types";

    let {animalDisplay = []}: {animalDisplay: AnimalDisplay} = $props();

    function handleImageClick(animal: Animal) {
        if (!$socket) {
            console.error("Socket not available!");
            return;
        }
        console.log('Sende Zug per WebSocket...');
        $socket.emit('player_move', {
            action: 'PlayerDisplayImageClick',
            payload: {
                name: animal.name 
            }
        });
    }

</script>

<div class="playerDisplay">
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    {#each animalDisplay as animal}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <img 
            src={`/animals/${animal.name}.jpg`} 
            alt={animal.name} 
            class="bild-box"
            onclick={() => handleImageClick(animal)}>
    {/each}
</div>

<style>
    .playerDisplay{
        width: 230px;
        height: 260px;
        background-color: aqua;
    }
    .bild-box {
        width: 70px;
        height: 120px;
        object-fit: cover;
        margin-top: 3px;
        border: 1px solid #ccc; /* Nur zur Veranschaulichung */
    }
    .bild-box:hover,
    .bild-box:focus {
        border-color: #007bff;
        transform: scale(2);
        outline: none;
    }
</style>