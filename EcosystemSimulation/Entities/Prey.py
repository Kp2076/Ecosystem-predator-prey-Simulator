from Entities.Organism import Organism
import random

class Prey(Organism):
    def __init__(self, attributes):
        super().__init__(attributes)
        self.type = "prey"
        self.fearFactor = attributes["fearFactor"]
        self.sprite = "\033[0;34m" + "H" + "\033[0m"
        
    def isPrey(self):
        return True

