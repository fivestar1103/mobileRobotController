# 이 클래스는 음성 인식과 관련된 모든 것을 다룬다.
# - 음성 인식 창(GUI)을 표시하고 음성 인식을 수행한다.
# - GUI는 tkinter 모듈을 사용한다.
# - 음성 인식은 Speech Recognition 모듈의 구글 STT API를 사용한다.
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import sounddevice as sd
import wavio
import os
from Utilities.UI_utilities import center_window, COLOR2

from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Map_Management_and_Display.Map import Map


class VoiceInputHandler:
    def __init__(self, parentWindow, mapInstance: Map, callback=None):
        self.__mapObject = mapInstance
        self.__callback = callback

        self.__points_listbox = None
        self.__latest_input_label = None
        self.__record_button = None
        self.__add_button = None

        self.__latest_input = [-1, -1, -1]
        self.__recorded_points = []

        self.__window = tk.Toplevel(parentWindow)
        self.__window.title("Record Voice")
        self.__window.config(bg=COLOR2)
        self.__window.withdraw()

    # 마이크 버튼을 누르면 실행
    def run(self):
        # Create a new Toplevel window each time the method is called.
        self.__window = tk.Toplevel()
        self.__window.title("Record Voice")
        self.__window.config(bg=COLOR2)

        self.setup_ui()
        center_window(self.__window)
        self.__window.deiconify()

    # GUI 화면 설정
    def setup_ui(self):
        record_frame = tk.Frame(self.__window, bg=COLOR2)
        record_frame.pack(padx=10, pady=5)

        record_label = tk.Label(record_frame, text="Record the type, row, and column number in Korean", bg=COLOR2)
        record_label.pack()

        record_button = tk.Button(record_frame, text="Record new point", command=self.record_audio)
        record_button.pack()
        self.__record_button = record_button

        # 녹음된 값을 모니터링 하기 위해 텍스트로 표시
        latest_input_frame = tk.Frame(self.__window, bg=COLOR2)
        latest_input_frame.pack(padx=10, pady=5)

        latest_input_label = tk.Label(latest_input_frame, text="Type at (Column, Row)", bg=COLOR2)
        latest_input_label.pack(side=tk.LEFT)
        self.__latest_input_label = latest_input_label

        # Add 버튼을 누르면 녹음된 지점이 지도에 추가된다
        add_button = tk.Button(latest_input_frame, text="Add", command=self.add_latest_input)
        add_button.pack(side=tk.LEFT)
        self.__add_button = add_button

        # 지도에 추가할 녹음된 지점들을 표시한다
        listbox_frame = tk.Frame(self.__window, bg=COLOR2)
        listbox_frame.pack(padx=10, pady=10)

        # 더블클릭하면 삭제할 수 있다
        points_listbox = tk.Listbox(listbox_frame, height=6, width=16, bg='lightgray')
        points_listbox.pack(side=tk.LEFT)
        points_listbox.bind('<Double-1>', self.delete_selected_point)

        scrollbar = tk.Scrollbar(listbox_frame, command=points_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        points_listbox.config(yscrollcommand=scrollbar.set)
        self.__points_listbox = points_listbox

        delete_message = tk.Label(self.__window, text="Double click each item to delete", bg=COLOR2)
        delete_message.pack(pady=(0, 10))

        # Back to Map 버튼을 누르면 지도 화면으로 돌아간다
        close_button = tk.Button(self.__window, text="Back to Map", command=self.close_window, bg=COLOR2)
        close_button.pack(pady=5)

    # 음성을 녹음하여 STT를 적용한다
    def record_audio(self):
        fs = 44100  # sample rate
        seconds = 5  # 5초간 녹음 수행

        # 버튼 텍스트를 Recording...으로 바꿔준다
        record_button = self.__record_button
        record_button.config(text="Recording...", state='disabled')
        self.__window.update()

        # 녹음 시작
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()

        # 녹음 파일을 audios 폴더에 WAV 파일로 저장
        file_path = os.path.join('audios', 'input.wav')
        wavio.write(file_path, recording, fs, sampwidth=2)

        # STT 적용하여 저장하고 모니터링 텍스트 변경
        self.__latest_input = self.speech_to_text(file_path)
        if -1 in self.__latest_input:  # 기본값이 반환된 경우 에러
            self.__latest_input_label.config(text="Error occurred! Try again")
            self.__add_button.config(state="disabled")  # 에러가 발생한 경우는 추가되지 못하게 막는다
        else:
            type_text = "ColorBlob" if self.__latest_input[0] == 0 else "Hazard"
            print(self.__latest_input)
            col, row = self.__latest_input[1:]
            self.__latest_input_label.config(text=f"{type_text} at ({col}, {row})")
            self.__add_button.config(state="normal")

        record_button.config(text="Record new point", state='normal')  # 녹음 버튼 텍스트 원래로 돌려놓기

    # AI를 통한 STT 구현
    def speech_to_text(self, audio_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)

        ret = [-1, -1, -1]  # 기본값
        try:
            str_value = recognizer.recognize_google(audio_data, language="ko-KR")  # 구글 API로 한국어 인식
            print(str_value)
            number_mapping = {  # 세 가지 형식으로 인식되므로 각 형식을 지정
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

            # 3 단어로 나눠지지 않은 경우 에러 발생
            pointType, pointCol, pointRow = str_value.split()

            pointType = 1 if '위' in pointType else 0  # 기본적으로 중요지점이고 '위'가 포함된 경우 위험지점이다
            # 2, 3번째 단어를 숫자(행/열 번호)로 변환
            pointCol, pointRow = number_mapping.get(pointCol, -1), number_mapping.get(pointRow, -1)

            ret = [pointType, pointCol, pointRow]
            if -1 in ret:
                ret = [-1, -1, -1]
                raise ValueError("Could not parse all needed numbers from speech")

            return ret

        except (KeyError, ValueError, sr.UnknownValueError, sr.RequestError) as e:
            print(f"An error occurred while processing the speech: {e}")
            return ret

    # add 버튼을 누르면 녹음된 지점이 추가된다
    def add_latest_input(self):
        if not self.is_valid_input():  # 올바른 값만 추가
            return
        self.__recorded_points.append(self.__latest_input)
        self.__points_listbox.delete(0, tk.END)
        for index, point in enumerate(self.__recorded_points, start=1):
            entry = f"#{index}: {'ColorBlob' if point[0] == 0 else 'Hazard'} at ({point[1]}, {point[2]})"
            self.__points_listbox.insert(tk.END, entry)
        self.__latest_input_label.config(text="Type at (Column, Row)")
        self.__latest_input = [-1, -1, -1]

    # 녹음된 값이 올바른 값인지 확인
    def is_valid_input(self):
        col, row = self.__latest_input[1:]

        # 중복된 지점인지 확인
        if (col, row) in [existingPoint for existingPoint in self.__mapObject.get_existing_positions()]:
            messagebox.showerror("Invalid Input", "❌ Point already occupied!")
            return False

        # 이미 녹음된 지점인지 확인
        if [col, row] in [recordedPoint[1:] for recordedPoint in self.__recorded_points]:
            messagebox.showerror("Invalid Input", "❌ Point already recorded!")
            return False

        # 맵 밖을 벗어나는 지점인지 확인
        cols, rows = self.__mapObject.get_map_length()
        if not (0 <= col < cols and 0 <= row < rows):
            messagebox.showerror("Invalid Input", "❌ Point is out of map bounds.")
            return False

        return True

    # 아이템을 더블클릭하여 삭제
    def delete_selected_point(self, event):
        try:
            selected_index = self.__points_listbox.curselection()[0]
            self.__points_listbox.delete(selected_index)
            del self.__recorded_points[selected_index]
        except IndexError:
            pass

    # Back to Map 버튼을 누르면 창을 닫고 맵 화면으로 돌아간다
    def close_window(self):
        newPoints = []  # 새로 녹음된 지점들을 추가
        for point in self.__recorded_points:
            pointType, pointCol, pointRow = point
            if pointType == 0:
                newPoints.append(ColorBlob(pointCol, pointRow, hidden=True))
            else:
                newPoints.append(Hazard(pointCol, pointRow, hidden=True))
        self.__mapObject.add_new_points(newPoints)
        self.__recorded_points = []

        self.__callback()
        self.__window.withdraw()

    # getter methods
    def get_add_button(self):
        return self.__add_button

    def get_window(self):
        return self.__window

    def get_map_object(self):
        return self.__mapObject

    def get_callback(self):
        return self.__callback

    def get_points_listbox(self):
        return self.__points_listbox

    def get_latest_input_label(self):
        return self.__latest_input_label

    def get_record_button(self):
        return self.__record_button

    def get_latest_input(self):
        return self.__latest_input

    def get_recorded_points(self):
        return self.__recorded_points

    # setter methods
    def set_latest_input(self, value):
        if not isinstance(value, list) or not all(isinstance(n, int) for n in value):
            raise ValueError("Latest input must be a list of integers.")
        self.__latest_input = value

    def set_recorded_points(self, points):
        if not all(isinstance(point, list) and len(point) == 3 for point in points):
            raise ValueError("Recorded points must be a list of [type, col, row].")
        self.__recorded_points = points

    def add_recorded_point(self, point):
        if not isinstance(point, list) or len(point) != 3:
            raise ValueError("Point must be a list of [type, col, row].")
        self.__recorded_points.append(point)

    def delete_recorded_point(self, index):
        if not (0 <= index < len(self.__recorded_points)):
            raise IndexError("Index out of range for recorded points.")
        del self.__recorded_points[index]
