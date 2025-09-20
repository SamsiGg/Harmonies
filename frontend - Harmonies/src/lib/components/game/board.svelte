<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { Board } from "../../types";
    import Tile from "./tile.svelte";

    /** @type {Array<{ position: { x: number, y: number }, tokens: any[], dice: number }>} */
    export let tiles: Board;
</script>

<div class="board-container">
  {#each tiles as tile (`${tile.position.x}-${tile.position.y}`)}
    <div 
            class="tile-wrapper"
        >
            <Tile {tile} />
        </div>
  {/each}
</div>

<style>
  .board-container {
        position: relative;
        /* Wir verwenden CSS Grid für ein flexibles Layout */
        display: grid;
        grid-template-columns: repeat(1, 1fr); /* Beispiel: 4 Spalten */
        padding: 10px;
        background-color: #d2b48c; /* Holzfarbe */
        border-radius: 10px;
        width: 255px; /* Beispielbreite */
        min-height: 280px;
        box-shadow: inset 0 0 10px #00000050;
    }

    .tile-wrapper {
        border-radius: 8px;
        transition: background-color 0.2s, transform 0.2s;
    }
</style>