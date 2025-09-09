<script lang="ts">
  import viteLogo from '/vite.svg'
  import pentagon from './lib/components/game/pentagon.svelte'
  import Button from './lib/components/ui/button.svelte';
  import { onMount, onDestroy } from 'svelte';

  let spielId = 'partie123';
  let intervalId = 0;

  async function frageSpielzustandAb() {
    const response = await fetch(`/api/spielzustand/${spielId}`); // GET-Anfrage
    const neuerZustand = await response.json();
    // ... hier aktualisierst du dein Frontend mit dem neuen Zustand
  }

  onMount(() => {
    // Frage alle 3 Sekunden beim Backend nach, ob sich etwas geändert hat
    intervalId = setInterval(frageSpielzustandAb, 3000);
  });

  onDestroy(() => {
    // Wichtig: Den Intervall stoppen, wenn die Komponente verlassen wird
    clearInterval(intervalId);
  });
</script>

<main>
  <div>
  </div>
  <h1>Hello World</h1>

  <div class="card">
  </div>

  <Button></Button>

  <p>
    Check out <a href="https://github.com/sveltejs/kit#readme" target="_blank" rel="noreferrer">SvelteKit</a>, the official Svelte app framework powered by Vite!
  </p>

  <p class="read-the-docs">
    Click on the Vite and Svelte logos to learn more
  </p>
</main>

<style>
  .read-the-docs {
    color: #888;
  }
</style>
