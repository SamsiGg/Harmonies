//GameState
export type GameState = {
    pentagon: Pentagon,
    animalStack: AnimalStack,
    animalDisplay: AnimalDisplay,
    players: Players,
    currentPlayerIndex: CurrentPlayerIndex,
    winner: string
}

//Pentagon
export type Pentagon = TokenGroups[];

export type TokenGroups = Token[];

export type Token = {
  type: string;
};

//AnimalStack
export type AnimalStack = {
    cardAmount: string;
}

//AnimalDisplay
export type AnimalDisplay = Animal[]

export type Animal = {
    name: string;
    dice: number;
}

//Players
export type Players = Player[]

export type Player = {
    board: Board,
    animals: Animal[],
    tokenHand: TokenHand,
    index: number,
    isBot: boolean,
    score: number
}

export type Board = Tile[]

export type Tile = {
    tokens: Token[],
    position: {
        x: number,
        y: number
    },
    die: boolean
}

export type TokenHand = Token[]

//CurrentPlayerIndex
export type CurrentPlayerIndex = number

export type Anwser = {
    message: string,
    state: GameState
}


