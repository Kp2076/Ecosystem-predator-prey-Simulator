import random
from Entities.Organism import Organism 
from Entities.Predator import Predator
from Entities.Prey import Prey

PREDATOR_MUTATION_RATE = 1 
PREY_MUTATION_RATE = 1 

def geneticAlgorithm(parent1, parent2):

    # parent attributes
    attribute1 = parent1.getAttributeList()
    attribute2 = parent2.getAttributeList()

    numAttributes = len(attribute1)

    # crossover point 
    randomNum = random.randint(0, numAttributes - 1)
    

    # get organism type
    # mutation
    if parent1.type == "predator":
        mutationRate = PREDATOR_MUTATION_RATE
    else:
        mutationRate = PREY_MUTATION_RATE

    # mix traits
    newAttributes = {}

    if random.random() < mutationRate:
        mutationIndex = random.randint(0, numAttributes - 1)

    for i, key in enumerate(attribute1.keys()):
        if i <= randomNum:
            newAttributes[key] = attribute1[key]
        else:
            newAttributes[key] = attribute2[key]

        if i == mutationIndex:
            newAttributes[key] = mutate(newAttributes[key], parent1.type)
    return newAttributes

def predGenetic(pred1, pred2):
    attributes = geneticAlgorithm(pred1, pred2)
    return Predator(attributes)

def preyGenetic(prey1, prey2):
    attributes = geneticAlgorithm(prey1, prey2)
    return Prey(attributes)


def mutate(attributeValue, organismType):
    if organismType == "predator":
        if isinstance(attributeValue, float):
            return attributeValue * random.uniform(0.95, 1.05)  # ±5%

        if isinstance(attributeValue, int):
            mutation = random.choice([-1, 0, 1])  # ±1
            return max(1, attributeValue + mutation)

        return attributeValue   
    
    elif organismType == "prey":
        if isinstance(attributeValue, float):
            return attributeValue * random.uniform(0.8, 1.2) # ±20%

        if isinstance(attributeValue, int):
            mutation = random.choice([-2, -1, 0, 1, 2]) # ±2
            return max(1, attributeValue + mutation)

        return attributeValue
    
    else:
        return attributeValue

