from Backend.Data_Structures.Position import Position


class Hazard(Position):
    # Hazard의 status: hidden or revealed
    def __init__(self, col, row, hidden):
        super().__init__(col, row, status=hidden)

    def is_hidden(self):
        return super().get_status()

    def set_revealed(self):
        super().set_status(False)
        print(f"[Robot]: ⚠️Hazard at {self.get_position()} was revealed!")

    def __str__(self):
        return f"Hazard({self.get_position()}, Hidden: {self.is_hidden()})"
