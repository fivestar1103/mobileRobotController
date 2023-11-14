import tkinter as tk
from tkinter import StringVar
from tkinter import *
from PIL import Image, ImageTk
import turtle 

class Display:
    def __init__(self, master, n, m, a, b, spot_pairs, color_blob_pairs, hazard_pairs):
        self.master = master
        self.master.title('Display Window')

        # Display the received data in the new window
        gui = tk.Tk()
        gui.title('Grid Map')
        grid_size = 100

        # Create a canvas
        c = Canvas(gui, width=grid_size * n, height=grid_size * m, background='white')
        c.pack()

        for x in range(0, grid_size * n, grid_size):
            for y in range(0, grid_size * m, grid_size):
                c.create_rectangle(x, y, x + grid_size, y + grid_size, outline='black')

        # Load and display the robot image at the specified start location
        robot_image = PhotoImage.open("C:/Users/Aiganym(01021515882)/Desktop/robot.jpg", width=30, height=30)
        self.robot_photo = ImageTk.PhotoImage(robot_image)
        
        #Draw
        for pair in spot_pairs:
            x, y = map(int, pair)
            self.draw_star(c, x, y, grid_size)

        for pair in hazard_pairs:
            x, y = map(int, pair)
            self.draw_circle(c, x, y, grid_size)

        for pair in color_blob_pairs:
            x, y = map(int, pair)
            self.draw_rectangle(c, x, y, grid_size)    
        gui.mainloop()

    def draw_star(self, canvas, x, y, grid_size, color="yellow"):
        angle = 120
        canvas.create_polygon(
            x, y - grid_size,
            x + grid_size * 0.15, y - grid_size * 0.35,
            x + grid_size, y - grid_size,
            x + grid_size * 0.35, y - grid_size * 0.15,
            x + grid_size * 0.5, y,
            x + grid_size * 0.35, y + grid_size * 0.15,
            x + grid_size, y + grid_size,
            x + grid_size * 0.15, y + grid_size * 0.35,
            x, y + grid_size,
            x - grid_size * 0.15, y + grid_size * 0.35,
            x - grid_size, y + grid_size,
            x - grid_size * 0.35, y + grid_size * 0.15,
            x - grid_size * 0.5, y,
            x - grid_size * 0.35, y - grid_size * 0.15,
            fill=color,
            outline=color
        )   

    def draw_circle(self, canvas, x, y, grid_size, color="black"):
        size = grid_size * 0.5
        canvas.create_oval(
            x * grid_size, y * grid_size,
            x * grid_size + size, y * grid_size + size,
            fill=color, outline=color
        )
    def draw_rectangle(self, canvas, x, y, grid_size, color="blue"):
        size = grid_size * 0.5
        canvas.create_rectangle(
            x * grid_size, y * grid_size,
            x * grid_size + size, y * grid_size + size,
            fill=color, outline=color
        )

class OperatorInterface:
    def __init__(self, master):
        self.master = master
        self.master.title('Mobile Robot Controller')

        self.label = tk.Label(master, text='Input Map data')
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # 사용자 id와 password를 저장하는 변수 생성
        self.map_var, self.start_var, self.spot_var, self.colorBlob_var, self.hazard_var = (
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        )

        # id와 password, 그리고 확인 버튼의 UI를 만드는 부분
        tk.Label(master, text="MapLength : ").grid(row=1, column=0, padx=10, pady=10)
        self.map_entry = tk.Entry(master, textvariable=self.map_var, fg='grey')
        self.map_entry.insert(0, '"4 5"와 같이 입력하세요')
        self.map_entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, self.map_entry, '"4 5"와 같이 입력하세요'))
        self.map_entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.map_entry, '"4 5"와 같이 입력하세요'))
        self.map_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(master, text="Start : ").grid(row=2, column=0, padx=10, pady=10)
        self.start_entry = tk.Entry(master, textvariable=self.start_var, fg='grey')
        self.start_entry.insert(0, '"4 5"와 같이 입력하세요')
        self.start_entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, self.start_entry, '"4 5"와 같이 입력하세요'))
        self.start_entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.start_entry, '"4 5"와 같이 입력하세요'))
        self.start_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(master, text="Spots : ").grid(row=3, column=0, padx=10, pady=10)
        self.spot_entry = tk.Entry(master, textvariable=self.spot_var, fg='grey')
        self.spot_entry.insert(0, '"4 5,1 5"와 같이 입력하세요')
        self.spot_entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, self.spot_entry, '"4 5,1 5"와 같이 입력하세요'))
        self.spot_entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.spot_entry, '"4 5,1 5"와 같이 입력하세요'))
        self.spot_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(master, text="Color : ").grid(row=4, column=0, padx=10, pady=10)
        self.colorBlob_entry = tk.Entry(master, textvariable=self.colorBlob_var, fg='grey')
        self.colorBlob_entry.insert(0, '"4 5,1 5"와 같이 입력하세요')
        self.colorBlob_entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, self.colorBlob_entry, '"4 5,1 5"와 같이 입력하세요'))
        self.colorBlob_entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.colorBlob_entry, '"4 5,1 5"와 같이 입력하세요'))
        self.colorBlob_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(master, text="Hazard : ").grid(row=5, column=0, padx=10, pady=10)
        self.hazard_entry = tk.Entry(master, textvariable=self.hazard_var, fg='grey')
        self.hazard_entry.insert(0, '"4 5,1 5"와 같이 입력하세요')
        self.hazard_entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, self.hazard_entry, '"4 5,1 5"와 같이 입력하세요'))
        self.hazard_entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.hazard_entry, '"4 5,1 5"와 같이 입력하세요'))
        self.hazard_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(master, text="GO", command=self.open_result_window).grid(row=6, column=1, padx=10, pady=10)

    def on_entry_click(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg='grey')

       
    def open_result_window(self):
        # Get the entered data
        map_data = self.map_entry.get()
        start_data = self.start_entry.get()
        spot_data = self.spot_entry.get()
        color_data = self.colorBlob_entry.get()
        hazard_data = self.hazard_entry.get()

        # Split the map_data and convert to integers
        map_values = map_data.split()
        n = int(map_values[0])
        m = int(map_values[1])

        start_values = start_data.split()
        a = int(start_values[0])
        b = int(start_values[1])

        spot_pairs = [tuple(map(int, pair.strip().split())) for pair in spot_data.split(',')]
        color_blob_pairs = [tuple(map(int, pair.strip().split())) for pair in color_data.split(',')]
        hazard_pairs = [tuple(map(int, pair.strip().split())) for pair in hazard_data.split(',')]
        
        print(f"n: {n}, m: {m}")  # for debugging
        print(f"a: {a}, b: {b}")
        print(f"s: {spot_pairs}")
        print(f"c: {color_blob_pairs}")
        print(f"h: {hazard_pairs}")
        
        # Create a new window with the received data
        result_window = tk.Toplevel(self.master)
        Display(result_window, n, m, a, b, spot_pairs, color_blob_pairs, hazard_pairs)

if __name__ == "__main__":
    root = tk.Tk()
    app = OperatorInterface(root)
    root.mainloop()
