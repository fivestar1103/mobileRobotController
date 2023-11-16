import tkinter as tk

from PIL import ImageTk, Image


class Display:
    def __init__(self, SIMControllerInstance, master=None):
        self.SIMControllerInstance = SIMControllerInstance
        self.mapInstance = self.SIMControllerInstance.mapInstance
        self.master = master if master else tk.Tk()
        self.master.title("Mobile Robot Controller")

        self.cell_size = 50  # Adjust the size as needed
        cols, rows = self.mapInstance.get_map_length()
        self.canvas = tk.Canvas(self.master, width=cols*self.cell_size, height=rows*self.cell_size)
        self.canvas.pack()

        # Load the robot image
        # Load the robot images
        self.robot_images = {
            0: ImageTk.PhotoImage(Image.open("assets/'Robot_N.png").resize((self.cell_size, self.cell_size))),
            1: ImageTk.PhotoImage(Image.open("assets/'Robot_E.png").resize((self.cell_size, self.cell_size))),
            2: ImageTk.PhotoImage(Image.open("assets/'Robot_S.png").resize((self.cell_size, self.cell_size))),
            3: ImageTk.PhotoImage(Image.open("assets/'Robot_W.png").resize((self.cell_size, self.cell_size)))
        }

    def draw_element(self, position, color, alpha='#'):
        col, row = position
        x1 = col * self.cell_size
        y1 = (self.mapInstance.get_map_length()[1] - row - 1) * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        if alpha != '#':
            color = color + alpha
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def update_display(self):
        self.canvas.delete("all")
        # Draw all blank points as white blocks
        cols, rows = self.mapInstance.get_map_length()
        for col in range(cols):
            for row in range(rows):
                self.draw_element((col, row), "white")
        for hazard in self.mapInstance.get_hazards():
            color = "#FF0000" if not hazard.is_hidden() else "#FFC0CB"  # Red or light pink for hidden hazards
            self.draw_element(hazard.get_position(), color)
        for colorBlob in self.mapInstance.get_color_blobs():
            color = "#FFFF00" if not colorBlob.is_hidden() else "#FFFFE0"  # Yellow or light yellow for hidden color blobs
            self.draw_element(colorBlob.get_position(), color)
        for spot in self.mapInstance.get_spots():
            color = "#008000" if spot.is_explored() else "#90EE90"  # Green or light green for unexplored spots
            self.draw_element(spot.get_position(), color)
        self.draw_robot()  # Ensure this method exists and is properly defined

    def draw_robot(self):
        position, direction = self.mapInstance.get_robot_coord()[:2], self.mapInstance.get_robot_coord()[2]
        x1, y1 = position
        y1 = self.mapInstance.get_map_length()[1] - y1 - 1  # Invert row index for display
        x1 *= self.cell_size
        y1 *= self.cell_size
        self.canvas.create_image(x1, y1, anchor="nw", image=self.robot_images[direction])

    def run(self):
        self.update_display()  # Initial display update
        self.master.after(100, self.SIMControllerInstance.start_movement)
        self.master.mainloop()
