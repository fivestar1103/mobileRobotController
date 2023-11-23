import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import sounddevice as sd
import wavio
import os

from Backend.Data_Structures.ColorBlob import ColorBlob
from Backend.Data_Structures.Hazard import Hazard
from Backend.Map_Management_and_Path_Planning.Map import Map


class VoiceInputHandler:
    def __init__(self, parent, mapObject: Map, callback=None):
        self.add_button = None
        self.window = tk.Toplevel(parent)
        self.window.title("Record Voice")

        self.color1 = "#79D6F7"
        self.color2 = "#F7F079"
        self.window.config(bg=self.color2)

        self.points_listbox = None
        self.latest_input_label = None
        self.record_button = None
        self.mapObject = mapObject
        self.robot_position = mapObject.get_robot_coord()
        self.cols, self.rows = mapObject.get_map_length()
        self.callback = callback

        self.latest_input = [-1, -1, -1]
        self.recorded_points = []

        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        record_frame = tk.Frame(self.window, bg=self.color2)
        record_frame.pack(padx=10, pady=5)

        record_label = tk.Label(record_frame, text="Record the type, row, and column number in Korean", bg=self.color2)
        record_label.pack()

        record_button = tk.Button(record_frame, text="Record new point", command=self.record_audio)
        record_button.pack()
        self.record_button = record_button

        # display the input with 'Add' button
        latest_input_frame = tk.Frame(self.window, bg=self.color2)
        latest_input_frame.pack(padx=10, pady=5)

        latest_input_label = tk.Label(latest_input_frame, text="Type at (Column, Row)", bg=self.color2)
        latest_input_label.pack(side=tk.LEFT)
        self.latest_input_label = latest_input_label

        add_button = tk.Button(latest_input_frame, text="Add", command=self.add_latest_input)
        add_button.pack(side=tk.LEFT)
        self.add_button = add_button

        # Listbox and Scrollbar for recorded points
        listbox_frame = tk.Frame(self.window, bg=self.color2)
        listbox_frame.pack(padx=10, pady=10)

        points_listbox = tk.Listbox(listbox_frame, height=6, width=16, bg='lightgray')
        points_listbox.pack(side=tk.LEFT)
        points_listbox.bind('<Double-1>', self.delete_selected_point)

        scrollbar = tk.Scrollbar(listbox_frame, command=points_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        points_listbox.config(yscrollcommand=scrollbar.set)
        self.points_listbox = points_listbox

        # Label for instruction below the listbox
        delete_message = tk.Label(self.window, text="Double click each item to delete", bg=self.color2)
        delete_message.pack(pady=(0, 10))

        # Button to close the window
        close_button = tk.Button(self.window, text="Back to Map", command=self.close_window, bg=self.color2)
        close_button.pack(pady=5)

    def record_audio(self):
        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording

        # Change the button text to "Recording..."
        record_button = self.record_button
        record_button.config(text="Recording...", state='disabled')

        # Force GUI update before starting the recording
        self.window.update()

        # Start recording
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished

        # Save the recording as a WAV file
        file_path = os.path.join('audios', 'input.wav')
        wavio.write(file_path, recording, fs, sampwidth=2)

        # Use the speech_to_text method to process the recorded audio
        processed_input = self.speech_to_text(file_path)
        self.latest_input = processed_input

        # Update the label and reset the button text
        if self.latest_input == (-1, -1, -1):
            self.latest_input_label.config(text="Error occurred! Try again")
            self.add_button.config(state="disabled")
        else:
            type_text = "ColorBlob" if self.latest_input[0] == 0 else "Hazard"
            col, row = self.latest_input[1:]
            self.latest_input_label.config(text=f"{type_text} at ({col}, {row})")
            self.add_button.config(state="normal")

        record_button.config(text="Record new point", state='normal')

    # AI를 통한 STT 구현
    def speech_to_text(self, audio_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        try:
            str_value = recognizer.recognize_google(audio_data, language="ko-KR")
            print(str_value)
            number_mapping = {
                '공': 0, '영': 0, '0': 0,
                '하나': 1, '일': 1, '1': 1,
                '둘': 2, '이': 2, '2': 2,
                '셋': 3, '삼': 3, '3': 3,
                '넷': 4, '사': 4, '4': 4,
                '다섯': 5, '오': 5, '5': 5,
                '여섯': 6, '육': 6, '6': 6,
                '일곱': 7, '칠': 7, '7': 7,
                '여덟': 8, '팔': 8, '8': 8,
                '아홉': 9, '구': 9, '9': 9
            }
            # Split the string into words for easier matching
            words = str_value.split()
            result = [1 if '위' in words[0] else 0]  # Default to 0 unless '위험' (danger) is detected

            # Map the spoken words to their corresponding number
            for word in words[1:]:  # Assume the first word is type, so start from the second word
                number = number_mapping.get(word, None)
                if number is not None:
                    result.append(number)
                if len(result) == 3:
                    break  # Stop if we already have three items

            if len(result) != 3:
                raise ValueError("Could not parse all needed numbers from speech")
            return tuple(result)

        except (KeyError, ValueError, sr.UnknownValueError, sr.RequestError) as e:
            print(f"An error occurred while processing the speech: {e}")
            ret = (-1, -1, -1)  # Return a default tuple on error
            return ret

    def add_latest_input(self):
        if not self.is_valid_input():
            return
        self.recorded_points.append(self.latest_input)
        self.points_listbox.delete(0, tk.END)
        for index, point in enumerate(self.recorded_points, start=1):
            entry = f"#{index}: {'ColorBlob' if point[0] == 0 else 'Hazard'} at ({point[1]}, {point[2]})"
            self.points_listbox.insert(tk.END, entry)
        self.latest_input_label.config(text="Type at (Column, Row)")
        self.latest_input = [-1, -1, -1]

    # Check if the point is the robot's position, a duplicate, or out of bounds
    def is_valid_input(self):
        col, row = self.latest_input[1:]
        for existingCol, existingRow in self.mapObject.get_existing_positions():
            if col == existingCol and row == existingRow:
                messagebox.showerror("Invalid Input", "❌ Point already occupied!")
                return False
        if not (0 <= col < self.cols and 0 <= row < self.rows):
            messagebox.showerror("Invalid Input", "❌ Point is out of map bounds.")
            return False

        return True

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

        self.window.destroy()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
