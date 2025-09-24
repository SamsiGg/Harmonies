from __future__ import annotations
import math
from player import Player, Animal, Board, Tile
import config

class ScoreCalculator():

    def __init__(self):
        ...

    def calculate_total_score(self, player: Player):
        score = 0

        score += self._calculate_animal_score(player.animals)
        score += self._calculate_token_score(player.board)

        return score

    def _calculate_animal_score(self, animals: list[Animal]):
        score = 0
        for animal in animals:
            if len(animal.points) != animal.dice_amount:
                score += animal.points[len(animal.points) - animal.dice_amount - 1]

        return score
    
    def _calculate_token_score(self, board: Board):
        score = 0
        checked_tiles = set()

        for tile in board.tiles:
            score += self._calculate_tree_score(tile)
            score += self._calculate_stone_score(tile, board)

            if self.find_yellow(tile, board, checked_tiles):
                score += config.POINT_RULES['field']

            score += self._calculate_house_score(tile, board)

        score += self._calculate_water_score(board)


        return score

    def _calculate_tree_score(self, tile: Tile):
        is_tree_points = 0
        for tree_possibility in config.POINT_RULES['tree']:
            if len(tile.tokens) == len(tree_possibility[0]):
                is_tree_points = tree_possibility[1]
                for i,type in enumerate(tree_possibility[0]):
                    if type != tile.tokens[i].type:
                        is_tree_points = 0

        return is_tree_points
    
    def _calculate_stone_score(self, tile: Tile, board: Board):
        score = 0
        borders_stone = False

        if len(tile.tokens) == 0:
                return 0

        for token in tile.tokens:
            if token.type != 'grey':
                return 0
        
        # confirm, that this tile borders stone/grey
        neighbour_tiles = self._get_neighbour_tiles(tile, board)
        for neighbour_tile in neighbour_tiles:
            if len(neighbour_tile.tokens) > 0:
                if neighbour_tile.tokens[-1].type == 'grey':
                    borders_stone = True
                    break

        if borders_stone: return config.POINT_RULES['stone'][len(tile.tokens)-1]

        return 0
    
    def find_yellow(self, tile: Tile, board: Board, checked_tiles: set[Tile]):
        has_yellow_neighbour = False

        if tile in checked_tiles or len(tile.tokens) == 0:
            return False
        
        checked_tiles.add(tile)

        if tile.tokens[0].type == 'yellow':
            neighbour_tiles = self._get_neighbour_tiles(tile, board)
            for neighbour_tile in neighbour_tiles:
                if len(neighbour_tile.tokens) > 0:
                    if neighbour_tile.tokens[0].type == 'yellow':
                        has_yellow_neighbour = True
                        if neighbour_tile not in checked_tiles:
                            self.find_yellow(neighbour_tile, board, checked_tiles)

            if has_yellow_neighbour:
                return True
        
        return False

    def _calculate_house_score(self, tile: Tile, board: Board):
        score = 0

        if len(tile.tokens) != 2:
            return 0
        
        if (tile.tokens[0].type not in config.POINT_RULES['house'][0][0]
             or tile.tokens[1].type != config.POINT_RULES['house'][0][1]):
            return 0
        
        neighbouring_colours = set()

        neighbour_tiles = self._get_neighbour_tiles(tile, board)

        for neighbour_tile in neighbour_tiles:
            if len(neighbour_tile.tokens) > 0:
                neighbouring_colours.add(neighbour_tile.tokens[-1].type)

        if len(neighbouring_colours) >= 3:
            return config.POINT_RULES['house'][1]
        
        return 0

    def _calculate_water_score(self, board: Board):
        # 1. Get a list of all the puddles of water on the board.
        # 2. 

        score = 0

        # First step:

        puddle_list: list[set[Tile]] = []
        checked_tiles = set()

        for tile in board.tiles:

            puddle_tiles: set[Tile] = self.find_puddle(tile, board, checked_tiles)

            if puddle_tiles:
                puddle_list.append(puddle_tiles)

        # Second step

        for puddle in puddle_list:

            blue_neighbour_list: list[tuple[int, Tile]] = []

            for tile in puddle:

                if len(tile.tokens) != 1:
                    break

                if tile.tokens[0].type == 'blue':
                    neighbour_tiles = self._get_neighbour_tiles(tile, board)
                    amount_blue_neighbours = 0
                    for neighbour_tile in neighbour_tiles:
                        if len(neighbour_tile.tokens) == 1:
                            if neighbour_tile.tokens[0].type == 'blue':
                                amount_blue_neighbours += 1

                    blue_neighbour_list.append((amount_blue_neighbours,tile))

            lowest_blue_neighbours = self._find_start_stop_points(blue_neighbour_list)
            second_lowest_blue_neighbours = []

            if len(lowest_blue_neighbours) == 1:
                blue_neighbour_list.remove(lowest_blue_neighbours[0])
                lowest_blue_neighbours.extend(self._find_start_stop_points(blue_neighbour_list))

            # third step
            shortest_paths: list[set[Tile]] = []

            for start_tile in lowest_blue_neighbours:
                # to make sure the start point is always the first one, if it has 
                # a smaller amount of blue neighbours thant the others
                if len(lowest_blue_neighbours) > 1:
                    if lowest_blue_neighbours[0][0] != lowest_blue_neighbours[1][0]:
                        start_tile = lowest_blue_neighbours[0]
                for stop_tile in lowest_blue_neighbours:
                    if start_tile != stop_tile:
                        shortest_paths.append(self._find_shortest_path(start_tile[1], stop_tile[1], board, set()))

            longest_short_path = []
            for path in shortest_paths:
                if len(longest_short_path) == 0:
                    longest_short_path = path
                elif len(path) > len(longest_short_path):
                    longest_short_path = path

            pathlength = len(longest_short_path)

            if pathlength == 0:
                return 0
            
            if pathlength > 6:
                score += config.POINT_RULES['water'][5]
                score += (pathlength - 6) * 4
            else:
                score += config.POINT_RULES['water'][pathlength-1]
            
        return score
    
    def _find_shortest_path(self,
                            tile: Tile,
                            stop_tile: Tile,
                            board: Board,
                            current_path: set[Tile]):
        
        current_path.add(tile)

        if tile == stop_tile:
            return current_path
        
        neighbour_tiles = self._get_neighbour_tiles(tile, board)
        possible_paths: list[set[Tile]] = []

        for neighbour_tile in neighbour_tiles:
            if len(neighbour_tile.tokens) == 1 and neighbour_tile not in current_path:
                if neighbour_tile.tokens[0].type == 'blue':
                    path = self._find_shortest_path(neighbour_tile, stop_tile, board, current_path.copy())
                    if path:
                        possible_paths.append(path)

        shortest_path: set[Tile] = set()
        for possible_path in possible_paths:
            if len(shortest_path) == 0:
                shortest_path = possible_path
            elif len(possible_path) < len(shortest_path):
                    shortest_path = possible_path

        if shortest_path:
            return shortest_path
        else:
            return None
        
        
    
    def _find_start_stop_points(self, blue_neighbour_list: list[tuple[int, Tile]]):
        lowest_blue_neighbours = []

        for blue_neighbour_tile in blue_neighbour_list:
            
            if not lowest_blue_neighbours:
                lowest_blue_neighbours.append(blue_neighbour_tile)
            else:
                if blue_neighbour_tile[0] == lowest_blue_neighbours[0][0]:
                    lowest_blue_neighbours.append(blue_neighbour_tile)

                if blue_neighbour_tile[0] < lowest_blue_neighbours[0][0]:
                    lowest_blue_neighbours = [blue_neighbour_tile]

        return lowest_blue_neighbours
    
    def find_puddle(self, tile: Tile, board: Board, checked_tiles: set[Tile]):
        puddle_tiles = set()

        if tile in checked_tiles or len(tile.tokens) != 1:
            return []
        
        checked_tiles.add(tile)
        
        if tile.tokens[0].type == 'blue':
            puddle_tiles.add(tile)

            neighbour_tiles = self._get_neighbour_tiles(tile, board)
            
            for neighbour_tile in neighbour_tiles:
                puddle_tiles.update(self.find_puddle(neighbour_tile, board, checked_tiles))

        return puddle_tiles

    def find_water_path(self, tile: Tile, board: Board, current_water_path: set[Tile]):

        if tile in current_water_path or len(tile.tokens) != 1:
            return set()
        
        if tile.tokens[0].type == 'blue':
            current_water_path.add(tile)

            neighbour_tiles = self._get_neighbour_tiles(tile, board)
            
            future_paths: list[set[Tile]] = []
            for neighbour_tile in neighbour_tiles:
                future_paths.append(self.find_water_path(neighbour_tile, 
                                                         board, 
                                                         current_water_path.copy()))

            longest_path: set[Tile] = set()
            for future_path in future_paths:
                if len(future_path) > len(longest_path):
                    longest_path = future_path

            longest_path.add(tile)
            return longest_path
        return set()

    def _get_neighbour_tiles(self, tile: Tile, board: Board):
        tile_pos = tile.position

        tiles:set[Tile] = set()
        angle = 0

        while angle < 360:
            neighbour_pos = [0,0]
            neighbour_pos[0] = round(tile_pos[0] + math.sin(math.radians(angle)),3)
            neighbour_pos[1] = round(tile_pos[1] + math.cos(math.radians(angle)),3)
            neighbour_pos_tupel = (neighbour_pos[0],neighbour_pos[1])

            if neighbour_pos_tupel in config.TILE_POSITIONS['yellow']:
                for tile in board.tiles:
                    if tile.position == neighbour_pos_tupel:
                        tiles.add(tile)
                        break

            angle += 60
        
        return tiles


