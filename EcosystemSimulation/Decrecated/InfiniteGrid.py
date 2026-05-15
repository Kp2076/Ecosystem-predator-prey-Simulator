import random
from Grid.Grid import Grid, Cell

class InfiniteGrid(Grid):

    MAX_WALL_HITS = 3   # hits before forced turn

    def __init__(self, width, height):
        super().__init__(width, height)
        self.wall_hits = {}     # { id(entity): count }

    # Hit 
    def get_hit_count(self, entity):
        return self.wall_hits.get(id(entity), 0)

    def increment_hit(self, entity):
        oid = id(entity)
        self.wall_hits[oid] = self.get_hit_count(entity) + 1

    def reset_hit(self, entity):
        self.wall_hits[id(entity)] = 0

    def detect_border_hit(self, entity, new_x, new_y):
        if new_x < 0:
            return "left"
        if new_x + entity.width > self.width:  
            return "right"
        if new_y < 0:
            return "top"
        if new_y + entity.height > self.height:
            return "bottom"
        return None
    
    # Turn
    def force_turn(self, entity):
        dx, dy = entity.direction
        if dx != 0:  # moving horizontally → turn up/down
            entity.direction = random.choice([(0, 1), (0, -1)])
        else:        # moving vertically → turn left/right
            entity.direction = random.choice([(1, 0), (-1, 0)])

    # Expand in correct direction
    def expand(self, direction):
        if direction == "left":
            new_cols = [[Cell() for _ in range(self.height)]]
            self.grid = new_cols + self.grid
            self.width += 1

        elif direction == "right":
            new_cols = [[Cell() for _ in range(self.height)]]
            self.grid += new_cols
            self.width += 1

        elif direction == "top":
            for x in range(self.width):
                self.grid[x] = [Cell()] + self.grid[x]
            self.height += 1

        elif direction == "bottom":
            for x in range(self.width):
                self.grid[x].append(Cell())
            self.height += 1

    # Expand Grid
    def expand_grid(self, x, y):
        """Expand grid to include coordinate (x, y)."""
        add_left = max(0, -x)
        add_right = max(0, x - (self.width - 1))
        add_top = max(0, -y)
        add_bottom = max(0, y - (self.height - 1))

        if add_left == add_right == add_top == add_bottom == 0:
            return False  # No expansion 

        if add_left > 0:
            new_cols = [[Cell() for _ in range(self.height)] for _ in range(add_left)]
            self.grid = new_cols + self.grid
            self.width += add_left

        if add_right > 0:
            new_cols = [[Cell() for _ in range(self.height)] for _ in range(add_right)]
            self.grid += new_cols
            self.width += add_right

        if add_top > 0:
            for x in range(self.width):
                self.grid[x] = [Cell() for _ in range(add_top)] + self.grid[x]
            self.height += add_top

        if add_bottom > 0:
            for x in range(self.width):
                self.grid[x] += [Cell() for _ in range(add_bottom)]
            self.height += add_bottom

        return True

    # Movement
    def movement(self, entity, new_x, new_y):
        border = self.detect_border_hit(entity, new_x, new_y)

        if border is None:
            self.reset_hit(entity)
            return super().update_organism_position(entity, new_x, new_y)

        self.increment_hit(entity)

        if self.get_hit_count(entity) >= self.MAX_WALL_HITS:
            print("WALL HIT 3X → forced turn")  # Debugging
            self.reset_hit(entity)
            self.force_turn(entity)
            return False  

        self.expand(border)
        return False
