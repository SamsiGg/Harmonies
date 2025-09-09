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
BOARD_POSITIONS = {
    #'yellow': [(0,0),(0,2*C),(0,4*C),(0.5,C),(0.5,3*C),(1,0),(1,2*C),(1,4*C),(1.5,C),(1.5,3*C),(2,0),(2,2*C),(2,4*C),(2.5,C),(2.5,3*C),(3,0),(3,2*C),(3,4*C),(3.5,C),(3.5,3*C),(4,0),(4,2*C),(4,4*C)],
    'yellow': [(0, 0), (2*C, 0), (4*C, 0), (C, 0.5), (3*C, 0.5), (0, 1), (2*C, 1), (4*C, 1), (C, 1.5), (3*C, 1.5), (0, 2), (2*C, 2), (4*C, 2), (C, 2.5), (3*C, 2.5), (0, 3), (2*C, 3), (4*C, 3), (C, 3.5), (3*C, 3.5), (0, 4), (2*C, 4), (4*C, 4)],
    'blue': (8,4)
}

ALLOWED_BOARD_TYPES = BOARD_POSITIONS.keys()

ANIMAL_DATA = {
    "stingray": {
        "points": [4,10,16],
        "structure": [
            ('blue',(0,0)),
            ('grey',(1,0)),
            ('grey',(1,60))]
    },
    # ... alle anderen Tiere
}
