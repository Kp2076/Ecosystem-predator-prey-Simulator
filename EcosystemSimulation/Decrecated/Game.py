
from Grid.Grid import Grid
from Entities.Organism import Organism
from Entities.Predator import Predator
from Entities.Prey import Prey

class Game:

    def __init__(self, size):

        self.grid = Grid(size)
        self.predators = []
        self.preys = []
        self.time = 0
        predatorReproductionCount = 0
        preyReproductionCount = 0

    def tick(self):
        for predator in self.predators:
            self.grid.applyMovementPredatorRules(predator)
            reproduced = self.grid.applyPredatorReproductionRules(predator)
            if (reproduced):
                predatorReproductionCount += 1
        
        for prey in self.preys:
            self.grid.applyMovementPreyRules(prey)
            reproduced = self.grid.applyPreyReproductionRules(prey)
            if (reproduced):
                preyReproductionCount += 1

        self.time += 1

        self.grid.display(self.predators, self.prey)

    def gameOver(self):
        return self.time