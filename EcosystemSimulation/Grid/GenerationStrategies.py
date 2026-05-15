from Grid.Grid import Grid, Cell
from Entities.Terrain import Terrain
from Entities.Prey import Prey
from Entities.Predator import Predator
import random

maxMove = 3
defaultAmt = 200

maxEnergyLoss = 4
minEnergyLoss = 2
maxEnergy = 13
minEnergy = 8

def generationStrategyFullGrass(size):
    return [[Cell(Terrain(3, 'grass')) for _ in range(size)] for _ in range(size)]

def generationStrategyAnimalsRandom(grid, preyAmt = defaultAmt, predAmt = defaultAmt):
    preyList = []
    for i in range(preyAmt):
        preyList.append(generateRandomPrey())
        placeRandomOrganism(grid, preyList[i])
        
    predatorList = []
    for i in range(predAmt):
        predatorList.append(generateRandomPredator())
        placeRandomOrganism(grid, predatorList[i])

    return grid

def placeRandomOrganism(grid, organism):
        placed = False
        while(not placed):
            col = random.randint(0,len(grid)-1)
            row = random.randint(0,len(grid)-1)
            if grid[row][col].organism is None:
                placed = True
                organism.location = (row,col)
                grid[row][col].organism = organism



def generateRandomPrey():
    attributes = generateRandomOrganismAttributes()
    attributes["fearFactor"] = random.random()
    attributes["agressiveness"] = 0      
    attributes["foodDrive"] = 0          
    attributes["type"] = "prey"
    return Prey(attributes)

def generateRandomPredator():
    attributes = generateRandomOrganismAttributes()
    attributes["agressiveness"] = random.random()
    attributes["fearFactor"] = 0         
    attributes["foodDrive"] = random.random()
    attributes["type"] = "predator"

    return Predator(attributes)

def generateRandomOrganismAttributes():
    attributes = {}
    attributes["climateSensetivity"] =random.random()
    attributes["reproductionRate"] = random.random()
    attributes["size"] = random.random()
    attributes["moveDistance"] = random.randint(1, maxMove)
    attributes["packMentality"] = random.random()
    attributes["maxEnergy"] = random.randint(minEnergy, maxEnergy)
    attributes['energyLoss'] = random.randint(minEnergyLoss, maxEnergyLoss)
    return attributes

