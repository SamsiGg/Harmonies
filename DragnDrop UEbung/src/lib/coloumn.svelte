<script lang="ts">
    import { getContext } from "svelte";
    import { DND_CONTEXT_KEY } from "./context";

    let isDragOver: boolean = $state(false);

    function onDragOver (event: DragEvent){
        event.preventDefault();
        isDragOver = true;
    }

    type DragDropContext = {
        draggedItemId: number,
        handleDrop: () => void
    }

    const context = getContext<DragDropContext>(DND_CONTEXT_KEY);
    const {handleDrop} = context;

</script>

<div 
    class='coloumn'
    class:drag-over={isDragOver}
    ondragover = {onDragOver}
    ondrop = {handleDrop}
></div>

<style>
    .coloumn {
        background-color: bisque;
        width: 70px;
        height: 200px;
    }
</style>