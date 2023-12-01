import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from Utilities.UI_utilities import center_window

from Map_Management_and_Display.Map import Map
from Map_Management_and_Display.VoiceInputHandler import VoiceInputHandler


class Display:
    def __init__(self, SIMControllerInstance, mapInstance: Map):
        self.__canvas_width, self.__canvas_height = None, None
        self.__rows, self.__cols = None, None

        self.__mic_button, self.__goOrStop_button, self.__auto_move_button = None, None, None
        self.__images = {}
        self.__log_text, self.__log_scroll = None, None
        self.__canvas = None
        self.__button_frame, self.__log_frame, self.__canvas_frame = None, None, None

        self.color1 = "#ebe0ff"
        self.color2 = "#7151a9"
        self.color3 = "#660099"
        self.color4 = "#46325d"
        self.color5 = "#dac7ff"
        self.color6 = "#3f3649"

        self.master = tk.Tk()
        self.master.config(bg=self.color1)
        self.master.title("Mobile Robot Controller")

        self.__SIMControllerInstance = SIMControllerInstance
        self.__mapInstance = mapInstance
        self.__voiceInputHandler = VoiceInputHandler(self.master, self.__mapInstance, self.update_display)

        self.__isStop = True
        self.__autoMove = False
        self.__log_counter = 0  # 이벤트 로그 작성을 위한 카운터
        self.__axis_padding = 15  # 맵을 프레임에서 살짝 띠워서 배치하기 위한 패딩
        self.__cell_size = 50  # 맵 상 한칸한칸의 사이즈

        self.load_images()  # 이미지 불러오기
        self.master.withdraw()  # 화면 가리기

    def run(self):
        # OperatorInterface로 초기화가 완료되면 세팅 실행
        self.__SIMControllerInstance.set_path()  # 경로 설정

        self.__cols, self.__rows = self.__mapInstance.get_map_length()
        self.__canvas_width = self.__cols * self.__cell_size + 2 * self.__axis_padding
        self.__canvas_height = self.__rows * self.__cell_size + 2 * self.__axis_padding

        self.setup_frames()
        self.create_buttons()

        center_window(self.master)
        self.update_display()

        self.master.deiconify()  # 화면 보이기
        self.master.after(500, self.__SIMControllerInstance.send_movement_command)  # 0.5초마다 다음 동작 명령을 지시
        self.master.mainloop()

    def setup_frames(self):
        # 프레임 생성
        self.__canvas_frame = tk.Frame(self.master, relief="groove", padx=10, pady=10, bg=self.color2)
        self.__log_frame = tk.Frame(self.master, relief="groove", padx=10, pady=10, bg=self.color2)
        self.__button_frame = tk.Frame(self.master, relief="groove", padx=10, pady=10, bg=self.color2)
        self.__out_frame = tk.Frame(self.master, relief="groove", padx=10, pady=10, bg=self.color2)

        # 프레임에 안에 그리드 생성
        self.__canvas_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=(10, 5))
        self.__button_frame.grid(row=1, column=0, sticky="ew", padx=(5, 5), pady=(10, 5))
        self.__log_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=(10, 5))
        self.__out_frame.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady=(10, 5))

        # 프레임에 제목 설정
        log_title = tk.Label(self.__log_frame, text="Event Log", font=("Broadway", 25, "bold"), bg=self.color2, fg = self.color1) 
        log_title.pack(side=tk.TOP, pady=10)
        canvas_title = tk.Label(self.__canvas_frame, text="Map", font=("Broadway", 30, "bold"), bg=self.color2,fg = self.color1)
        canvas_title.pack(side=tk.TOP, pady=10)

        self.out_button = tk.Button(self.__out_frame, text="EXIT", font=("Serif", 14, "bold"), height=2, bg = self.color2, fg = self.color1, command=self.on_out_button_clicked)
        self.out_button.pack(pady=5, fill=tk.X)

    def on_out_button_clicked(self):
        # 현재 윈도우를 닫습니다.
        self.master.destroy()

        # 캔버스(맵 표시 프레임) 설정
        self.__canvas = tk.Canvas(self.__canvas_frame, width=self.__canvas_width, height=self.__canvas_height,
                                bg=self.color1, highlightbackground=self.color6)
        self.__canvas.pack(side='top', fill='both', expand=True)

        # 이벤트 로그 설정
        self.__log_scroll = tk.Scrollbar(self.log_frame)
        self.__log_text = tk.Text(self.log_frame, yscrollcommand=self.log_scroll.set,
                                state='disabled', bg=self.color1, width=38,
                                highlightbackground=self.color6)
        self.__log_scroll.config(command=self.log_text.yview)
        self.__log_scroll.pack(side='right', fill='y')
        self.__log_text.pack(side='left', fill='both', expand=False)

    def create_buttons(self):
        # 버튼 프레임 생성
        self.__button_frame.pack_propagate(False)
        self.__button_frame.config(width=180, height=80)

        # 자동 이동 버튼 생성
        self.__auto_move_button = tk.Button(self.__button_frame, command=self.toggle_auto_move, text="Auto Move Off", font=("Arial", 12, "bold"),
                                          borderwidth=0, highlightthickness=0, compound=tk.CENTER, relief='flat', fg = self.color1, bg = self.color3,
                                          width=15, height=3
                                          )
        self.__auto_move_button.grid(row=0, column=0, padx=5, pady=2)

        # 재생/멈춤 버튼 생성
        initial_image = self.__images["buttons"]["go"] if self.__isStop else self.__images["buttons"]["stop"]
        self.__goOrStop_button = tk.Button(self.__button_frame, image=initial_image, command=self.on_goOrStop,
                                        borderwidth=0, highlightthickness=0, compound=tk.CENTER, relief='flat')
        self.__goOrStop_button.image = initial_image
        self.__goOrStop_button.grid(row=0, column=1, padx=5, pady=2)

        # 녹음 버튼 생성
        self.__mic_button = tk.Button(
            self.__button_frame,
            image=self.__images["buttons"]["mic_enabled"],
            command=self.__voiceInputHandler.run,
            state=tk.NORMAL,
            borderwidth=0,
            highlightthickness=0,
            compound=tk.CENTER,
            relief='flat'
        )

        self.__mic_button.image = self.__images["buttons"]["mic_enabled"]
        self.__mic_button.pack(side=tk.TOP, fill=tk.NONE, pady=2)  

    def update_display(self):
        # 화면의 모든 구성요소를 지우고 전부 다시 그린다
        self.__canvas.delete("all")

        # 전체 칸을 하얀색으로 표시
        for col in range(self.__cols):
            for row in range(self.__rows):
                self.draw_element((col, row), "white")

        self.draw_axes()  # 축 번호 표시

        # 경로 표시
        self.draw_path(self.__SIMControllerInstance.get_path())

        # 위험/중요/탐색 지점 표시
        for hazard in self.__mapInstance.get_hazards():
            self.draw_image(hazard.get_position(),
                            self.__images["hazard"]["revealed"] if not hazard.is_hidden() else self.__images["hazard"][
                                "hidden"])

        for colorBlob in self.__mapInstance.get_color_blobs():
            self.draw_image(colorBlob.get_position(),
                            self.__images["colorBlob"]["revealed"] if not colorBlob.is_hidden() else
                            self.__images["colorBlob"]["hidden"])

        for spot in self.__mapInstance.get_spots():
            self.draw_image(spot.get_position(),
                            self.__images["spot"]["visited"] if spot.is_explored() else self.__images["spot"][
                                "unvisited"])

        self.draw_robot()  # 로봇 표시

        self.master.update_idletasks()  # tkinter 업데이트

    def draw_axes(self):
        # 맵 위아래에 열번호 표시
        for i in range(self.__cols):
            x1 = i * self.__cell_size + self.__cell_size / 2 + self.__axis_padding
            x2 = x1
            y1 = self.__axis_padding + self.__cell_size / 2
            y2 = y1 + self.__canvas_height - self.__cell_size - self.__axis_padding*2
            self.__canvas.create_line([x1, y1], [x2, y2], fill=self.color6, width=1)

            self.__canvas.create_text(x1, self.__axis_padding / 2, text=str(i), font=("Serif", 12, "bold"), fill = self.color4, anchor="e")
            self.__canvas.create_text(x1, self.__canvas_height - self.__axis_padding / 2, text=str(i), font=("Serif", 12, "bold"), fill = self.color4,anchor="e")

        # 맵 좌우에 행번호 표시
        for i in range(self.__rows):
            x1 = self.__axis_padding + self.__cell_size / 2
            x2 = x1 + self.__canvas_width - self.__cell_size - self.__axis_padding*2
            y1 = i * self.__cell_size + self.__cell_size / 2 + self.__axis_padding
            y2 = y1
            self.__canvas.create_line([x1, y1], [x2, y2], fill=self.color6, width=1)

            self.__canvas.create_text(self.__axis_padding / 2, y1, text=str(self.__rows - 1 - i), font=("Serif", 12, "bold"), fill = self.color4,anchor="n")
            self.__canvas.create_text(self.__canvas_width - self.__axis_padding / 2, y1, text=str(self.__rows - 1 - i), font=("Serif", 12, "bold"), fill = self.color4,anchor="n")

    def draw_element(self, position, color, alpha='#'):
        # 전체 칸 그리기
        col, row = position
        x1 = col * self.__cell_size + self.__axis_padding
        y1 = (self.__rows - row - 1) * self.__cell_size + self.__axis_padding
        x2 = x1 + self.__cell_size
        y2 = y1 + self.__cell_size
        if alpha != '#':
            color = color + alpha
        self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")

    def draw_path(self, path):
        # 경로 그리기
        if path:
            # 경로를 맵 상의 좌표로 변환
            pathWithSelfCoord = reversed(path + [self.__mapInstance.get_robot_coord()[:2]])
            canvas_path = [(col * self.__cell_size + self.__cell_size // 2 + self.__axis_padding,
                            (self.__rows - row - 1) * self.__cell_size + self.__cell_size // 2 + self.__axis_padding)
                           for
                           col, row in pathWithSelfCoord]

            # 각 점 사이에 점선 그리기
            for i in range(len(canvas_path) - 1):
                self.__canvas.create_line(canvas_path[i], canvas_path[i + 1], fill=self.color3, width=3, dash=(4, 2),
                                          arrow=tk.LAST)

    def draw_robot(self):
        # 로봇 그리기
        robotRow, robotCol, robotDirection = self.__mapInstance.get_robot_coord()
        x1 = robotRow * self.__cell_size + self.__axis_padding
        y1 = (self.__mapInstance.get_map_length()[1] - robotCol - 1) * self.__cell_size + self.__axis_padding
        self.__canvas.create_image(x1, y1, anchor="nw", image=self.__images["robot"][robotDirection])

    def draw_image(self, position, image):
        # 위험/중요/탐색 지점 그리기
        col, row = position
        x = col * self.__cell_size + self.__axis_padding
        y = (self.__rows - row - 1) * self.__cell_size + self.__axis_padding  # Adjust for y-axis inversion
        self.__canvas.create_image(x, y, anchor="nw", image=image)

    def load_images(self):
        # 이미지 불러오기
        self.__images["robot"] = {
            0: ImageTk.PhotoImage(Image.open("assets/Robot_N.png").resize((self.__cell_size, self.__cell_size))),
            1: ImageTk.PhotoImage(Image.open("assets/Robot_E.png").resize((self.__cell_size, self.__cell_size))),
            2: ImageTk.PhotoImage(Image.open("assets/Robot_S.png").resize((self.__cell_size, self.__cell_size))),
            3: ImageTk.PhotoImage(Image.open("assets/Robot_W.png").resize((self.__cell_size, self.__cell_size)))
        }

        self.__images["colorBlob"] = {
            "revealed": ImageTk.PhotoImage(
                Image.open("assets/ColorBlob_revealed.png").resize((self.__cell_size, self.__cell_size))),
            "hidden": ImageTk.PhotoImage(
                Image.open("assets/ColorBlob_hidden.png").resize((self.__cell_size, self.__cell_size)))
        }

        self.__images["hazard"] = {
            "revealed": ImageTk.PhotoImage(
                Image.open("assets/Hazard_revealed.png").resize((self.__cell_size, self.__cell_size))),
            "hidden": ImageTk.PhotoImage(
                Image.open("assets/Hazard_hidden.png").resize((self.__cell_size, self.__cell_size)))
        }

        self.__images["spot"] = {
            "visited": ImageTk.PhotoImage(
                Image.open("assets/Spot_visited.png").resize((self.__cell_size, self.__cell_size))),
            "unvisited": ImageTk.PhotoImage(
                Image.open("assets/Spot_unvisited.png").resize((self.__cell_size, self.__cell_size)))
        }

        self.__images["buttons"] = {
            "go": ImageTk.PhotoImage(
                Image.open("assets/go_button.png").resize((self.__cell_size, self.__cell_size))),
            "stop": ImageTk.PhotoImage(
                Image.open("assets/stop_button.png").resize((self.__cell_size, self.__cell_size))),
            "mic_enabled": ImageTk.PhotoImage(
                Image.open("assets/mic_button_enabled.png").resize((self.__cell_size, self.__cell_size))),
            "mic_disabled": ImageTk.PhotoImage(
                Image.open("assets/mic_button_disabled.png").resize((self.__cell_size, self.__cell_size)))
        }

    def log_message(self, message):
        # 색깔을 번갈아가며 로그 박스를 표시
        color = "#18005f" if self.__log_counter % 2 == 0 else "#660099"
        self.__log_counter += 1

        # 텍스트 삽입
        self.__log_text.config(state='normal')
        if self.__log_counter > 1:
            self.__log_text.insert('1.0', '\n')

        # 로그박스 생성
        log_frame = tk.Frame(self.__log_text, bg=color, highlightthickness=0)  
        log_label = tk.Label(log_frame, text=f"#{self.__log_counter}: {message}", bg = self.color1, fg=color, font=("Serif", 12), anchor='w',
                             justify=tk.LEFT, width=30)
        log_label.pack(side=tk.TOP, fill=tk.X)  
        self.__log_text.window_create('1.0', window=log_frame)  # 제일 위에 배치
        self.__log_text.yview('1.0')  # 제일 위로 오토 스크롤
        self.__log_text.config(state='disabled')

    def toggle_auto_move(self):
        # 자동 이동 버튼 로직
        self.__autoMove = not self.__autoMove
        if self.__autoMove:
            text = "Auto Move On"
            bg = self.color1
            fg = self.color3
        else:
            text = "Auto Move Off"
            bg = self.color6
            fg = self.color1
        self.__auto_move_button.config(text=text, bg=bg, fg=fg)
        self.__isStop = True if self.__autoMove else False
        self.on_goOrStop()

    def on_goOrStop(self):
        # 재생/중지 버튼 로직
        self.__isStop = not self.__isStop
        new_image = self.__images["buttons"]["go"] if self.__isStop else self.__images["buttons"]["stop"]
        self.__goOrStop_button.config(image=new_image)
        self.__goOrStop_button.image = new_image  # Update the reference to prevent garbage collection

        # 녹음 버튼 바꾸기
        mic_new_image = self.__images["buttons"]["mic_enabled"] if self.__isStop else self.__images["buttons"]["mic_disabled"]
        self.__mic_button.config(image=mic_new_image, state=tk.NORMAL if self.__isStop else tk.DISABLED)
        self.__mic_button.image = mic_new_image  # Update the reference

        # 자동이동시에는 계속해서, 아닐때는 버튼 누를때마다 이동 지시 내리기
        if self.__autoMove:
            self.__SIMControllerInstance.send_movement_command()
        else:
            self.__mic_button.config(image=self.__images["buttons"]["mic_enabled"], state=tk.NORMAL)
            self.__SIMControllerInstance.send_movement_command()
            self.__isStop = True
            self.__goOrStop_button.config(image=self.__images["buttons"]["go"])

    def alert(self, message):
        messagebox.showinfo(message=message)  # 경고 팝업

    # Getters
    def get_canvas_width(self):
        return self.__canvas_width

    def get_canvas_height(self):
        return self.__canvas_height

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    def get_mic_button(self):
        return self.__mic_button

    def get_goOrStop_button(self):
        return self.__goOrStop_button

    def get_auto_move_button(self):
        return self.__auto_move_button

    def get_images(self):
        return self.__images

    def get_log_text(self):
        return self.__log_text

    def get_log_scroll(self):
        return self.__log_scroll

    def get_canvas(self):
        return self.__canvas

    def get_button_frame(self):
        return self.__button_frame

    def get_log_frame(self):
        return self.__log_frame

    def get_canvas_frame(self):
        return self.__canvas_frame

    def get_SIMControllerInstance(self):
        return self.__SIMControllerInstance

    def get_mapInstance(self):
        return self.__mapInstance

    def get_voiceInputHandler(self):
        return self.__voiceInputHandler

    def get_isStop(self):
        return self.__isStop

    def get_autoMove(self):
        return self.__autoMove

    def get_log_counter(self):
        return self.__log_counter

    def get_axis_padding(self):
        return self.__axis_padding

    def get_cell_size(self):
        return self.__cell_size

    # Setters
    def set_canvas_width(self, width):
        self.__canvas_width = width

    def set_canvas_height(self, height):
        self.__canvas_height = height

    def set_rows(self, rows):
        self.__rows = rows

    def set_cols(self, cols):
        self.__cols = cols

    def set_mic_button(self, mic_button):
        self.__mic_button = mic_button

    def set_goOrStop_button(self, goOrStop_button):
        self.__goOrStop_button = goOrStop_button

    def set_auto_move_button(self, auto_move_button):
        self.__auto_move_button = auto_move_button

    def set_images(self, images):
        self.__images = images

    def set_log_text(self, log_text):
        self.__log_text = log_text

    def set_log_scroll(self, log_scroll):
        self.__log_scroll = log_scroll

    def set_canvas(self, canvas):
        self.__canvas = canvas

    def set_button_frame(self, button_frame):
        self.__button_frame = button_frame

    def set_log_frame(self, log_frame):
        self.__log_frame = log_frame

    def set_canvas_frame(self, canvas_frame):
        self.__canvas_frame = canvas_frame

    def set_SIMControllerInstance(self, SIMControllerInstance):
        self.__SIMControllerInstance = SIMControllerInstance

    def set_mapInstance(self, mapInstance):
        self.__mapInstance = mapInstance

    def set_voiceInputHandler(self, voiceInputHandler):
        self.__voiceInputHandler = voiceInputHandler

    def set_isStop(self, isStop):
        self.__isStop = isStop

    def set_autoMove(self, autoMove):
        self.__autoMove = autoMove

    def set_log_counter(self, log_counter):
        self.__log_counter = log_counter

    def set_axis_padding(self, axis_padding):
        self.__axis_padding = axis_padding

    def set_cell_size(self, cell_size):
        self.__cell_size = cell_size
