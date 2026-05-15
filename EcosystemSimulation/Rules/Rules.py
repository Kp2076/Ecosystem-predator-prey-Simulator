from Entities.Predator import Predator
from Entities.Prey import Prey
import random
import time

def getNearestTerrain(view, origin):
    px, py = origin
    nearest = None
    bestDist = float("inf")

    for dy, row in enumerate(view):
        for dx, cell in enumerate(row):
            terrain = cell.terrain

            # edible = fully grown
            if terrain.currentGrowth == 0:
                dist = abs(dx) + abs(dy)
                if dist < bestDist:
                    bestDist = dist
                    nearest = (terrain, (px + dx, py + dy))

    return nearest

def getNearestPredator(view, origin):
    px, py = origin
    nearest = None
    bestDist = float("inf")

    for dy, row in enumerate(view):
        for dx, cell in enumerate(row):
            org = cell.organism
            if isinstance(org, Predator):
                dist = abs(dx) + abs(dy)
                if dist < bestDist:
                    bestDist = dist
                    nearest = org

    return nearest

def getView(organism, grid, size):
    row, col = organism.location
    cells = grid.grid  
    maxSize = grid.size
    colStart = max(0, col - size)
    colEnd   = min(maxSize, col + size + 1)
    rowStart = max(0, row - size)
    rowEnd   = min(maxSize, row + size + 1)

    view = [cells[r][colStart:colEnd] for r in range(rowStart, rowEnd)]

    for rIndex, r in enumerate(view):
        for cIndex, cell in enumerate(r):
            if cell.organism == organism:
                return view, (rIndex, cIndex)

    print('Organism Not in view')
    print(organism.location)
    print("Col")
    print(colStart)
    print(colEnd)
    print("Row")
    print(rowStart)
    print(rowEnd)
    return view, (-1,-1)

def getNumberOfPrey(view):
    preyCount = 0
    for row in enumerate(view):
        for col in enumerate(row):
            if isinstance(view[row][col].organism, Prey):
                preyCount += 1
    return preyCount

def getNumberOfPredators(view):
    predCount = 0
    for row in enumerate(view):
        for col in enumerate(row):
            if isinstance(view[row][col].organism, Predator):
                predCount += 1
    return predCount

def getNumberOfPredatorsAndPrey(view):
    predCount = 0
    preyCount = 0
    for i, row in enumerate(view):
        for k, col in enumerate(row):
            if isinstance(view[i][k].organism, Prey):
                preyCount += 1
            if isinstance(col.organism, Predator):
                predCount += 1
    return predCount, preyCount

def nearestPredatorDistance(view, origin):
    predator = getNearestPredator(view, origin)
    if predator is None:
        return float("inf")

    px, py = origin
    ox, oy = predator.location

    return abs(ox - px) + abs(oy - py)

def randomAction(organism, view):
    prRow, prCol = organism.relativeLocation
    count = 0
    while (True):
        row = random.randint(0, len(view)-1)
        col = random.randint(0, len(view[0])-1)
        if view[row][col].organism == None:
            return (row-prRow, col-prCol)
        count += 1
        if count >= 100:
            return  (0,0)

def findSameSpecies(view, organism):
    organismList = []
    for i, row in enumerate(view):
        for k,col in enumerate(row):
            org = view[i][k].organism
            if not ( org == None):
                if org.type == organism.type:
                    if org != organism:
                        organismList.append(org)
    return maxFitness(organismList)

def countSameSpecies(view, organism):
    species = organism.type
    count = 0

    for row in view:
        for cell in row:
            if cell.organism and cell.organism.type == species:
                count += 1

    return count

###### ADD FITNESS FUNCTION #######
# Random For Now
def maxFitness(organismList):
    leng = len(organismList)
    if leng == 0:
        return None
    if leng == 1:
        return organismList[0]
    choice = random.randint(0,len(organismList)-1)
    return organismList[choice]
            













