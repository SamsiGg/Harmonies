<script lang="ts">
	import Token from "./token.svelte";

	// This component expects an array of strings (colors) as a prop.
	// We'll give it a default value for easy testing.
	let {
        tokens = []
    }: {
        tokens?: (string | null)[]
    } = $props();

	// Create a reactive variable that only contains the valid (non-null) tokens.
	const displayableTokens = $derived(tokens.filter(token => token !== null));
</script>

<div class="token-hand-container">
	{#each displayableTokens as color,i}
		<Token 
			parent = 'token_hand' 
			color = {color} 
			index = {i}
		/>
	{/each}
</div>

<style>
	.token-hand-container {
		/* --- Positioning --- */
		position: fixed; /* Fixes the position relative to the browser window */
		bottom: 20px; /* 20px from the bottom */
		right: 20px; /* 20px from the right */

		/* --- Styling --- */
		background-color: rgba(224, 216, 192, 0.9); /* A slightly transparent beige */
		padding: 12px;
		border-radius: 8px;
		border: 3px solid #4a4a4a;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		backdrop-filter: blur(4px); /* Adds a nice frosted glass effect */

		/* --- Content Alignment (Flexbox) --- */
		display: flex;
		gap: 8px; /* Creates space between the tokens */
		align-items: center;
		justify-content: center;
		height: 100px; /* Fixed height for the container */
		min-width: 40px; /* Ensures it has a minimum size even when empty */
		z-index: 100;
	}
</style>