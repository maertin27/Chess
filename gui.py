import tkinter as tk
import tkinter as tk
from chess_board import *
from PIL import *

def print_board2(board, root):
    img = tk.PhotoImage(file="chess_pieces\Chess_wKing.png")
    for i, row in enumerate(board):
        for j, file in enumerate(row):
            frame = tk.Frame(master=root,
                             relief=tk.RAISED,
                             borderwidth=0.1,
                             bd = 0.1
                             )
            frame.grid(row=i, column=j)
            if (i + j) % 2:
                color = 'antique white'
            else:
                color = 'sienna4'
            canvas = tk.Canvas(frame, bg=color, width=9, height=4)
            canvas.grid(ipadx=60,ipady=60)
            if file:
                canvas.create_image(65,60,anchor='center', image=file.img)
    root.mainloop()