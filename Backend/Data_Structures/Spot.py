from Backend.Data_Structures.Position import Position


class Spot(Position):
    # Spot의 status: explored or unexplored
    def __init__(self, col, row, explored):
        super().__init__(col, row, status=explored)

    def is_explored(self):
        return super().get_status()

    def set_explored(self):
        super().set_status(True)
        print(f"[Robot]: ✅Spot at {self.get_position()} was explored!")

    def __str__(self):
        return f"Spot({self.get_position()}, Explored: {self.is_explored()})"
