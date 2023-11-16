import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image


class Display:
    def __init__(self, SIMControllerInstance, master=None):
        # Initialize axis padding and size variables
        self.axis_padding = 20
        self.cell_size = 50  # Adjust the size as needed
        self.SIMControllerInstance = SIMControllerInstance
        self.mapInstance = self.SIMControllerInstance.mapInstance
        self.master = master if master else tk.Tk()
        self.master.title("Mobile Robot Controller")
        self.isStop = True
        self.cols, self.rows = self.mapInstance.get_map_length()

        # Modify the size of the canvas to include space for the axes
        self.canvas_width = self.cols * self.cell_size + self.axis_padding
        self.canvas_height = self.rows * self.cell_size + self.axis_padding

        # Initialize the canvas with the new size
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.TOP)

        # Load robot images
        self.robot_images = {
            0: ImageTk.PhotoImage(Image.open("assets/'Robot_N.png").resize((self.cell_size, self.cell_size))),
            1: ImageTk.PhotoImage(Image.open("assets/'Robot_E.png").resize((self.cell_size, self.cell_size))),
            2: ImageTk.PhotoImage(Image.open("assets/'Robot_S.png").resize((self.cell_size, self.cell_size))),
            3: ImageTk.PhotoImage(Image.open("assets/'Robot_W.png").resize((self.cell_size, self.cell_size)))
        }

        self.ColorBlob_revealed_image = ImageTk.PhotoImage(
            Image.open("assets/ColorBlob_revealed.png").resize((self.cell_size, self.cell_size)))
        self.Hazard_revealed_image = ImageTk.PhotoImage(
            Image.open("assets/Hazard_revealed.png").resize((self.cell_size, self.cell_size)))
        self.Spot_unvisited_image = ImageTk.PhotoImage(
            Image.open("assets/Spot_unvisited.png").resize((self.cell_size, self.cell_size)))
        self.ColorBlob_hidden_image = ImageTk.PhotoImage(
            Image.open("assets/ColorBlob_hidden.png").resize((self.cell_size, self.cell_size)))
        self.Hazard_hidden_image = ImageTk.PhotoImage(
            Image.open("assets/Hazard_hidden.png").resize((self.cell_size, self.cell_size)))
        self.Spot_visited_image = ImageTk.PhotoImage(
            Image.open("assets/Spot_visited.png").resize((self.cell_size, self.cell_size)))

        # Create button frame and buttons
        self.create_buttons()

    def create_buttons(self):
        # Initialize a vertical frame for the buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.BOTTOM)

        # Place buttons inside the frame
        self.go_button = tk.Button(self.button_frame, text="Go", command=self.on_go)
        self.go_button.pack(side=tk.TOP, pady=5)  # Use pady for vertical padding

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.on_stop)
        self.stop_button.pack(side=tk.TOP, pady=5)

    def on_go(self):
        # Continue with the next move
        self.isStop = False
        self.SIMControllerInstance.send_movement_command()

    def on_stop(self):
        # Replan the path and continue
        self.isStop = True

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
        self.draw_axes()

        # Draw all blank points as white blocks
        for col in range(self.cols):
            for row in range(self.rows):
                self.draw_element((col, row), "white")

        # Draw the planned path if it exists
        self.draw_path(self.SIMControllerInstance.get_path())

        # Draw images for hazards, color blobs, and spots
        for hazard in self.mapInstance.get_hazards():
            self.draw_image(hazard.get_position(), self.Hazard_revealed_image if not hazard.is_hidden() else self.Hazard_hidden_image)

        for colorBlob in self.mapInstance.get_color_blobs():
            self.draw_image(colorBlob.get_position(), self.ColorBlob_revealed_image if not colorBlob.is_hidden() else self.ColorBlob_hidden_image)

        for spot in self.mapInstance.get_spots():
            self.draw_image(spot.get_position(), self.Spot_visited_image if spot.is_explored() else self.Spot_unvisited_image)

        # Draw the robot
        self.draw_robot()

        self.master.update_idletasks()

    def draw_robot(self):
        robotRow, robotCol, robotDirection = self.mapInstance.get_robot_coord()
        x1, y1 = robotRow, robotCol
        y1 = self.mapInstance.get_map_length()[1] - y1 - 1
        x1 *= self.cell_size
        y1 *= self.cell_size
        self.canvas.create_image(x1, y1, anchor="nw", image=self.robot_images[robotDirection])

    def alert(self, message):
        messagebox.showinfo("📝 Replanning path...", message)

    def run(self):
        # Perform the initial update and start the main loop
        self.center_window()
        self.update_display()

        self.master.after(500, self.SIMControllerInstance.send_movement_command)
        self.master.mainloop()

    def draw_axes(self):
        # Draw column numbers (horizontal axis)
        for i in range(self.cols):
            self.canvas.create_text(i * self.cell_size + self.cell_size / 2,
                                    self.canvas_height - self.axis_padding / 2,
                                    text=str(i), font=("Arial", 10))

        # Draw row numbers (vertical axis)
        for i in range(self.rows):
            self.canvas.create_text(self.canvas_width - self.axis_padding / 2,
                                    i * self.cell_size + self.cell_size / 2,
                                    text=str(self.rows - 1 - i), font=("Arial", 10))  # Note the reverse order for y-axis

    def draw_path(self, path):
        if path:
            # Convert path points to canvas coordinates
            pathWithSelfCoord = reversed(path + [self.mapInstance.get_robot_coord()[:2]])
            canvas_path = [(col * self.cell_size + self.cell_size // 2,
                            (self.rows - row - 1) * self.cell_size + self.cell_size // 2) for col, row in pathWithSelfCoord]

            # Draw lines between each point in the path
            for i in range(len(canvas_path) - 1):
                self.canvas.create_line(canvas_path[i], canvas_path[i + 1], fill="lightblue", width=2, dash=(4,2), arrow=tk.LAST)

            # Update the canvas to reflect the new drawing

    def draw_image(self, position, image):
        col, row = position
        x = col * self.cell_size
        y = (self.rows - row - 1) * self.cell_size  # Adjust for y-axis inversion
        self.canvas.create_image(x, y, anchor="nw", image=image)

    def center_window(self):
        # Get the screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the position for the window to be centered
        x = (screen_width // 2) - ((self.cols * self.cell_size) // 2)
        y = (screen_height // 2) - ((self.rows * self.cell_size) // 2)

        # Set the geometry of the main window, format: widthxheight+x_offset+y_offset
        self.master.geometry(f"+{x}+{y}")
