<script lang="ts">
  import { onMount, onDestroy, setContext } from 'svelte';
  import io from 'socket.io-client';
  import Pentagon from './lib/components/game/pentagon.svelte';
  import { gameState, implementGameState } from './lib/gameState';
  import Player from './lib/components/game/player.svelte';
  import AnimalDisplay from './lib/components/game/animalDisplay.svelte';
  import { SOCKET_KEY } from './lib/contextKeys';
  import type { Socket } from 'socket.io-client';
  import { writable } from 'svelte/store';
  import { socket } from './lib/socketStore';

  onMount(() => {
    const socketInstance = io('http://localhost:8080');
    socket.set(socketInstance);

    socketInstance.on('update_game_state', (data: any) => {
        implementGameState(data);
    });

    socketInstance.on('move_failed', (data: any) => {
        console.error("Zug fehlgeschlagen: ", data.error);
    });

    return () => {
        socketInstance.disconnect();
    };
  });

  $: if ($gameState?.winner && $gameState?.winner != '') {
    alert(`Spiel beendet! Der Gewinner ist ${$gameState.winner}`);
  }

  function handleStartButtonClick() {
        if (!$socket) {
            console.error("Socket not available!");
            return;
        }
        console.log('Sende Zug per WebSocket...');
        $socket.emit('player_move', {
            action: 'StartGame',
            payload: { 
            }
        });
    }
</script>

<div class="game-container">
  <AnimalDisplay animalDisplay = {$gameState?.animalDisplay ?? []}/>
  <div class='pentagon'>
    <Pentagon pentagon = {$gameState?.pentagon ?? []}/>
  </div>
  <button onclick={handleStartButtonClick}>Start Game</button>
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
  .asdf{
    width: 10px;
    height: 10px;
    background-color: rgb(30, 215, 228);
  }
</style>
