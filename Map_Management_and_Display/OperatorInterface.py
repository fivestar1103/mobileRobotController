# 이 클래스는 맵 초기화와 관련된 모든 것을 다룬다.
# - tkinter를 사용하여 GUI를 표시한다.
# - 사용자의 입력을 받아 Map 객체의 값을 수정한다.
import tkinter as tk
from tkinter import messagebox
from Utilities.UI_utilities import center_window, COLOR1, COLOR2

from Controllers.RobotController import RobotController
from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Data_Structures.Spot import Spot
from Map_Management_and_Display.Map import Map


class OperatorInterface:
    def __init__(self, mapInstance: Map, robotController: RobotController):
        self.__on_close_callback = None
        self.__mapInstance = mapInstance
        self.__robotController = robotController

        self.__hazards_display, self.__colorBlobs_display, self.__spots_display = None, None, None

        self.__cols, self.__rows = 0, 0
        self.__robotCol, self.__robotRow = -1, -1
        self.__spots, self.__hazards, self.__colorBlobs = [], [], []

        self.__master = tk.Tk()
        self.__master.title("Map Initialization")
        self.__master.config(bg=COLOR1)
        self.__master.withdraw()

        self.create_widgets()

    def run(self, on_close):
        # 프로그램 시작시 실행
        self.__on_close_callback = on_close
        center_window(self.__master)
        self.__master.geometry("900x500")
        self.__master.deiconify()
        self.__master.mainloop()

    def create_widgets(self):
        # 프레임 등 기본 뼈대 생성
        first_row = tk.Frame(self.__master)
        first_row.config(bg=COLOR1)
        first_row.pack(fill=tk.X)

        self.create_input_section(first_row, "Set Map Size", self.set_map_size)
        self.create_input_section(first_row, "Set Robot Start", self.set_robot_start)

        second_row = tk.Frame(self.__master)
        second_row.config(bg=COLOR1)
        second_row.pack(fill=tk.X)

        self.__spots_display = self.create_input_section(second_row, "Set Spots", self.set_spots, display=True)
        self.__colorBlobs_display = self.create_input_section(second_row, "Set Color Blobs", self.set_colorBlobs, display=True)
        self.__hazards_display = self.create_input_section(second_row, "Set Hazards", self.set_hazards, display=True)

        delete_message = tk.Label(self.__master, text="Double click each item to delete", font=("Serif", 12), bg=COLOR1, fg="#660099")
        delete_message.pack()

        start_button = tk.Button(self.__master, text="Start", font=("Serif", 12, "bold"), command=self.start_next_scene, bg="#660099", fg="#ebe0ff")
        start_button.pack(pady=5)

    def create_input_section(self, parent, label_text, command, display=False):
        # 좌표 입력 칸 생성
        frame = tk.Frame(parent)
        frame.config(bg=COLOR2)
        frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        title_label = tk.Label(frame, text=label_text, font=("Broadway", 20, "bold"), bg=COLOR2, fg = "#ebe0ff")
        title_label.pack(pady=5)

        input_frame = tk.Frame(frame)
        input_frame.config(bg=COLOR2)
        input_frame.pack(pady=2)

        col_label = tk.Label(input_frame, text="Column:", font=("Serif", 14), bg="#573d7f", fg = "#ebe0ff")
        col_label.pack(side=tk.LEFT, padx=3)
        col_entry = tk.Entry(input_frame, width=5, font=("Serif", 14, "bold"), bg = COLOR1, fg = "#46325d")  
        col_entry.pack(side=tk.LEFT, padx=3)

        row_label = tk.Label(input_frame, text="Row:", font=("Serif", 14), bg="#573d7f", fg = "#ebe0ff")
        row_label.pack(side=tk.LEFT, padx=3)
        row_entry = tk.Entry(input_frame, width=5, font=("Serif", 14, "bold"), bg = COLOR1, fg = "#46325d")
        row_entry.pack(side=tk.LEFT, padx=3)

        button = tk.Canvas(frame, width=40, height=40, bg=COLOR2, highlightthickness=0)
        button.pack(pady=8)
        circle = button.create_oval(5, 5, 35, 35, fill="#46325d", outline="#46325d")
        text_id = button.create_text(20, 20, text="OK", fill="#ebe0ff")

        button.tag_bind(circle, "<Button-1>", lambda event: command(col_entry.get(), row_entry.get(), frame))
        button.tag_bind(text_id, "<Button-1>", lambda event: command(col_entry.get(), row_entry.get(), frame))


        if display:
            list_frame = tk.Frame(frame, bg=COLOR2)

            list_frame.pack()

            display_area = tk.Listbox(list_frame, height=6, width=10, font=("Serif", 14), bg=COLOR1, fg=COLOR2)
            display_area.pack(side=tk.LEFT, fill=tk.BOTH, pady=5)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=display_area.yview)
            scrollbar.pack(side=tk.LEFT, fill=tk.Y, pady=5)
            display_area.config(yscrollcommand=scrollbar.set)

            display_area.bind('<Double-1>', lambda event, da=display_area: self.delete_item(da))
            return display_area

    def start_next_scene(self):
        # start 버튼을 누르면 입력된 맵 정보를 반영하고 종료
        if not (self.__cols != 0 and self.__rows != 0 and self.__robotCol != -1 and self.__robotRow != -1 and self.__spots and self.__colorBlobs and self.__hazards):
            messagebox.showerror("Invalid initialization", "❌ Please initialize the map with correct values.")
            return
        self.__mapInstance.set_map_length(self.__cols, self.__rows)
        robot_coord = (self.__robotCol, self.__robotRow, 0)
        self.__mapInstance.set_robot_coord(robot_coord)
        self.__robotController.set_current_position(robot_coord)
        spotsFormatted, hazardsFormatted, colorBlobsFormatted = [], [], []
        for spot in self.__spots:
            col, row = spot
            spotsFormatted.append(Spot(col, row, explored=False))
        for colorBlob in self.__colorBlobs:
            col, row = colorBlob
            colorBlobsFormatted.append(ColorBlob(col, row, hidden=True))
        for hazard in self.__hazards:
            col, row = hazard
            hazardsFormatted.append(Hazard(col, row, hidden=True))
        self.__mapInstance.set_spots(spotsFormatted)
        self.__mapInstance.set_hazards(hazardsFormatted)
        self.__mapInstance.set_color_blobs(colorBlobsFormatted)

        self.__master.destroy()
        self.__on_close_callback()

    def set_map_size(self, cols, rows, frame):
        # 맵 크기 설정
        try:
            self.__cols, self.__rows = (int(cols) + 1, int(rows) + 1)
            if self.__cols > 10 or self.__rows > 10 or self.__cols < 1 or self.__rows < 1:
                messagebox.showerror("Invalid Input", "❌ Please enter valid integers for columns and rows.")
                self.__cols, self.__rows = 0, 0
            else:
                messagebox.showinfo("Success", "✅ Map size set successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Please enter valid integers for columns and rows.")

    def set_robot_start(self, col, row, frame):
        # 로봇 위치 설정
        if self.is_valid_input(col, row):
            self.__robotCol, self.__robotRow = int(col), int(row)
            messagebox.showinfo("Success", "✅ Robot start position set successfully.")

    def set_spots(self, col, row, frame):
        # 탐색 지점 설정
        if self.is_valid_input(col, row):
            col, row = int(col), int(row)
            self.__spots.append((col, row))
            self.update_display(self.__spots_display, self.__spots)

    def set_colorBlobs(self, col, row, frame):
        # 중요 지점 설정
        if self.is_valid_input(col, row):
            col, row = int(col), int(row)
            self.__colorBlobs.append((col, row))
            self.update_display(self.__colorBlobs_display, self.__colorBlobs)

    def set_hazards(self, col, row, frame):
        # 위험 지점 설정
        if self.is_valid_input(col, row):
            col, row = int(col), int(row)
            self.__hazards.append((col, row))
            self.update_display(self.__hazards_display, self.__hazards)

    def is_valid_input(self, col, row):
        # 입력값이 적절한지 검사
        try:
            col, row = int(col), int(row)
            position = (col, row)
            if 0 <= col < self.__cols and 0 <= row < self.__rows:
                if position in self.__spots or position in self.__hazards or position in self.__colorBlobs or position == (self.__robotCol, self.__robotRow):
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
        # tkinter 업데이트
        display_area.delete(0, tk.END)
        for index, item in enumerate(items, start=1):
            display_area.insert(tk.END, f"#{index}: {item}")

    def delete_item(self, display_area):
        # 더블클릭하여 리스트에 있는 아이템 삭제
        try:
            selected_index = display_area.curselection()[0]
            display_area.delete(selected_index)
            if display_area == self.__spots_display:
                self.__spots.pop(selected_index)
            elif display_area == self.__colorBlobs_display:
                self.__colorBlobs.pop(selected_index)
            elif display_area == self.__hazards_display:
                self.__hazards.pop(selected_index)
        except IndexError:
            pass  # 삭제할 아이템이 없는 경우
