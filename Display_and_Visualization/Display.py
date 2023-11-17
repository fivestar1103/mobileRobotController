import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image


class Display:
    def __init__(self, SIMControllerInstance, master=None):
        self.log_counter = 0
        self.on_mic = None
        self.mic_button = None

        self.Spot_visited_image = None
        self.Hazard_hidden_image = None
        self.ColorBlob_hidden_image = None
        self.Spot_unvisited_image = None
        self.Hazard_revealed_image = None
        self.ColorBlob_revealed_image = None

        self.robot_images = None

        self.mic_button_enabled_image = None
        self.mic_button_disabled_image = None
        self.go_button_enabled_image = None
        self.go_button_disabled_image = None
        self.stop_button_enabled_image = None
        self.stop_button_disabled_image = None
        self.stop_button = None
        self.go_button = None

        self.axis_padding = 10
        self.cell_size = 50

        self.color1 = "#79D6F7"
        self.color2 = "#F7F079"
        self.color3 = "#A0374A"
        self.color4 = "#3C6575"

        self.SIMControllerInstance = SIMControllerInstance
        self.mapInstance = self.SIMControllerInstance.mapInstance
        self.master = master if master else tk.Tk()
        self.master.config(bg=self.color1)
        self.master.title("Mobile Robot Controller")
        self.isStop = True
        self.cols, self.rows = self.mapInstance.get_map_length()

        # Calculate canvas size with padding
        self.canvas_width = self.cols * self.cell_size + 2 * self.axis_padding
        self.canvas_height = self.rows * self.cell_size + 2 * self.axis_padding

        # Create frames
        self.canvas_frame = tk.Frame(self.master, relief="groove", padx=10, pady=10, bg=self.color2)
        self.log_frame = tk.Frame(self.master, relief="groove", padx=10, pady=10, bg=self.color2)
        self.button_frame = tk.Frame(self.master, relief="groove", bg=self.color2)

        # Create titles
        self.log_title = tk.Label(self.log_frame, text="Event Log", font=("Arial", 30), bg=self.color2)
        self.log_title.pack(side=tk.TOP, pady=10)
        self.canvas_title = tk.Label(self.canvas_frame, text="Map", font=("Arial", 30), bg=self.color2)
        self.canvas_title.pack(side=tk.TOP, pady=10)

        # Configure the grid layout manager
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        # Place frames using the grid manager
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(10, 5))
        self.button_frame.grid(row=1, column=1, sticky="ew", padx=(5, 5), pady=(10, 5))
        self.log_frame.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=(10, 5))

        # Initialize the canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, bg='white',
                                highlightbackground="black")
        self.canvas.pack(side='top', fill='both', expand=True)

        # Initialize the log text widget with a scrollbar
        self.log_scroll = tk.Scrollbar(self.log_frame)
        self.log_text = tk.Text(self.log_frame,
                                yscrollcommand=self.log_scroll.set,
                                state='disabled',
                                bg='lightgray',
                                width=37,
                                highlightbackground="black",
                                )
        self.log_scroll.config(command=self.log_text.yview)
        self.log_scroll.pack(side='right', fill='y')
        self.log_text.pack(side='left', fill='both', expand=False)

        # Load images
        self.load_images()

        # Create buttons and pack them in the button_frame using the pack manager
        self.create_buttons()

        # Draw axes and update the display
        self.draw_axes()
        self.update_display()

        # Set the window to open in the center of the screen
        self.center_window()

    def load_images(self):
        # Load robot images
        self.robot_images = {
            0: ImageTk.PhotoImage(Image.open("assets/Robot_N.png").resize((self.cell_size, self.cell_size))),
            1: ImageTk.PhotoImage(Image.open("assets/Robot_E.png").resize((self.cell_size, self.cell_size))),
            2: ImageTk.PhotoImage(Image.open("assets/Robot_S.png").resize((self.cell_size, self.cell_size))),
            3: ImageTk.PhotoImage(Image.open("assets/Robot_W.png").resize((self.cell_size, self.cell_size)))
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

        self.go_button_enabled_image = ImageTk.PhotoImage(
            Image.open("assets/go_button_enabled.png").resize((self.cell_size, self.cell_size)))
        self.go_button_disabled_image = ImageTk.PhotoImage(
            Image.open("assets/go_button_disabled.png").resize((self.cell_size, self.cell_size)))
        self.stop_button_enabled_image = ImageTk.PhotoImage(
            Image.open("assets/stop_button_enabled.png").resize((self.cell_size, self.cell_size)))
        self.stop_button_disabled_image = ImageTk.PhotoImage(
            Image.open("assets/stop_button_disabled.png").resize((self.cell_size, self.cell_size)))
        self.mic_button_enabled_image = ImageTk.PhotoImage(
            Image.open("assets/mic_button_enabled.png").resize((self.cell_size, self.cell_size)))
        self.mic_button_disabled_image = ImageTk.PhotoImage(
            Image.open("assets/mic_button_disabled.png").resize((self.cell_size, self.cell_size)))

    def log_message(self, message):
        # Alternate colors for each log entry
        color = self.color3 if self.log_counter % 2 == 0 else self.color4
        self.log_counter += 1

        # Enable the text widget, insert the message, then disable it
        self.log_text.config(state='normal')
        # Insert a new frame for each log entry to control the background color at the beginning of the text widget
        log_frame = tk.Frame(self.log_text, bg=color, highlightthickness=0)  # Remove any highlight border
        log_label = tk.Label(log_frame, text=message, bg=color, fg="white", anchor='w', justify=tk.LEFT, width=28)
        log_label.pack(side=tk.TOP, fill=tk.X)  # Pack with fill=X to fill frame horizontally
        self.log_text.window_create('1.0', window=log_frame)  # Insert at the beginning
        self.log_text.insert('1.0', '\n')  # Add space after the log entry
        self.log_text.config(state='disabled')

    def create_buttons(self):
        self.go_button = tk.Button(self.button_frame, image=self.go_button_disabled_image, command=self.on_go,
                                   borderwidth=0, highlightthickness=0, bg=self.color3)
        self.go_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        self.stop_button = tk.Button(self.button_frame, image=self.stop_button_enabled_image, command=self.on_stop)
        self.stop_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        # Initialize the microphone button in a disabled state
        self.mic_button = tk.Button(self.button_frame, image=self.mic_button_disabled_image, command=self.on_mic,
                                    state=tk.DISABLED)
        self.mic_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

    def on_go(self):
        self.isStop = False
        # Change the button image to indicate it's active
        self.go_button.config(image=self.go_button_enabled_image)
        self.stop_button.config(image=self.stop_button_disabled_image)
        self.mic_button.config(image=self.mic_button_disabled_image, state=tk.DISABLED)
        self.SIMControllerInstance.send_movement_command()

    def on_stop(self):
        self.isStop = True
        # Change the button image to indicate it's active
        self.stop_button.config(image=self.stop_button_enabled_image)
        self.go_button.config(image=self.go_button_disabled_image)
        self.mic_button.config(image=self.mic_button_enabled_image, state=tk.NORMAL)

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
        # Center the window before the main loop starts
        self.center_window()
        self.master.after(500, self.SIMControllerInstance.send_movement_command)
        self.master.mainloop()

    def draw_axes(self):
        # Draw column numbers (horizontal axis)
        for i in range(self.cols):
            self.canvas.create_text(i * self.cell_size + self.cell_size / 2,
                                    self.canvas_height - self.axis_padding / 2,
                                    text=str(i), font=("Arial", 12, "bold"))

        # Draw row numbers (vertical axis)
        for i in range(self.rows):
            self.canvas.create_text(self.canvas_width - self.axis_padding / 2,
                                    i * self.cell_size + self.cell_size / 2,
                                    text=str(self.rows - 1 - i), font=("Arial", 12, "bold"))  # Note the reverse order for y-axis
    def draw_path(self, path):
        if path:
            # Convert path points to canvas coordinates
            pathWithSelfCoord = reversed(path + [self.mapInstance.get_robot_coord()[:2]])
            canvas_path = [(col * self.cell_size + self.cell_size // 2,
                            (self.rows - row - 1) * self.cell_size + self.cell_size // 2) for col, row in pathWithSelfCoord]

            # Draw lines between each point in the path
            for i in range(len(canvas_path) - 1):
                self.canvas.create_line(canvas_path[i], canvas_path[i + 1], fill=self.color3, width=2, dash=(4,2), arrow=tk.LAST)

            # Update the canvas to reflect the new drawing

    def draw_image(self, position, image):
        col, row = position
        x = col * self.cell_size
        y = (self.rows - row - 1) * self.cell_size  # Adjust for y-axis inversion
        self.canvas.create_image(x, y, anchor="nw", image=image)

    def center_window(self):
        # Calculate the correct center position
        self.master.update_idletasks()  # Update "requested size" from geometry manager
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.master.geometry("+{}+{}".format(position_right, position_down))

