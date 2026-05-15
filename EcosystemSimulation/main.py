import time
from Grid.Grid import Grid
import random
import matplotlib.pyplot as plt
import numpy as np

from Rules.PredatorRules import SIMULATION_BEHAVIOR_LOG
from Data.DataExtraction import loadMammalTraitRow
from Predator_Prey_Relationship import compareBehaviorToDataset
from Entities.Predator import Predator
from Entities.Prey import Prey

def buildSimulationBehaviorLog(grid):
    SIMULATION_BEHAVIOR_LOG.clear()

    for row in grid.grid:
        for cell in row:
            org = cell.organism
            if org is None:
                continue
            if not getattr(org, "alive", False):
                continue

            life = getattr(org, "lifeLog", {})
            steps = life.get("stepsSurvived", 0)
            totalEnergy = life.get("totalEnergy", 0.0)
            avgEnergy = totalEnergy / steps if steps > 0 else 0.0

            entry = {
                "type": getattr(org, "type", None),
                "energy": getattr(org, "energy", 0),
                "reproductionRate": getattr(org, "reproductionRate", 0),
                "size": getattr(org, "size", 0),
                "aggression": getattr(org, "agressiveness", 0) if hasattr(org, "agressiveness") else getattr(org, "fearFactor", 0),
                "climateSensetivity": getattr(org, "climateSensetivity", 0),
                "moveDistance": getattr(org, "moveDistance", 0),
                "packMentality": getattr(org, "packMentality", 0),
                "maxEnergy": getattr(org, "maxEnergy", 0),
                "energyLoss": getattr(org, "energyLoss", 0),
                "stepsSurvived": steps,
                "avgEnergy": avgEnergy,
                "actions": life.get("actions", {}),
            }
            SIMULATION_BEHAVIOR_LOG.append(entry)

def validateSimulation(grid):
    print("\n=== VALIDATION RESULTS ===")

    traitRows = loadMammalTraitRow("mammalAnimals.csv")
    if not traitRows:
        print("No trait data found.")
        return

    # Build the behavior log
    buildSimulationBehaviorLog(grid)

    # groupValidation
    from collections import defaultdict

    predatorMatches = defaultdict(list)
    preyMatches = defaultdict(list)

    predatorsAlive = []
    preyAlive = []

    for entry in SIMULATION_BEHAVIOR_LOG:
        orgType = entry.get("type")
        if orgType not in ("predator", "prey"):
            continue

        if orgType == "predator":
            predatorsAlive.append(entry)
        elif orgType == "prey":
            preyAlive.append(entry)

        species, score = compareBehaviorToDataset(entry, traitRows)

        if orgType == "predator":
            predatorMatches[species].append(score)
        elif orgType == "prey":
            preyMatches[species].append(score)

    # --- PRINT RESULTS ---

    print("\n--- Predator validation ---")
    if predatorMatches:
        # Sort species by how many predators matched them
        sortedPredators = sorted(predatorMatches.items(), key=lambda x: len(x[1]), reverse=True)
        for species, scores in sortedPredators:
            avgScore = sum(scores) / len(scores)
            print(f"{species}: {len(scores)} predators matched (average similarity={avgScore:.2f})")
    else:
        print("No predators were tracked or survived.")

    print("\n--- Prey validation ---")
    if preyMatches:
        sortedPrey = sorted(preyMatches.items(), key=lambda x: len(x[1]), reverse=True)
        for species, scores in sortedPrey:
            avgScore = sum(scores) / len(scores)
            print(f"{species}: {len(scores)} prey matched (average similarity={avgScore:.2f})")
    else:
        print("No prey were tracked or survived.")
    printAvgTraits(predatorsAlive, "Predators")
    printAvgTraits(preyAlive, "Prey")


def printAvgTraits(entries, label):
    if not entries:
        print(f"\nNo data for {label}")
        return

    print(f"\n--- Average Traits of {label} (Compared to Dataset) ---")

    keys = [
        "reproductionRate", "size", "aggression", "climateSensetivity",
        "moveDistance", "packMentality", "maxEnergy", "energyLoss"
    ]

    traitSums = {k: 0.0 for k in keys}
    count = len(entries)

    for entry in entries:
        for k in keys:
            traitSums[k] += entry.get(k, 0)

    for k in keys:
        avgVal = traitSums[k] / count
        print(f"{k}: {avgVal:.3f}")

def spawnOrganisms(grid, numPred, numPrey):

    # random placement
    def place(org):
        while True:
            r = random.randint(0, grid.size - 1)
            c = random.randint(0, grid.size - 1)
            if grid.grid[r][c].organism is None:
                org.location = (r, c)
                grid.grid[r][c].organism = org
                return

    # prey
    for _ in range(numPrey):
        prey = Prey(grid.randomPreyAttributes())  
        place(prey)

    # predators
    for _ in range(numPred):
        pred = Predator(grid.randomPredatorAttributes())   
        place(pred)


def main():
    random.seed(time.time())

    print("\nSpawn animals manually or randomly?")
    print(" 1 Manual (choose number of predators & prey)")
    print(" 2 Random")
    choice = input("Choice: ").strip()

    print("\nEnter grid size \nMinimum grid size for Random is 20")
    gridSize = int(input(" Grid size (e.g., 45): "))

    grid = Grid(gridSize)

    if choice == "1":
        pred_count = int(input(" Predator count: "))
        prey_count = int(input(" Prey count: "))
        
        # spawn predators
        for _ in range(pred_count):
            attrs = grid.randomPredatorAttributes()
            grid.spawnAnimal(Predator(attrs))

        # spawn prey
        for _ in range(prey_count):
            attrs = grid.randomPreyAttributes()
            grid.spawnAnimal(Prey(attrs))

    else:
        from Grid.GenerationStrategies import generationStrategyAnimalsRandom
        generationStrategyAnimalsRandom(grid.grid)

    # Tick Count
    numTicks = int(input("\n Number of Ticks: "))
    print("\n")

    print("\nInitial (Tick 0)")
    grid.display()

    totalPredPop = []
    totalPreyPop = []
    ticks = []

    totalPredPop.append( int(grid.alivePred))
    totalPreyPop.append(int(grid.alivePrey))
    ticks.append(int(0))
    
    print("\nAlive:")
    # print(" Total:", count)
    print(" Predators:", grid.alivePred)
    print(" Prey:", grid.alivePrey)
    print("\n")

    for tick in range(1, numTicks + 1):    
        print(f"\nTick ({tick})")

        grid.runThough()
        count = grid.display()
        

        if (tick % 1) == 0:
            totalPredPop.append( int(grid.alivePred))
            totalPreyPop.append(int(grid.alivePrey))
            ticks.append(int(tick))

        print("\nAlive:")
        print(" Total:", count)
        print(" Predators:", grid.alivePred)
        print(" Prey:", grid.alivePrey)

        print("\nBorn:")
        print(" Predators:", grid.predBorn)
        print(" Prey:", grid.preyBorn)

        print("\nStarved:")
        print(" Predators:", grid.predStarveCount)

        print("\nNum of Preys that have been Eaten")
        print(" Prey eaten:", grid.preyEatenCount)

        time.sleep(0.5)
        # time.sleep(3)

    # print(np.array(ticks))
    # print(totalPredPop)
    plt.plot(np.array(ticks), np.array(totalPredPop), color='red', linewidth=3, label="Predator")
    plt.plot(np.array(ticks), np.array(totalPreyPop), color='blue', linewidth=3, label="Prey")
    plt.legend()
    plt.show()
    validateSimulation(grid)

main()
