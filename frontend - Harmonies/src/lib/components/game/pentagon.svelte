<script lang="ts">
    import TokenGroup from "./tokengroup.svelte";
    import { implementGameState} from "../../gameState";
    import type { Anwser, Pentagon } from "../../types";

    export let pentagon: Pentagon;

    $: tokenGroupsArray = Object.values(pentagon);

    async function handleGroupClick(clickedIndex: number) {

		try {
			const response = await fetch('http://localhost:8080/api/spielzug', { // Dein API-Endpunkt
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
                    action: 'TokenGroupClick',
                    payload: {
                        index: clickedIndex 
                    }
                    })
			});

			if (!response.ok) {
				console.error('Server-Error:', response.statusText);
				return;
			}

			const result = await response.json() as Anwser;
			console.log('Antwort vom Server:', result);
			
            // TODO dynamic stuff that shows that that move is illegal
            implementGameState(result.state)

		} catch (error) {
			console.error('Network-Error:', error);
		}
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