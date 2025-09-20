<script lang='ts'>
    import { setContext } from 'svelte';
    import Tile from './lib/tile.svelte';
    import { DND_CONTEXT_KEY } from './lib/context';
    import Coloumn from './lib/coloumn.svelte';

    let tasks: any[];
    let draggedItemId: number | null = 0;

    function handleDragStart(id: number){
      draggedItemId += 2;
    }

    function handleDrop(id: number){
      draggedItemId -= 1;
    }


    setContext(DND_CONTEXT_KEY, {
      tasks,
      draggedItemId,
      handleDragStart,
      handleDrop
    });
</script>

<Tile/>
<Tile/>
<Coloumn/>
<div>{draggedItemId}</div>

<style>
  .hi {
    background-color: aqua;
  }
</style>