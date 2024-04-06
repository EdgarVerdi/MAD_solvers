import re
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

window = tk.Tk()
window.geometry("600x800")


def frameOfMatrix(matrix, fatherFrame):
    """

    :param matrix: The matrix to be framed
    :param fatherFrame: An empty frame to be filled
    :return: the frame that was generated
    """
    frame = tk.Frame(fatherFrame, width=1, height=1)
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        for j in range(cols):
            cell = tk.Text(frame, width=3, height=2)
            cell.insert(tk.INSERT, matrix[i][j])
            cell.grid(row=i, column=j)
    return frame


# rowsQuestionFrame.grid(row=0, column=0)
matFrame: tk.Frame = frameOfMatrix([[2, 4], [1, 5]], window)
matFrame.grid(row=1, column=1)

window.mainloop()
