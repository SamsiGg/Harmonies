MAX_PLAYERS = 4

TOKEN_AMOUNT = {
    'blue':   23,
    'grey':   23,
    'brown':  21,
    'green':  19,
    'yellow': 19,
    'red':    15
}

ALLOWED_TOKEN_STATES = TOKEN_AMOUNT.keys()

C = 0.866
D = 1.732
TILE_POSITIONS = {
    #'yellow': [(0,0),(0,2*C),(0,4*C),(0.5,C),(0.5,3*C),(1,0),(1,2*C),(1,4*C),(1.5,C),(1.5,3*C),(2,0),(2,2*C),(2,4*C),(2.5,C),(2.5,3*C),(3,0),(3,2*C),(3,4*C),(3.5,C),(3.5,3*C),(4,0),(4,2*C),(4,4*C)],
    'yellow': [(0, 0), (2*C, 0), (4*C, 0), (C, 0.5), (3*C, 0.5), (0, 1), (2*C, 1), (4*C, 1), (C, 1.5), (3*C, 1.5), (0, 2), (2*C, 2), (4*C, 2), (C, 2.5), (3*C, 2.5), (0, 3), (2*C, 3), (4*C, 3), (C, 3.5), (3*C, 3.5), (0, 4), (2*C, 4), (4*C, 4)],
    'blue': (8,4)
}

ALLOWED_BOARD_TYPES = TILE_POSITIONS.keys()

ALLOWED_STACKS = {
    'brown': {'brown'},
    'green': {'brown'},
    'grey':  {'grey'},
    'red':   {'grey', 'red', 'brown'}
}

