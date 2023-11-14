import tkinter as tk
from tkinter import StringVar
from tkinter import *
from PIL import Image, ImageTk
import turtle
from Path_Planning_and_Map_Management.Map import Map


class Display:
    def __init__(self, mapInstance: Map):
        n, m = mapInstance.get_map_length()
        spot_pairs = mapInstance.get_spots()
        hazard_pairs = mapInstance.get_hazards()
        color_blob_pairs = mapInstance.get_color_blobs()

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
        robot_image = Image.open("/Users/osh/Library/Mobile Documents/com~apple~CloudDocs/UOS 23/UOS 23-2/소프트웨어 공학/과제/mobileRobotController/robot.png")
        self.robot_photo = ImageTk.PhotoImage(robot_image)
        
        #Draw
        for pair in spot_pairs:
            x, y = pair.get_position()
            self.draw_star(c, x, y, grid_size)

        for pair in hazard_pairs:
            x, y = pair.get_position()
            self.draw_circle(c, x, y, grid_size)

        for pair in color_blob_pairs:
            x, y = pair.get_position()
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
