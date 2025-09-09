import config # Assuming you have a config.py file
import math

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