ANIMAL_DATA = {
    "ray": {
        "points": [4,10,16],
        "structure": [
            ('blue',(0,0)),
            ('grey',(1,0)),
            ('grey',(1,60))]
    },
    "fox": {
        "points": [4,9,16],
        "structure": [
            ('grey',(0,0)),
            ('grey',(1,0)),
            ('yellow',(2,0))]
    },
    "monkey": {
        "points": [5,11],
        "structure": [
            ('grey',(0,0)),
            ('grey',(0,0)),
            ('blue',(1,0)),
            ('blue',(1,60))]
    },
    "fish": {
        "points": [3,6,10,16],
        "structure": [
            ('blue',(0,0)),
            ('grey',(1,0)),
            ('grey',(1,0)),
            ('grey',(1,0))]
    },
    "squirrel": {
        "points": [4,9,15],
        "structure": [
            ('grb',(0,0)),
            ('red',(0,0)),
            ('brown',(1,0)),
            ('brown',(1,0)),
            ('green',(1,0))]
    },
    "frog": {
        "points": [2,4,6,10,15],
        "structure": [
            ('blue',(0,0)),
            ('green',(1,0))]
    },
    "gecko": {
        "points": [5,10,16],
        "structure": [
            ('grb',(0,0)),
            ('red',(0,0)),
            ('yellow',(1,0)),
            ('yellow',(2,0))]
    },
    "hedgehog": {
        "points": [5,12],
        "structure": [
            ('grb',(0,0)),
            ('red',(0,0)),
            ('brown',(1,0)),
            ('green',(1,0)),
            ('green',(1,60)),
            ('brown',(1,60))]
    },
    "crocodile": {
        "points": [4,9,15],
        "structure": [
            ('blue',(0,0)),
            ('blue',(1,0)),
            ('brown',(2,0)),
            ('brown',(2,0)),
            ('green',(2,0))]
    },
    "flamingo": {
        "points": [4,10,16],
        "structure": [
            ('blue',(0,0)),
            ('yellow',(1,0)),
            ('yellow',(1,60))]
    },
    "bat": {
        "points": [3,6,10,15],
        "structure": [
            ('grey',(0,0)),
            ('brown',(1,0)),
            ('brown',(1,0)),
            ('green',(1,0))]
    },
    "ladybug": {
        "points": [2,5,8,12,17],
        "structure": [
            ('yellow',(0,0)),
            ('green',(1,0))]
    },
    "boar": {
        "points": [4,8,13],
        "structure": [
            ('brown',(0,0)),
            ('green',(0,0)),
            ('grb',(1,0)),
            ('red',(1,0))]
    },
    "eagle": {
        "points": [5,11],
        "structure": [
            ('grey',(0,0)),
            ('grey',(0,0)),
            ('grey',(0,0)),
            ('yellow',(1,0))]
    },
    "peacock": {
        "points": [5,10,17],
        "structure": [
            ('grb',(0,0)),
            ('red',(0,0)),
            ('blue',(1,300)),
            ('blue',(1,60))]
    },
    "parrot": {
        "points": [4,9,14],
        "structure": [
            ('brown',(0,0)),
            ('green',(0,0)),
            ('blue',(1,0)),
            ('blue',(1,60))]
    },
    "bear": {
        "points": [5,11],
        "structure": [
            ('green',(0,0)),
            ('grey',(1,0)),
            ('grey',(1,0)),
            ('grey',(1,60)),
            ('grey',(1,60))]
    },
    "meerkat": {
        "points": [2,5,9,14],
        "structure": [
            ('grey',(0,0)),
            ('yellow',(1,0))]
    },
    "duck": {
        "points": [2,4,8,13],
        "structure": [
            ('blue',(0,0)),
            ('grb',(1,0)),
            ('red',(1,0))]
    },
    "wolf": {
        "points": [4,10,16],
        "structure": [
            ('brown',(0,0)),
            ('brown',(0,0)),
            ('green',(0,0)),
            ('yellow',(1,0)),
            ('yellow',(1,60))]
    },
    "otter": {
        "points": [5,10,16],
        "structure": [
            ('blue',(0,0)),
            ('green',(1,0)),
            ('green',(2,0))]
    },
    "kingfisher": {
        "points": [5,11,18],
        "structure": [
            ('brown',(0,0)),
            ('brown',(0,0)),
            ('green',(0,0)),
            ('blue',(1,300)),
            ('blue',(1,60))]
    },
    "mouse": {
        "points": [5,10,17],
        "structure": [
            ('grb',(0,0)),
            ('red',(0,0)),
            ('yellow',(1,300)),
            ('yellow',(1,60))]
    },
    "bunny": {
        "points": [5,10,17],
        "structure": [
            ('green',(0,0)),
            ('green',(1,0)),
            ('grb',(2,0)),
            ('red',(2,0))]
    },
    "koala": {
        "points": [3,6,10,15],
        "structure": [
            ('brown',(0,0)),
            ('green',(0,0)),
            ('green',(1,0))]
    },
    "panther": {
        "points": [5,11],
        "structure": [
            ('yellow',(0,0)),
            ('brown',(1,0)),
            ('green',(1,0)),
            ('brown',(2,0)),
            ('green',(2,0))]
    },
    "raven": {
        "points": [4,9],
        "structure": [
            ('yellow',(0,0)),
            ('grb',(1,300)),
            ('red',(1,300)),
            ('grb',(1,60)),
            ('red',(1,60))]
    },
    "llama": {
        "points": [5,12],
        "structure": [
            ('yellow',(0,0)),
            ('yellow',(1,0)),
            ('grey',(2,0)),
            ('grey',(2,0))]
    },
    "raccoon": {
        "points": [6,12],
        "structure": [
            ('yellow',(0,0)),
            ('blue',(1,300)),
            ('blue',(1,0)),
            ('blue',(1,60))]
    },
    "bee": {
        "points": [8,18],
        "structure": [
            ('brown',(0,0)),
            ('green',(0,0)),
            ('yellow',(1,300)),
            ('yellow',(1,0)),
            ('yellow',(1,60))]
    },
    "snowfox": {
        "points": [5,10,17],
        "structure": [
            ('yellow',(0,0)),
            ('brown',(1,300)),
            ('green',(1,300)),
            ('brown',(1,60)),
            ('green',(1,60))]
    },
    "penguin": {
        "points": [4,10,16],
        "structure": [
            ('grey',(0,0)),
            ('blue',(1,300)),
            ('blue',(1,60))]
    }
}
