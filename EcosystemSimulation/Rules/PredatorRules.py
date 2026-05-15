
from .GeneticAlgorithms import predGenetic
import math
import  random
from .Rules import randomAction
from Entities.Prey import Prey
SIMULATION_BEHAVIOR_LOG = []

import numpy as np

# Hunger
def predatorHungerRules(predator, grid):
    from .Rules import getView, getNumberOfPredatorsAndPrey
    view, relativeLocation = getView(predator,grid, 3)
    predator.relativeLocation = relativeLocation
    scores = {
        'hungerScore': 0,
        'agroScore': 0,
        'lonelynessScore': 0,
        'otherScore': 0.5}
    
    numPred, numPrey = getNumberOfPredatorsAndPrey(view)

    proximityPrey = numPrey / (len(view)^2)
    proximityPred = numPred / (len(view)^2)
    

    if (predator.energy - predator.energyLoss <= 0):
        scores['hungerScore'] = 1
    elif(predator.energy/predator.energyLoss < predator.agressiveness):
        scores['hungerScore'] = predator.foodDrive
    else:
        scores['hungerScore'] = 0.25

    if (predator.packMentality > proximityPred):
        scores["lonelynessScore"] = proximityPred


    if (predator.agressiveness > proximityPrey):
        scores['agroScore'] = predator.agressiveness


    #action = np.argmax(scores)
    action = max(scores, key=scores.get)
    
    if hasattr(predator, "lifeLog"):
        acts = predator.lifeLog.setdefault("actions", {})
        acts[action] = acts.get(action, 0) + 1
    
    return do(action, predator, grid, view)


def do(action, predator, grid, view):
    if action == 'hungerScore':
        return doHungerAction(predator, view)
    if action == 'lonelynessScore':
        return doLonelyAction(predator, view)
    if action == 'agroScore':
        return doAgroAction(predator, view)
    return randomAction(predator, view)

# def doHungerAction(predator, view):
#     closest = None
#     organisms = []
#     for i,row in enumerate(view):
#         for k,col in enumerate(row):
#             curOrg = view[i][k].organism 
#             if curOrg:
#                 if curOrg.type == predator.type:
#                     organisms.append(curOrg)
#     if len(organisms) == 0:
#         return doLonelyAction(predator, view)
    
#     predRow, predCol = predator.location
#     nearest = organisms[0]
#     row,col = nearest.location
#     curLowest = (abs(col-predCol) + abs(row-predRow))
#     for org in organisms:
#         row, col = org.location
#         if (abs(col-predCol) + abs(row-predRow)) < curLowest:
#             curLowest = (abs(col-predCol) + abs(row-predRow))
#             nearest = org
#     col, row = nearest.location
#     return (predCol-col, predRow-row)

def doHungerAction(predator, view):
    # Look for prey
    organisms = []
    for row in view:
        for cell in row:
            if isinstance(cell.organism, Prey):
                organisms.append(cell.organism)

    # No prey 
    if not organisms:
        return doLonelyAction(predator, view)

    # Move toward the first prey found
    target = organisms[0]
    pr, pc = predator.location
    tr, tc = target.location

    dRow = 1 if tr > pr else -1 if tr < pr else 0
    dCol = 1 if tc > pc else -1 if tc < pc else 0

    return dRow, dCol

    
def doAgroAction(predator, view):
    return randomAction(predator, view)

def doLonelyAction(predator, view):
    return randomAction(predator, view)


# Reproduction
def predatorReproductionRules(predator, grid):
    from .Rules import getView, getNumberOfPredatorsAndPrey, findSameSpecies
    view, relativeLocation = getView(predator, grid, 3)

    predAmt, preyAmt = getNumberOfPredatorsAndPrey(view)

    npSize = np.array(view).size

    total_density = (predAmt + preyAmt) / npSize
    
    if total_density >= predator.agressiveness:
        #print("To many Enities")
        return None, None

    species_density = predAmt / npSize
    if species_density <= predator.packMentality:
        #print("To Lonely")
        return None, None

    mate = findSameSpecies(view, predator) 

    if mate:
        offspring = predGenetic(predator, mate)
        return offspring, mate
    #print("No near By Preadators")

    return None, None


