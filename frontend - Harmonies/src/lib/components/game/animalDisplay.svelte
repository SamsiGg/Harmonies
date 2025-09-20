<script lang="ts">
    import { implementGameState } from "../../gameState";
    import type { AnimalDisplay,Animal, Anwser } from "../../types";

    let {animalDisplay = []}: {animalDisplay: AnimalDisplay} = $props();

    async function handleImageClick(animal: Animal) {

		try {
			const response = await fetch('http://localhost:8080/api/spielzug', { // Dein API-Endpunkt
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
                    action: 'PlayerDisplayImageClick',
                    payload: {
                        name: animal.name 
                    }
                    })
			});

			if (!response.ok) {
				console.error('Server-Error:', response.statusText);
				return;
			}

			const result = await response.json() as Anwser;
			console.log('Antwort vom Server:', result);
			
            implementGameState(result.state)

		} catch (error) {
			console.error('Network-Error:', error);
		}
	}

</script>

<div class="playerDisplay">
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    {#each animalDisplay as animal}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <img 
            src={`/animals/${animal.name}.jpg`} 
            alt={animal.name} 
            class="bild-box"
            onclick={() => handleImageClick(animal)}>
    {/each}
</div>

<style>
    .playerDisplay{
        width: 230px;
        height: 260px;
        background-color: aqua;
    }
    .bild-box {
        width: 70px;
        height: 120px;
        object-fit: cover;
        margin-top: 3px;
        border: 1px solid #ccc; /* Nur zur Veranschaulichung */
    }
    .bild-box:hover,
    .bild-box:focus {
        border-color: #007bff;
        transform: scale(2);
        outline: none;
    }
</style>