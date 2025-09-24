<script lang='ts'>
  import type { Tile } from "../../types";
  import { getContext } from "svelte";
  import { DND_CONTEXT_KEY } from "../../contextKeys";
  import Token from "./token.svelte";

  /** @type {{ position: { x: number, y: number }, tokens: any[], dice: number }} */
  let {tile}: {tile: Tile} = $props();
  const sizeFactor = 60;
  const top = tile.position.y * sizeFactor;
  const left = tile.position.x * sizeFactor;

  let isDragOver: boolean = $state(false);

  function onDragOver (event: DragEvent){
      event.preventDefault();
      isDragOver = true;
  }

  type DropItem = {
    type: string,
    position: [number, number]
  }

  type DragDropContext = {
    handleDrop: (dropItem: DropItem) => void
  }

  const handleDrop = getContext<DragDropContext>(DND_CONTEXT_KEY).handleDrop;

</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div 
  class="hexagon" 
  class:drag-over={isDragOver}
  style="left: {left}px; top: {top}px;"
  ondragover = {onDragOver}
  ondragleave={() => isDragOver = false}
  ondrop={() => {
        if (handleDrop) {
            handleDrop({
                type: 'tile',
                position: [left/sizeFactor, top/sizeFactor]
            });
        }
        isDragOver = false;
    }}
>
  <div class="content">
    {#if tile.tokens.length > 0}
      <span class="token-count">{tile.tokens.length}
        {#each tile.tokens as token, i}
          <Token 
            color={token.type} 
            index={i} 
            parent='tile' 
            amount={tile.tokens.length}
            position={tile.position}
            has_die={tile.die}/>
        {/each}
      </span>
    {/if}
  </div>
</div>


<style>
  .hexagon {
    position: absolute;
    --hex-size: 35px;
    /* Die Breite des Sechsecks ist jetzt die Basisgröße */
    width: var(--hex-size); 
    /* Die Höhe ist breiter, ca. das 1.732-fache (Wurzel 3) */
    height: calc(var(--hex-size) * 1.732);
    background-color: #a7c957;
    transition: transform 0.2s ease-in-out;
    
    /* Wichtig: margin muss jetzt horizontal sein, nicht vertikal */
    margin: 0 calc(var(--hex-size) * 0.433); /* (sqrt(3)/2)/2 */
  }

  /* Die Dreiecke links und rechts mit Pseudo-Elementen erstellen */
  .hexagon::before,
  .hexagon::after {
    content: "";
    position: absolute;
    width: 0;
    
    /* Die transparenten Ränder sind jetzt oben und unten */
    border-top: calc(var(--hex-size) * 0.866) solid transparent;
    border-bottom: calc(var(--hex-size) * 0.866) solid transparent;
  }

  /* Linkes Dreieck */
  .hexagon::before {
    right: 98%; /* Positioniert links vom Hauptelement */
    border-right: calc(var(--hex-size) / 2) solid #a7c957;
  }

  /* Rechtes Dreieck */
  .hexagon::after {
    left: 98%; /* Positioniert rechts vom Hauptelement */
    border-left: calc(var(--hex-size) / 2) solid #a7c957;
  }
  
  .hexagon:hover {
    transform: scale(1.1);
    cursor: pointer;
    z-index: 10;
    filter: brightness(1.1);
  }

  .content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
    z-index: 1;
  }
  .drag-over {
    /* Hintergrund für das mittlere Rechteck */
    background-color: #4a90e2; /* Ein kräftigeres Blau für besseres Feedback */
    filter: brightness(1.2);   /* Etwas aufhellen, um es hervorzuheben */
  }

  /* Wichtig: Wir müssen auch die Farbe der Dreiecke anpassen! */
  .drag-over::before {
    border-right-color: #4a90e2; 
  }

  .drag-over::after {
    border-left-color: #4a90e2;
  }
</style>