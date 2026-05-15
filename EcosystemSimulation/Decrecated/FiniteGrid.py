import random
from Grid.Grid import Grid

class FiniteGrid(Grid):
    def add_entity(self, organism, x, y):
        for dx in range(organism.width):
            for dy in range(organism.height):
                if not self.is_in_bounds(x + dx, y + dy):
                    return False
        return super().set_cell(organism, x, y)  

    # Wall collision
    def handle_wall_collision(self, organism):
        dx, dy = organism.direction
        if organism.x == 0 and dx < 0:
            organism.direction = random.choice([(0, 1), (0, -1)])
            return True
        if organism.x + organism.width - 1 == self.width - 1 and dx > 0:
            organism.direction = random.choice([(0, 1), (0, -1)])
            return True
        if organism.y == 0 and dy < 0:
            organism.direction = random.choice([(1, 0), (-1, 0)])
            return True
        if organism.y + organism.height - 1 == self.height - 1 and dy > 0:
            organism.direction = random.choice([(1, 0), (-1, 0)])
            return True
        return False

    def movement(self, organism, new_x, new_y):
        for dx in range(organism.width):
            for dy in range(organism.height):
                if not self.is_in_bounds(new_x + dx, new_y + dy):
                    self.handle_wall_collision(organism)
                    return False
        return super().update_organism_position(organism, new_x, new_y)
