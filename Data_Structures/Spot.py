from Data_Structures.Position import Position


class Spot(Position):
    # Spot의 status: explored or unexplored
    def __init__(self, col, row, explored):
        super().__init__(col, row, status=explored)

    def isExplored(self):
        return super().getStatus()

    def setExplored(self):
        super().setStatus(True)
        print(f"[Robot]: ✅Spot at {self.getPosition()} was explored!")

    def __str__(self):
        return f"Spot({self.getPosition()}, Explored: {self.isExplored()})"
