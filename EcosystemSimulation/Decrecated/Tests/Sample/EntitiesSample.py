
CARDINAL_DIRS = [(1,0), (0,1), (-1,0), (0,-1)]

class Animal:
    def __init__(self, x=0, y=0, width=1, height=1, name="animal", role=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.role = role  

class PredatorTest(Animal):
    def __init__(self, width, height, name="predator"):
        super().__init__(0, 0, width, height, name, role="predator")

class PreyTest(Animal):
    def __init__(self, width, height, name="prey"):
        super().__init__(0, 0, width, height, name, role="prey")

def create_animal_test(name):
    # n = name.lower()
    n = name
    if n == "lion":
        return PredatorTest(width=1, height=1, name="lion")
    if n == "wolf":
        return PredatorTest(width=1, height=1, name="wolf")
    if n == "deer":
        return PreyTest(width=1, height=1, name="deer")
    if n == "rabbit":
        return PreyTest(width=1, height=1, name="rabbit")
    return PreyTest(width=1, height=1, name=n)
