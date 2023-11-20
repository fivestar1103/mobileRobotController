import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import wavio
import os
import random

from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Path_Planning_and_Map_Management.Map import Map


class VoiceInputHandler(tk.Toplevel):
    def __init__(self, parent, mapObject: Map, callback=None):
        super().__init__(parent)
        self.mapObject = mapObject
        self.robot_position = mapObject.get_robot_coord()
        self.cols, self.rows = mapObject.get_map_length()
        self.existingHazards = mapObject.get_hazards()
        self.existingColorBlobs = mapObject.get_color_blobs()
        self.existingSpots = mapObject.get_spots()
        self.existingPoints = [hazard.get_position() for hazard in self.existingHazards] + [colorBlob.get_position() for colorBlob in self.existingColorBlobs] + [spot.get_position() for spot in self.existingSpots]
        self.callback = callback

        self.close_button = None
        self.points_listbox = None
        self.add_button = None
        self.latest_input_label = None
        self.title("Voice Input")

        self.color1 = "#79D6F7"
        self.color2 = "#F7F079"

        self.type_button = None
        self.column_button = None
        self.row_button = None

        self.latest_input = {'type': '', 'column': '', 'row': ''}
        self.recorded_points = []

        self.config(bg=self.color2)

        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        # Frames for Type, Column, Row inputs
        self.create_input_frame("Type (0 for ColorBlob, 1 for Hazard)", "type")
        self.create_input_frame("Column Number", "column")
        self.create_input_frame("Row Number", "row")

        # Latest input display with 'Add' button
        latest_input_frame = tk.Frame(self, bg=self.color2)
        latest_input_frame.pack(padx=10, pady=5)

        self.latest_input_label = tk.Label(latest_input_frame, text="Type at (Column, Row)", bg=self.color2)
        self.latest_input_label.pack(side=tk.LEFT)

        self.add_button = tk.Button(latest_input_frame, text="Add", command=self.add_latest_input)
        self.add_button.pack(side=tk.LEFT)

        # Listbox and Scrollbar for recorded points
        listbox_frame = tk.Frame(self, bg=self.color2)
        listbox_frame.pack(padx=10, pady=10)

        self.points_listbox = tk.Listbox(listbox_frame, height=6, width=16, bg='lightgray')
        self.points_listbox.pack(side=tk.LEFT)
        self.points_listbox.bind('<Double-1>', self.delete_selected_point)

        scrollbar = tk.Scrollbar(listbox_frame, command=self.points_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.points_listbox.config(yscrollcommand=scrollbar.set)

        # Label for instruction below the listbox
        delete_message = tk.Label(self, text="Double click each item to delete", bg=self.color2)
        delete_message.pack(pady=(0, 10))

        # Button to close the window
        self.close_button = tk.Button(self, text="Back to Map", command=self.close_window, bg=self.color2)
        self.close_button.pack(pady=5)

    def create_input_frame(self, label_text, field_name):
        frame = tk.Frame(self, bg=self.color2)
        frame.pack(padx=10, pady=5)

        label = tk.Label(frame, text=label_text, bg=self.color2)
        label.pack()

        button = tk.Button(frame, text=f"Record {field_name.capitalize()}", command=lambda: self.record_audio(field_name))
        setattr(self, f"{field_name}_button", button)
        button.pack()

    def record_audio(self, field):
        fs = 44100  # Sample rate
        seconds = 2  # Duration of recording

        # Change the button text to "Recording..."
        record_button = getattr(self, f"{field}_button")
        original_text = record_button.cget("text")
        record_button.config(text="Recording...", state='disabled')

        # Force GUI update before starting the recording
        self.update()

        # Start recording
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished

        # Save the recording as a WAV file
        file_path = os.path.join('audios', f'{field}_input.wav')
        wavio.write(file_path, recording, fs, sampwidth=2)

        # Use the speech_to_text method to process the recorded audio
        processed_input = self.speech_to_text(file_path)
        self.latest_input[field] = processed_input

        # Update the label and reset the button text
        self.update_latest_input_label()
        record_button.config(text=original_text, state='normal')

    def speech_to_text(self, audio_file_path):
        # audio_file_path에 존재하는 음성을 읽어서 stt 적용하여 파싱된 정수 세개 반환
        
        

    def simulate_recording(self, field):
        self.latest_input[field] = 0  # Placeholder value for demonstration
        self.update_latest_input_label()
        getattr(self, f"{field}_button").config(text=f"Record {field.capitalize()}", state='normal')

    def update_latest_input_label(self):
        type_text = "ColorBlob" if self.latest_input['type'] == 0 else "Hazard"
        self.latest_input_label.config(
            text=f"{type_text} at ({self.latest_input['column']}, {self.latest_input['row']})"
        )

    def add_latest_input(self):
        if self.is_valid_input():
            self.recorded_points.append((self.latest_input['type'], self.latest_input['column'], self.latest_input['row']))
            self.update_points_listbox()
            self.latest_input_label.config(text="Type at (Column, Row)")
            self.latest_input = {'type': 'Type', 'column': '', 'row': ''}

    def is_valid_input(self):
        # Check if any field is empty
        if '' in self.latest_input.values():
            messagebox.showerror("Invalid Input", "Please record all fields.")
            return False

        # Convert column and row to integers and handle invalid inputs
        try:
            col, row = int(self.latest_input['column']), int(self.latest_input['row'])
        except ValueError:
            messagebox.showerror("Invalid Input", "Column and row must be integers.")
            return False

        # Check if the point is the robot's position, a duplicate, or out of bounds
        if (col, row) == self.robot_position:
            messagebox.showerror("Invalid Input", "Point is the robot's current position.")
            return False
        if (col, row) in self.existingPoints or (col, row) in [(int(p[1]), int(p[2])) for p in self.recorded_points]:
            messagebox.showerror("Invalid Input", "Duplicate point.")
            return False
        if not (0 <= col < self.cols and 0 <= row < self.rows):
            messagebox.showerror("Invalid Input", "Point is out of map bounds.")
            return False

        return True

    def update_points_listbox(self):
        self.points_listbox.delete(0, tk.END)
        for index, point in enumerate(self.recorded_points, start=1):
            entry = f"#{index}: {'ColorBlob' if point[0] == 0 else 'Hazard'} at ({point[1]}, {point[2]})"
            self.points_listbox.insert(tk.END, entry)

    def delete_selected_point(self, event):
        try:
            selected_index = self.points_listbox.curselection()[0]
            self.points_listbox.delete(selected_index)
            del self.recorded_points[selected_index]
        except IndexError:
            pass

    def close_window(self):
        newPoints = []
        for point in self.recorded_points:
            pointType, pointCol, pointRow = point
            if pointType == 0:
                newPoints.append(ColorBlob(pointCol, pointRow, hidden=True))
            else:
                newPoints.append(Hazard(pointCol, pointRow, hidden=True))
        self.mapObject.add_new_points(newPoints)
        if self.callback:
            self.callback()

        self.destroy()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

