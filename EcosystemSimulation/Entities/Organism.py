
class Organism:
    def __init__(self, attributes):
        self.climateSensetivity = attributes["climateSensetivity"]
        self.reproductionRate = attributes["reproductionRate"]
        self.size = attributes["size"]
        self.moveDistance = attributes["moveDistance"]
        self.packMentality = attributes["packMentality"]
        self.maxEnergy = attributes["maxEnergy"]
        self.energyLoss = attributes["energyLoss"]

        self.attributes = attributes
        self.lifeLog = {
            "stepsSurvived": 0,
            "totalEnergy": 0.0,
            "actions": {}
        }

        # type
        self.type = attributes.get("type", None)

        self.location = (0,0)

        self.energy = self.maxEnergy
        self.alive = True
        

    def feed(self, energy_gain): 
        if hasattr(self, "lifeLog"):
            self.lifeLog["stepsSurvived"] = self.lifeLog.get("stepsSurvived", 0) + 1
            self.lifeLog["totalEnergy"] = self.lifeLog.get("totalEnergy", 0.0) + self.energy
            
        self.energy += energy_gain
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy

    # Simulate aging by reducing energy over time
    def age(self):
        self.energy -= self.energyLoss
        if self.energy <= 0:
            self.die()

    def die(self):
        self.alive = False

    def reproduce(self):
        pass

    def setEnergyLoss(self, energyLoss):
        self.energyLoss = energyLoss

    # used by genetic algorithm
    def getAttributeList(self):
        return self.attributes

# move toward a target location
def moveToward(self, target):
        tx, ty = target
        px, py = self.location

        dx = tx - px
        dy = ty - py

        # go long distance first
        if abs(dx) > abs(dy): 
            step_x = 1 if dx > 0 else -1
            step_y = 0
        else:
            step_x = 0
            step_y = 1 if dy > 0 else -1

        new_loc = (px + step_x, py + step_y)
        self.location = new_loc
        return new_loc
    
