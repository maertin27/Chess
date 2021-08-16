import tkinter as tk
import tkinter as tk
from chess_board import *
from PIL import *
from pieces import *

def print_board2(board,root):
    imgs = []
    for color in ['w', 'b']:
        for piece in ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']:
            imgs.append(tk.PhotoImage(file=f"chess_pieces\Chess_{color}{piece}.png"))
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
            canvas.grid(ipadx=60, ipady=60)
            if file:
                counter = 0
                for color in ['w', 'b']:
                    for piece in [King, Queen, Rook, Bishop, Knight, Pawn]:
                        if file.color == color and isinstance(file,piece):
                            canvas.create_image(65,60,anchor='center', image=imgs[counter])
                        counter += 1
    root.update()