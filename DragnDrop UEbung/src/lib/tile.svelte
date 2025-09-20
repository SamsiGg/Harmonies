<script lang="ts">

    import { getContext } from 'svelte';
    import { DND_CONTEXT_KEY } from './context';

    type DragDropContext = {
        draggedItemId: number,
        handleDragStart: (id: number) => void
    }

    const context = getContext<DragDropContext>(DND_CONTEXT_KEY);

    const { draggedItemId, handleDragStart } = context;

</script>

<div
    class = 'helo'
    ondragstart = {handleDragStart(1)}
    draggable="true"
>
</div>

<style>
    .helo {
        background-color: aquamarine;
        width: 30px;
        height: 30px;
        margin: 10px;
    }
</style>

