import { writable } from 'svelte/store';
import type { GameState } from './types';

export const gameState = writable<GameState | null>(null);

export function implementGameState(newGameState: GameState) {
    gameState.set(newGameState);
    //console.log(newGameState)
}