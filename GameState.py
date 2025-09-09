import random
import config # Assuming you have a config.py file
import math

class GameState():
    """
    Represents the entire state of a single game instance, including all
    players, the board components, and game variables.

    Args:
        player_amount (int): The number of players that will participate in the game.
        board_type (str): The type of board to create for each player (e.g., 'yellow').
    """
    def __init__(self, player_amount, board_type = 'yellow'):
        self.pentagon = Pentagon()
        self.animal_display = AnimalDisplay()
        self.animal_stack = AnimalStack()
        self.pouch = Pouch()

        self.players = [] # Add all the players and give them their board
        for _ in range(player_amount):
            board = Board(board_type)
            self.players.append(Player(board))

class Animal():

    def __init__(self,name,data):
        self.name = name
        self.points = data['points']
        self.structure = data['structure']

    def rotate_next(self, position, start_angle, rotate_angle):
        """
        Rotates till the next possible angle.

        Args:
            position (tuple): Position of the center token
            start_angle (int): Start angle (is not checked, beause it is expected to be correct)
            rotate_angle (int): Angle by which the Animal is rotated.
        """

        phi = start_angle + rotate_angle
        dphi = 0
        dr = 0
        dx = dr*math.sin(math.radians(dphi)+math.radians(phi))
        dy = dr*math.cos(math.radians(dphi)+math.radians(phi))
        

        while phi < 360:
            check = True

            for token in self.structure:
                token_position = token[1]
                dr = token_position[0]
                dphi = token_position[1]

                dx, dy = self._calculate_offsets(dr, dphi, phi)

                new_x = position[0] + dx
                new_y = position[1] + dy
                if not self._point_exists(config.BOARD_POSITIONS['yellow'], new_x, new_y):
                    check = False
                #print(f"phi={phi}, dr={dr}, dphi={dphi} -> new_x={new_x:.3f}, new_y={new_y:.3f}")
            
            if check:
                return phi

            phi += rotate_angle
        
        return None

    def _calculate_offsets(self, dr, dphi, phi):
        total_angle_rad = math.radians(dphi + phi)
        
        dy = dr * math.cos(total_angle_rad)
        dx = dr * math.sin(total_angle_rad)
        
        return dx, dy

    def _point_exists(self, board_points, x, y):
        for point in board_points:
            if self._are_points_close(point,(x,y)):
                return True
        return False    
        

    def _are_points_close(self, p1, p2, toleranz=1e-3):
        y1, x1 = p1
        y2, x2 = p2
        
        return math.isclose(x1, x2, abs_tol=toleranz) and math.isclose(y1, y2, abs_tol=toleranz)

class AnimalStack():

    def __init__(self):
        self.animals = []
        for name, data in config.ANIMAL_DATA.items():
            self.animals.append(Animal(name,data))
        random.shuffle(self.animals)

class AnimalDisplay():
    """ 
    The five Animal cards displayed in the middle of the board.

    Args:
        
    """
    def __init__(self):
        self.animals = []

class Player():
    """
    Represents a single player in the game, holding their personal board.

    Args:
        board (Board): The specific Board object assigned to this player.
    """
    def __init__(self, board):
        self.board = board
        self.animals = []
    
class Board():
    """
    Represents a player's personal hexagonal game board, composed of
    individual Tile objects.

    Args:
        board_type (str): A string identifier for the board layout, which
                          determines its dimensions from the config file.
    """
    def __init__(self, board_type):
        if board_type not in config.ALLOWED_BOARD_TYPES:
            raise ValueError(f'Board was given the wrong board type: "{board_type}"')

        for key, positions in config.BOARD_POSITIONS.items():
            if board_type == key:
                self.tiles = []
                for pos in positions:
                    self.tiles.append(Tile(pos))

class Tile():
    """
    Represents a single hexagonal tile on a player's board. It has a
    position and can hold tokens.

    Args:
        position (tuple): The (x, y) coordinates of the tile on the board.
    """
    def __init__(self, position: tuple):
        self.tokens = []
        self.position = position
        self.dice = False

    def __repr__(self):
        if len(self.tokens) == 0:
            return '<Tile: empty>'
        return f'Tile: "{self.tokens}"'

class Pentagon():
    """
    Represents the central token display (the pentagon), holding 5 groups
    of 3 tokens each.
    """
    def __init__(self):
        self.token_groups = [[None for _ in range(3)] for _ in range(5)]

class Token():
    """
    Represents a single game token with a specific state (e.g., color).

    Args:
        state (str): The state of the token, typically its color.
    """
    def __init__(self, state):
        if state not in config.ALLOWED_TOKEN_STATES:
            self.state = None
            raise ValueError(f'The given state "{state}" is not compatible with the possible states of a Token')
        else:
            self.state = state

    def __repr__(self):
        return f'<Token: {self.state}>'

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
                all_tokens.append(Token(state))

        random.shuffle(all_tokens)
        return all_tokens

    def take_out_tokens(self, amount = 3):
        if amount > len(self.tokens):
            return None

        tokens = [self.tokens.pop() for _ in range(amount)]
        return tokens


if __name__ == "__main__":
    t = Token('green')
    g = GameState(4, 'yellow')
    g.pentagon.token_groups[0][1] = t

    print('Anwser: ' + str(g.animal_stack.animals[0].rotate_next((2*config.C,2),60,15)))