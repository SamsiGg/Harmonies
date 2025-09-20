<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Pentagon from './lib/components/game/pentagon.svelte';
  import { gameState, implementGameState } from './lib/gameState';
  import Player from './lib/components/game/player.svelte';
  import AnimalDisplay from './lib/components/game/animalDisplay.svelte';

  let intervalId = 0;

  async function getGameState() {
      const response = await fetch(` http://localhost:8080/api/spielzustand`); // GET-Anfrage
      if (response.ok) {
        const data = await response.json();
        implementGameState(data);
		}
  }

  onMount(() => {
    // Frage alle 3 Sekunden beim Backend nach, ob sich etwas geändert hat
    intervalId = setInterval(getGameState, 3000);
  });

  onDestroy(() => {
    clearInterval(intervalId);
  });
</script>

<div class="game-container">
  <AnimalDisplay animalDisplay = {$gameState?.animalDisplay ?? []}/>
  <div class='pentagon'>
    <Pentagon pentagon = {$gameState?.pentagon ?? []}/>
  </div>
  
</div>

{#if $gameState?.players[0]}
  {#each $gameState.players as player}
    <Player player={player} currentPlayerIndex={$gameState.currentPlayerIndex}/>
  {/each}
{/if}

<style>
  .game-container {
    display: flex;
    align-items: flex-start;
    gap: 2rem;
  }

  .pentagon{
    position: relative;
    width: 250px;
    height: 250px;
  }
</style>
