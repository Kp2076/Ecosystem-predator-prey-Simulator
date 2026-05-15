import random
import time
from Decrecated.FiniteGrid import FiniteGrid

class Game:
    def __init__(self, grid, ui=None):
        self.grid = grid
        self.ui = ui
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def try_move(self, entity, dx, dy):
        nx, ny = entity.x + dx, entity.y + dy
        if isinstance(self.grid, FiniteGrid):
            for ax in range(entity.width):
                for ay in range(entity.height):
                    if not self.grid.is_in_bounds(nx + ax, ny + ay):
                        return False, entity.x, entity.y
        return True, nx, ny

    def handle_collision(self, entity, nx, ny):
        for dx in range(entity.width):
            for dy in range(entity.height):
                tx, ty = nx + dx, ny + dy
                if self.grid.is_in_bounds(tx, ty):
                    cell_entities = self.grid.get_cell(tx, ty)
                    for other in cell_entities:
                        if other is not entity:
                            # Predator eats prey
                            if entity.role == "predator" and other.role == "prey":
                                print(f"{entity.name} ate {other.name}!")
                                if other in self.entities:
                                    self.entities.remove(other)
                                return False  # predator still moves
                            # Prey avoids predator
                            if entity.role == "prey" and other.role == "predator":
                                print(f"{entity.name} avoided {other.name}!")
                                return True  # block move
                            # Otherwise block overlapping
                            return True
        return False

    def movement_logic(self, entity):
        # Pick a random direction each tick
        entity.direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        dx, dy = entity.direction
        ok, nx, ny = self.try_move(entity, dx, dy)
        if ok and not self.handle_collision(entity, nx, ny):
            return nx, ny
        return entity.x, entity.y

    def run_loop(self):
        while True:
            for entity in self.entities:
                nx, ny = self.movement_logic(entity)
                self.grid.movement(entity, nx, ny) 
            if self.ui:
                self.ui.flag_redraw = True
            time.sleep(0.4)
