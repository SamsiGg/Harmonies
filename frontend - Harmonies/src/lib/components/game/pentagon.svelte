<script lang="ts">
    import TokenGroup from "./tokengroup.svelte";
    import type { Anwser, Pentagon } from "../../types";
    import { socket } from "../../socketStore";

    export let pentagon: Pentagon;

    $: tokenGroupsArray = Object.values(pentagon);

    function handleGroupClick(clickedIndex: number) {
        if (!$socket) {
            console.error("Socket not available!");
            return;
        }
        console.log('Sende Zug per WebSocket...');
        $socket.emit('player_move', {
            action: 'TokenGroupClick',
            payload: {
                index: clickedIndex 
            }
        });
    }
</script>

<div class="pentagon">
    {#each tokenGroupsArray as group, i}
        <div class="node" style="--i: {i};">
            <TokenGroup 
                tokens={group.filter(token => token !== null).map(token => token.type)} 
                onclick={() => handleGroupClick(i)}    
            />
        </div>
    {/each}
</div>

<style>
    .pentagon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .node {
        position: absolute;
        top: 50%;
        left: 50%;
        transform:
            rotate(calc(var(--i) * 72deg))
            translate(80px)
            rotate(calc(var(--i) * -72deg))
            translate(-50%, -50%);
    }
</style>