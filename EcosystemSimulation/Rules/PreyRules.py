from .Rules import getView, findSameSpecies, getNearestTerrain, getNearestPredator, nearestPredatorDistance
from .GeneticAlgorithms import preyGenetic
from Entities.Prey import Prey
from Entities.Predator import Predator

# Movement
def preyMovementRules(prey, grid):
    view, origin = getView(prey, grid, prey.moveDistance)
    
    predator = getNearestPredator(view, origin)
    if predator:
        # flee
        return flee(prey, predator, grid)

    return (0, 0)  

# Hunger
def preyHungerRules(prey, grid):
    view, origin = getView(prey, grid, prey.moveDistance)
    px, py = prey.location

    predator = getNearestPredator(view, origin)
    if predator:
        return flee(prey, predator, grid)

    # seek food
    if prey.energy < prey.maxEnergy * 0.15:

        foodTile = getNearestTerrain(view, origin)
        if foodTile:
            terrain, (fx, fy) = foodTile

            dx = fx - px
            dy = fy - py

            if abs(dx) > abs(dy):
                dCol = 1 if dx > 0 else -1
                dRow = 0
            else:
                dRow = 1 if dy > 0 else -1
                dCol = 0

            # eat tile
            if (px + dRow, py + dCol) == (fx, fy):
                terrain.eaten()
                prey.feed(5)

            return dRow, dCol

    # move
    return preyMovementRules(prey, grid)


# Reproduction
def preyReproductionRules(prey, grid):
    view, origin = getView(prey, grid, 3)

    mate = findSameSpecies(view, prey)
    if mate:
        offspring = preyGenetic(prey, mate)
        prey.hasReproduced = True
        mate.hasReproduced = True
        return mate, offspring

    return None, None

# flee
def flee(prey, predator, grid):
    px, py = prey.location
    ex, ey = predator.location

    dx = px - ex
    dy = py - ey

    if abs(dx) > abs(dy):
        step_x = 1 if dx > 0 else -1
        step_y = 0
    else:
        step_x = 0
        step_y = 1 if dy > 0 else -1

    new_x = px + step_x
    new_y = py + step_y

    if not (0 <= new_x < grid.size and 0 <= new_y < grid.size):
        return 0, 0 

    # avoid running into predator 
    target_cell = grid.grid[new_y][new_x]
    if isinstance(target_cell.organism, Predator):
        return 0, 0 
    
    # movement
    prey.location = (new_x, new_y)

    return new_y - py, new_x - px