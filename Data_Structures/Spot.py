class Spot:
    def __init__(self, row, col, explored=False):
        self.position = (row, col)
        self.explored = explored

    def getPosition(self):
        return self.position

    def setExplored(self, explored):
        self.explored = explored

    def isExplored(self):
        return self.explored

    def __str__(self):
        return f"Spot({self.position}, Explored: {self.explored})"
