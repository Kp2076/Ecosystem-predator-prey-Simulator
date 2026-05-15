
from Entities.Terrain import Terrain
from Entities.Predator import Predator
from Entities.Prey import Prey
import random
import copy

class Cell:
    def __init__(self, terrain):
        self.terrain = terrain
        self.organism = None

class Grid:
    def __init__(self, size):
        self.size = size
        # To prevent Cirular Initialization 
        from .GenerationStrategies import generationStrategyFullGrass
        self.grid = generationStrategyFullGrass(size)

        # Predator
        self.predStarveCount = 0
        self.predBorn = 0
        self.alivePred = 0

        # Prey
        self.preyBorn = 0
        self.preyEatenCount = 0
        self.alivePrey = 0
        
    def getView(self, location, size):
        x,y = location
        yStart = max(0, y-size)
        yEnd = min(self.size, y + size + 1)
        xStart = max(0, x-size)
        xEnd = min(self.size, x + size + 1)
        return [row[xStart:xEnd] for row in self.grid[yStart:yEnd]]

    def runThough(self):
        from Rules.PredatorRules import predatorHungerRules, predatorReproductionRules
        from Rules.PreyRules import preyHungerRules, preyReproductionRules

        reproductionList = []
        for i, row in enumerate (self.grid):
            for k, cell in enumerate(row):
                cell.terrain.grow()
                
                if not (cell.organism is None):
                    
                    if (cell.organism):
                     cell.organism.age()
                    if not cell.organism.alive:
                        if isinstance(cell.organism, Predator):
                            self.predStarveCount += 1
                        cell.organism = None
                        continue

                    # Predator
                    if isinstance(cell.organism, Predator):
                        # Repoduction First
                        if(cell.organism not in reproductionList):
                            offspring, mate = predatorReproductionRules(cell.organism, self)
                            if offspring is not None:
                                self.addNearby((i,k), offspring)
                                reproductionList.append(cell.organism)
                                reproductionList.append(mate)
                                self.predBorn += 1
                        #     else:
                        #         print("No Offspring")
                        # else:
                        #     print("In List")
                        oRow, oCol = predatorHungerRules(cell.organism, self)
                        targetCell = self.grid[i + oRow][k + oCol]

                        # Number of Prey that have been Eaten
                        if isinstance(targetCell.organism, Prey):
                                self.preyEatenCount += 1

                        # Then Move
                        organism = copy.deepcopy(cell.organism)
                        organism.location = (i+oRow,k+oCol)
                        self.grid[i+oRow][k+oCol].organism = organism
                        cell.organism = None

                    # Prey
                    elif isinstance(cell.organism, Prey):
                        # Reproduce
                        if cell.organism not in reproductionList:
                            mate, offspring = preyReproductionRules(cell.organism, self)
                            if offspring is not None:
                                self.addNearby((i, k), offspring)
                                reproductionList.append(cell.organism)
                                reproductionList.append(mate)
                                self.preyBorn += 1
                        # Hunger
                        dRow, dCol = preyHungerRules(cell.organism, self)
                        newRow, newCol = i + dRow, k + dCol

                        if 0 <= newRow < self.size and 0 <= newCol < self.size:
                            targetCell = self.grid[newRow][newCol]
                            if isinstance(targetCell.organism, Prey):
                                self.preyEatenCount += 1

                            organism = copy.deepcopy(cell.organism)
                            organism.location = (newRow, newCol)
                            self.grid[newRow][newCol].organism = organism
                            cell.organism = None
                        else:
                            return None
                        
    def display(self):
        count = 0
        predCount = 0
        preyCount = 0

        for row in self.grid:
            rowStr = ""
            for cell in row:
                if cell.organism is not None:
                    count += 1
                    if isinstance(cell.organism, Predator):
                        predCount += 1
                    elif isinstance(cell.organism, Prey):
                        preyCount += 1
                    rowStr += cell.organism.sprite
                else:
                    rowStr += cell.terrain.getSprite()
            print(rowStr)

        self.alivePred = predCount
        self.alivePrey = preyCount

        return count


    ##### IMPROVE ######
    def addRandomish(self, loc, offspring):
        while (True):
            count = 0
            row = random.randint(0,len(self.grid)-1)
            col = random.randint(0,len(self.grid)-1)

            if self.grid[row][col].organism is None:
                offspring.location = (row,col)
                self.grid[row][col].organism = offspring
                return

            count += 1
            if count >= 2500:
                print("Error")
                return

    def addNearby(self, loc, offspring, size=1):
        base_row, base_col = loc
        candidates = []

        for dr in range(-size, size + 1):
            for dc in range(-size, size + 1):
                r = base_row + dr
                c = base_col + dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.grid[r][c].organism is None:
                        candidates.append((r, c))

        if candidates:
            row, col = random.choice(candidates)
            offspring.location = (row, col)
            self.grid[row][col].organism = offspring
            return

        # fallback to random if neighbourhood is full
        self.addRandomish(loc, offspring)
        
    def getTerrain(self, location, size):
        view = self.getView(location, size)
        px, py = location

        nearest = None
        bestDist = float()

        for cell, x, y in view: # check getview updated return
            terrain = cell.terrain

            if terrain.currentGrowth == 0:   
                dist = abs(x - px) + abs(y - py) # manhattan distance

                if dist < bestDist:
                    bestDist = dist
                    nearest = terrain

        return nearest
    
    # Predator
    def randomPredatorAttributes(self):
        return {
            "type": "predator",
            "climateSensetivity": random.uniform(0.1, 1.0),
            "reproductionRate": random.uniform(0.02, 0.10),
            "size": random.randint(3, 10),
            "moveDistance": random.randint(1, 3),
            "packMentality": random.uniform(0.2, 0.8),
            "maxEnergy": random.randint(20, 40),
            "energyLoss": random.randint(5, 10),
            "agressiveness": random.uniform(0.3, 1.0),
            "foodDrive": random.uniform(0.3, 1.0),
            "fearFactor": 0,  
        }

    # Prey
    def randomPreyAttributes(self):
        return {
            "type": "prey",
            "climateSensetivity": random.uniform(0.1, 1.0),
            "reproductionRate": random.uniform(0.05, 0.20),
            "size": random.randint(1, 5),
            "moveDistance": random.randint(1, 3),
            "packMentality": random.uniform(0.1, 0.4),
            "maxEnergy": random.randint(15, 35),
            "energyLoss": random.randint(5, 10),
            "fearFactor": random.uniform(0.5, 1.0),
            "agressiveness": 0, 
            "foodDrive": 0,      
        }
    
    def spawnAnimal(self, organism):
        size = len(self.grid)
        while True:
            r = random.randint(0, size - 1)
            c = random.randint(0, size - 1)
            if self.grid[r][c].organism is None:
                organism.location = (r, c)
                self.grid[r][c].organism = organism
                return
