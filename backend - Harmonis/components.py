import random
import config # Assuming you have a config.py file
import objects

class AnimalStack():

    def __init__(self):
        self.animals = []
        for name, data in config.ANIMAL_DATA.items():
            self.animals.append(objects.Animal(name,data))
        random.shuffle(self.animals)

    def draw_cards(self, amount = 1):
        animals = []
        for _ in range(amount):
            animals.append(self.animals.pop())
        return animals

class Pentagon():
    """
    Represents the central token display (the pentagon), holding 5 groups
    of 3 tokens each.
    """
    def __init__(self, tokens):
        if len(tokens) >= 15:
            self.token_groups = [[tokens.pop() for j in range(3)] for i in range(5)]
        else:
            [[None for _ in range(3)] for _ in range(5)]

class Pouch():
    """
    Manages the supply of all game tokens. It creates, shuffles,
    and deals tokens from a virtual pouch.
    """
    def __init__(self):
        self.tokens = self._create_all_shuffled_tokens(config.TOKEN_AMOUNT)

    def _create_all_shuffled_tokens(self, token_amount: dict):
        all_tokens = []
        for state, amount in token_amount.items():
            for _ in range (amount):
                all_tokens.append(objects.Token(state))

        random.shuffle(all_tokens)
        return all_tokens

    def take_out_tokens(self, amount = 3):
        if amount > len(self.tokens):
            return None

        tokens = [self.tokens.pop() for _ in range(amount)]
        return tokens

class AnimalDisplay():
    """ 
    The five Animal cards displayed in the middle of the board.

    Args:
        animals (list): A list of five animals, that were taken from the AnimalStack
    """
    def __init__(self, animals):
        self.animals = animals
