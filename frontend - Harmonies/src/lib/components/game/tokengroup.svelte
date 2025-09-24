<script lang='ts'>
    import Token from "./token.svelte";

    // In Svelte 5 definieren wir die Schnittstelle der Komponente mit $props().
    // Wir erwarten ein 'tokens'-Array und eine 'onclick'-Funktion als Eigenschaften.
    let { 
        tokens = [], 
        onclick = (event: MouseEvent) => {} 
    }: {
        tokens?: string[];
        onclick?: (event: MouseEvent) => void;
    } = $props();
</script>

<div
    class="token-group-container count-{tokens.length}"
    onclick={onclick}
    role="button"
    tabindex="0"
    onkeydown={(event) => { if (event.key === 'Enter') onclick(event as any) }}
>
    
    {#each tokens as color,i}
        {#if color}
            <Token parent = 'token_group' {color} index = {i} position={{x:-1000,y:-1000}} has_die={false}/>
        {/if}
    {/each}

</div>

<style>
    .token-group-container {
        width: 90px;
        height: 90px;
        border: 4px solid #4a4a4a;
        border-radius: 50%;
        background: #e0d8c0;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: inset 0 3px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: transform 0.2s, border-color 0.2s;
    }

    .token-group-container:hover,
    .token-group-container:focus {
        border-color: #007bff;
        transform: scale(1.05);
        outline: none;
    }
</style>