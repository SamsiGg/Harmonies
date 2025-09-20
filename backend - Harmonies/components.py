import random
import config # Assuming you have a config.py file
import objects
from objects import Animal,Token

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
    
    def to_dict(self):
        return {'card_amount': int(len(self.animals))}

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
    
    def to_dict(self):
        pentagon_list = []
        for group in self.token_groups:
            group_list = []
            for token in group:
                if token is None:
                    group_list.append(None)
                else:
                    group_list.append(token.to_dict())
            pentagon_list.append(group_list)
        return pentagon_list
    
    def take_token_group(self, index):

        tokens = self.token_groups[index].copy()
        for token in tokens:
            if token is None:
                return False
        
        for i in range(len(self.token_groups[index])):
            self.token_groups[index][i] = None

        return tokens
    
    def add_token_group(self, tokens: list[Token]):
        if len(tokens) == 3:
            for i,token_group in enumerate(self.token_groups):
                if token_group[0] is None:
                    self.token_groups[i] = tokens

class Pouch():
    """
    Manages the supply of all game tokens. It creates, shuffles,
    and deals tokens from a virtual pouch.
    """
    def __init__(self):
        self.tokens = self._create_all_shuffled_tokens(config.TOKEN_AMOUNT)

    def _create_all_shuffled_tokens(self, token_amount: dict):
        all_tokens = []
        for type, amount in token_amount.items():
            for _ in range (amount):
                all_tokens.append(objects.Token(type))

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
    def __init__(self, animals: list[Animal], max_amount = 5):
        self.animals: list[Animal] = animals
        self.max_amount: int = max_amount

    def to_dict(self):
        animal_list = []
        for animal in self.animals:
            animal_list.append(animal.to_dict())
        return animal_list
    
    def get_animal(self, name):
        for i,animal in enumerate(self.animals):
            if(animal.name == name):
                self.animals.pop(i)
                return animal
            
        return None
    
    def add_animal(self, animal: Animal):
        if len(self.animals) < self.max_amount:
            self.animals.append(animal)
