

class Terrain():    
    def __init__(self, gr, type):
        self.growthRate = gr
        self.type = type
        self.currentGrowth = 0

    def grow(self):
        if (self.currentGrowth > 0):
            self.currentGrowth -= 1
        
    def eaten(self):
        self.currentGrowth = self.growthRate

    def getSprite(self):
        return "\033[0;32m" + str(self.currentGrowth) + "\033[0m"