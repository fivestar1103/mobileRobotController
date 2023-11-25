# 이 클래스는 맵 초기화와 관련된 모든 것을 다룬다.
# - tkinter를 사용하여 GUI를 표시한다.
# - 사용자의 입력을 받아 Map 객체의 값을 수정한다.
import tkinter as tk
from tkinter import messagebox

from Backend.Controllers.RobotController import RobotController
from Backend.Data_Structures.ColorBlob import ColorBlob
from Backend.Data_Structures.Hazard import Hazard
from Backend.Data_Structures.Spot import Spot
from Backend.Map_Management_and_Path_Planning.Map import Map


class OperatorInterface:
    def __init__(self, mapInstance: Map, robotController: RobotController):
        self.on_close_callback = None
        self.mapInstance = mapInstance
        self.robotController = robotController
        self.master = tk.Tk()
        self.master.title("Map Initialization")

        self.hazards_display = None
        self.colorBlobs_display = None
        self.spots_display = None

        self.cols, self.rows = 0, 0
        self.robotCol, self.robotRow = -1, -1
        self.spots = []
        self.hazards = []
        self.color_blobs = []

        self.color1 = "#79D6F7"
        self.color2 = "#F7F079"
        self.color3 = "#A0374A"
        self.color4 = "#3C6575"

        self.master.config(bg=self.color1)
        self.master.withdraw()
        self.create_widgets()

    def create_widgets(self):
        first_row = tk.Frame(self.master)
        first_row.config(bg=self.color1)
        first_row.pack(fill=tk.X)

        self.create_input_section(first_row, "Set Map Size", self.set_map_size)
        self.create_input_section(first_row, "Set Robot Start", self.set_robot_start)

        second_row = tk.Frame(self.master)
        second_row.config(bg=self.color1)
        second_row.pack(fill=tk.X)

        self.spots_display = self.create_input_section(second_row, "Set Spots", self.set_spots, display=True)
        self.colorBlobs_display = self.create_input_section(second_row, "Set Color Blobs", self.set_color_blobs, display=True)
        self.hazards_display = self.create_input_section(second_row, "Set Hazards", self.set_hazards, display=True)

        delete_message = tk.Label(self.master, text="Double click each item to delete", bg=self.color1)
        delete_message.pack()

        start_button = tk.Button(self.master, text="Start", command=self.start_next_scene)
        start_button.pack(pady=5)

    def create_input_section(self, parent, label_text, command, display=False):
        frame = tk.Frame(parent)
        frame.config(bg=self.color2)
        frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        title_label = tk.Label(frame, text=label_text, font=("Arial", 16, "bold"), bg=self.color2)
        title_label.pack(pady=5)

        input_frame = tk.Frame(frame)
        input_frame.config(bg=self.color2)
        input_frame.pack(pady=2)

        col_label = tk.Label(input_frame, text="Column:", bg=self.color2)
        col_label.pack(side=tk.LEFT, padx=2)
        col_entry = tk.Entry(input_frame, width=2)
        col_entry.pack(side=tk.LEFT, padx=2)

        row_label = tk.Label(input_frame, text="Row:", bg=self.color2)
        row_label.pack(side=tk.LEFT, padx=2)
        row_entry = tk.Entry(input_frame, width=2)
        row_entry.pack(side=tk.LEFT, padx=2)

        button = tk.Button(frame, text="OK", command=lambda: command(col_entry.get(), row_entry.get(), frame), bg=self.color2)
        button.pack(pady=5)

        if display:
            list_frame = tk.Frame(frame, bg=self.color2)

            list_frame.pack()

            display_area = tk.Listbox(list_frame, height=6, width=7)
            display_area.pack(side=tk.LEFT, fill=tk.BOTH, pady=5)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=display_area.yview)
            scrollbar.pack(side=tk.LEFT, fill=tk.Y, pady=5)
            display_area.config(yscrollcommand=scrollbar.set)

            display_area.bind('<Double-1>', lambda event, da=display_area: self.delete_item(da))
            return display_area

    def set_map_size(self, cols, rows, frame):
        try:
            self.cols, self.rows = (int(cols), int(rows))
            if self.cols > 9 or self.rows > 9 or self.cols < 1 or self.rows < 1:
                messagebox.showerror("Invalid Input", "❌ Please enter valid integers for columns and rows.")
                self.cols, self.rows = 0, 0
            else:
                messagebox.showinfo("Success", "✅ Map size set successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Please enter valid integers for columns and rows.")

    def set_robot_start(self, col, row, frame):
        if self.is_valid_input(col, row):
            self.robotCol, self.robotRow = int(col), int(row)
            messagebox.showinfo("Success", "✅ Robot start position set successfully.")

    def set_spots(self, col, row, frame):
        if self.is_valid_input(col, row):
            col, row = int(col), int(row)
            self.spots.append((col, row))
            self.update_display(self.spots_display, self.spots)

    def set_color_blobs(self, col, row, frame):
        if self.is_valid_input(col, row):
            col, row = int(col), int(row)
            self.color_blobs.append((col, row))
            self.update_display(self.colorBlobs_display, self.color_blobs)

    def set_hazards(self, col, row, frame):
        if self.is_valid_input(col, row):
            col, row = int(col), int(row)
            self.hazards.append((col, row))
            self.update_display(self.hazards_display, self.hazards)

    def is_valid_input(self, col, row):
        try:
            col, row = int(col), int(row)
            position = (col, row)
            if 0 <= col < self.cols and 0 <= row < self.rows:
                if position in self.spots or position in self.hazards or position in self.color_blobs or position == (self.robotCol, self.robotRow):
                    messagebox.showerror("Invalid Input", "❌ Position already occupied.")
                    return False
                return True
            else:
                messagebox.showerror("Invalid Input", "❌ Input out of map range.")
                return False
        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Please enter valid integers.")
            return False

    def update_display(self, display_area, items):
        display_area.delete(0, tk.END)
        for index, item in enumerate(items, start=1):
            display_area.insert(tk.END, f"#{index}: {item}")

    def delete_item(self, display_area):
        try:
            selected_index = display_area.curselection()[0]
            display_area.delete(selected_index)
            if display_area == self.spots_display:
                self.spots.pop(selected_index)
            elif display_area == self.colorBlobs_display:
                self.color_blobs.pop(selected_index)
            elif display_area == self.hazards_display:
                self.hazards.pop(selected_index)
        except IndexError:
            pass  # No item selected or empty list

    def start_next_scene(self):
        if not (self.cols != 0 and self.rows != 0 and self.robotCol != -1 and self.robotRow != -1 and self.spots and self.color_blobs and self.hazards):
            messagebox.showerror("Invalid initialization", "❌ Please initialize the map with correct values.")
            return
        self.mapInstance.set_map_length(self.cols, self.rows)
        robot_coord = (self.robotCol, self.robotRow, 0)
        self.mapInstance.set_robot_coord(robot_coord)
        self.robotController.set_current_position(robot_coord)
        spotsFormatted, hazardsFormatted, colorBlobsFormatted = [], [], []
        for spot in self.spots:
            col, row = spot
            spotsFormatted.append(Spot(col, row, explored=False))
        for colorBlob in self.color_blobs:
            col, row = colorBlob
            colorBlobsFormatted.append(ColorBlob(col, row, hidden=True))
        for hazard in self.hazards:
            col, row = hazard
            hazardsFormatted.append(Hazard(col, row, hidden=False))
        self.mapInstance.set_spots(spotsFormatted)
        self.mapInstance.set_hazards(hazardsFormatted)
        self.mapInstance.set_color_blobs(colorBlobsFormatted)

        self.master.destroy()
        self.on_close_callback()

    def center_window(self):
        self.master.update_idletasks()
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

    def run(self, on_close):
        self.on_close_callback = on_close
        self.center_window()
        self.master.deiconify()
        self.master.mainloop()
