<script lang="ts">
    import { DND_CONTEXT_KEY } from "../../contextKeys";
    import { socket } from "../../socketStore";
    import type { Token } from "../../types";
    import Tile from "./tile.svelte";
    import { getContext,hasContext } from "svelte";



    let {
        color,
        index,
        parent,
        amount,
        position = {x:0,y:0},
        has_die = false
    }: {
        color?: string,
        index: number,
        parent: string,
        amount?: number,
        position: {
            x: number,
            y: number
        },
        has_die: boolean
    } = $props();

    const tileTransform = $derived(() => {
        // Diese Logik nur ausführen, wenn wir auf einem 'tile' sind
        if (parent !== 'tile' || !amount || amount <= 0) {
            return null; // Für alle anderen Fälle keinen Style anwenden
        }

        const step = -8; // Höhe (35px) - Überlappung (10px)
        const middle = (amount - 1) / 2;
        const translateY = (index - middle) * step;

        // Den vollständigen transform-String zurückgeben
        return `translate(-50%, -50%) translateY(${translateY}px)`;
    });

    type DraggedItem = {
            type: string,
            id: number
        }

    type DragDropContext = {
        handleDragStart: (draggedItem: DraggedItem) => void
    }
    
    const handleDragStart = hasContext(DND_CONTEXT_KEY)
        ? getContext<DragDropContext>(DND_CONTEXT_KEY).handleDragStart
        : undefined;

    function handleTokenClick (event: MouseEvent){
        if(event.ctrlKey && parent==='tile'){
            if (!$socket) {
                console.error("Socket not available!");
                return;
            }
            $socket.emit('player_move', {
                action: 'PlaceDie',
                payload: {
                    position: position 
                }
            });
        }
    }

</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
    class="token {parent}_{index}"
    style="background-color: {color};"
    draggable={parent === 'token_hand'}
    style:transform={tileTransform()}
    ondragstart={handleDragStart ? () => handleDragStart({
            type: parent + '_token',
            id: index
        }) 
        : undefined}
    role="button"
    tabindex="0"
    onclick={handleTokenClick}
    
>
{has_die}
</div>

<style>
    .token {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.25);
        position: absolute;
        transition: transform 0.3s ease;
        z-index: 10;
    }
    .token:active {
        cursor: grabbing;
    }

    .token_group_0 {
        transform: translateY(-16px);
    }
    .token_group_1 {
        transform: translate(-18px, 16px);
    }
    .token_group_2 {
        transform: translate(18px, 16px);
    }

    .token_hand_0 {
        transform: translateY(-40px);
        cursor: grab;
    }
    .token_hand_1 {
        transform: translateY(0);
        cursor: grab;
    }
    .token_hand_2 {
        transform: translateY(40px);
        cursor: grab;
    }

    .tile_0{
        cursor: grab;
        top: 50%;
        left: 50%;
    }
    .tile_1 {
        cursor: grab;
        top: 50%;
        left: 50%;
    }
    .tile_2 {
        cursor: grab;
        top: 50%;
        left: 50%;
    }
</style>