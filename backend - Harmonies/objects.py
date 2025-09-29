from __future__ import annotations
import config # Assuming you have a config.py file
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Board

class Animal():

    def __init__(self,name,data):

        self.name = name
        self.points = data['points']
        self.structure: list[tuple[str, tuple[int, int]]] = data['structure']
        self.dice_amount = len(self.points)

    def to_dict(self):
        return {
            'name': self.name,
            'dice': self.dice_amount
        }
    
    def die_placeable(self, position, board: Board):
        angle = self.rotate_next(position, -60) #-60, so that angle=0 is first checked
        while angle is not None:
            placeable = True
            
            for animal_tile_data in self.structure:
                types = animal_tile_data[0]
                dpos = animal_tile_data[1]
                dr = dpos[0]
                dphi = dpos[1]

                dx, dy = self._calculate_offsets(dr, dphi, angle)
                target_x = round(position[0] + dx,3)
                target_y = round(position[1] + dy,3)

                target_tile = None
                for tile in board.tiles:
                    if self._are_points_close(tile.position, (target_x, target_y)):
                        target_tile = tile
                        break

                if target_tile.has_die or len(types) != len(target_tile.tokens):
                    placeable = False
                    break

                for i, type in enumerate(types):
                    token_type = target_tile.tokens[i].type
                    if isinstance(type, str) and token_type != type:
                        placeable = False
                        break
                    if isinstance(type, tuple) and token_type not in type:
                        placeable = False
                        break
                
                if not placeable:
                    break
                    

            if placeable:
                return True          
                  
            angle = self.rotate_next(position, angle)               
        return False
    
    def take_die(self):
        self.dice_amount -= 1


    def rotate_next(self, position, start_angle, rotate_angle=60, ):
        """
        Gives the next possible angle to rotate the animal from starting position.

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

                new_x = round(position[0] + dx,3)
                new_y = round(position[1] + dy,3)
                if not self._point_exists(config.TILE_POSITIONS['yellow'], new_x, new_y):
                    check = False
                
            if check:
                return phi

            phi += rotate_angle
        
        return None

    def _calculate_offsets(self, dr, dphi, phi):
        total_angle_rad = math.radians(dphi + phi)
        
        dy = dr * math.cos(total_angle_rad)
        dx = dr * math.sin(total_angle_rad)
        
        return dx, dy

    def _point_exists(self, board_points: set[tuple[float, float]], x, y):
        for point in board_points:
            if self._are_points_close(point,(x,y)):
                return True
        return False    
        
    def _are_points_close(self, p1, p2, toleranz=1e-3):
        x1, y1 = p1
        x2, y2 = p2
        
        return math.isclose(x1, x2, abs_tol=toleranz) and math.isclose(y1, y2, abs_tol=toleranz)

class Token():
    """
    Represents a single game token with a specific state (e.g., color).

    Args:
        state (str): The state of the token, typically its color.
    """
    def __init__(self, state):
        if state not in config.ALLOWED_TOKEN_STATES:
            self.type = None
            raise ValueError(f'The given state "{state}" is not compatible with the possible states of a Token')
        else:
            self.type = state

    def __repr__(self):
        return f'<Token: {self.type}>'
    
    def to_dict(self):
        return {'type': self.type}
