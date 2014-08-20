"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        if not self.is_empty(row, col):
            raise Exception('Cannot add zombie to cell (%d, %d), there is an obstacle' \
                            % (row, col))
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        if not self.is_empty(row, col):
            raise Exception('Cannot add human to cell (%d, %d), there is an obstacle' \
                            % (row, col))
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def _clone_grid(self):
        """
        Clone obstacle grid
        """
        clone = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if not self.is_empty(row, col):
                    clone.set_full(row, col)
        return clone
    
    def _get_entity_list(self, entity_type):
        """
        Return list of entities with specified type (humans or zombies)
        """
        if entity_type == HUMAN:
            return self.humans()
        elif entity_type == ZOMBIE:
            return self.zombies()
        else:
            raise Exception('Unknown entity type: ' + entity_type)

    def _get_base_distances(self):
        """
        Return base distances grid (all cells preset to max value)
        """
        max_distance = self.get_grid_height() * self.get_grid_width()
        distances = [[max_distance for dummy_col in range(self.get_grid_width())] \
                      for dummy_row in range(self.get_grid_height())]
        return distances
    
    def _bfs(self, entity_type, visited, distances, cell_queue):
        """
        Compute all the distances using breadth-first search
        """
        while not len(cell_queue) == 0:
            cell = cell_queue.dequeue()
            distance = distances[cell[0]][cell[1]]
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                row, col = neighbor[0], neighbor[1]
                if visited.is_empty(row, col):
                    distances[row][col] = min(distances[row][col], distance + 1)
                    visited.set_full(row, col)
                    cell_queue.enqueue(neighbor)
        return distances    
    
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = self._clone_grid()
        entity_list = self._get_entity_list(entity_type)
        distances = self._get_base_distances()
        cell_queue = poc_queue.Queue()
        for entity in entity_list:
            # distance to self is zero
            distances[entity[0]][entity[1]] = 0
            cell_queue.enqueue(entity)
        distances = self._bfs(entity_type, visited, distances, cell_queue)
        return distances
    
    def _best_distance(self, cells, distances, worst_distance, is_better):
        """
        Return best distance across all possible
        """
        best_distance = worst_distance
        for cell in cells:
            cur_distance = distances[cell[0]][cell[1]]
            if is_better(cur_distance, best_distance):
                best_distance = cur_distance
        return best_distance
    
    def _move(self, cells, distances, worst_distance, is_better):
        """
        Return optimal cell to move to (according to distances grid and is_better strategy)
        """
        best_distance = self._best_distance(cells, distances, worst_distance, is_better)
        all_best = []
        for cell in cells:
            if distances[cell[0]][cell[1]] == best_distance:
                all_best.append(cell)
        return random.choice(all_best)
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_idx = 0
        for human in self.humans():
            neighbors = [cell for cell in self.eight_neighbors(human[0], human[1]) \
                         if self.is_empty(cell[0], cell[1])]
            neighbors.append(human)
            self._human_list[human_idx] = self._move(neighbors, zombie_distance, 0,
                                                     lambda x, y: x > y)
            human_idx += 1
            
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        max_distance = self.get_grid_height() * self.get_grid_width()
        zombie_idx = 0
        for zombie in self.zombies():
            neighbors = [cell for cell in self.four_neighbors(zombie[0], zombie[1]) \
                         if self.is_empty(cell[0], cell[1])]
            neighbors.append(zombie)
            self._zombie_list[zombie_idx] = self._move(neighbors, human_distance, max_distance,
                                                     lambda x, y: x < y)
            zombie_idx += 1

# poc_zombie_gui.run_gui(Zombie(30, 40))
