from Entities.Organism import Organism


class Predator(Organism):
    def __init__(self, attributes):
        super().__init__(attributes)
        self.type = "predator"
        self.agressiveness = attributes["agressiveness"]
        self.sprite =  "\033[0;31m" + "C" + "\033[0m"

    def isPrey(self):
        return False