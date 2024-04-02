import re
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np


def excel_col(col):
    """
    Covert 0-relative column number to excel-style column label.
    inspired by: https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number
    """
    col+=1
    t = ''
    while col != 0:
        col, rem = divmod(col-1,26)
        t = chr(rem+ord('A')) + t
    return t


window = tk.Tk()
window.geometry("600x800")

rowsQuestionFrame = tk.Frame(window)
rowsQuestionFrame.grid(row=0, column=0)
tk.Label(rowsQuestionFrame, text="How many Rows?").grid(row=0, column=0)
numberOfRowsRequested = tk.StringVar()
tk.Entry(rowsQuestionFrame, textvariable=numberOfRowsRequested).grid(row=0, column=1)
numberOfRowsInUse = 0

tableFrame = tk.Frame(window)
tableFrame.grid(row=1, column=0)
cells = {}

canvasFrame = tk.Frame(window)
canvasFrame.grid(row=3, column=0)


def genNewTable():
    global numberOfRowsInUse
    oldNumberOfRowsInUse = numberOfRowsInUse
    numberOfRowsInUse = numberOfRowsRequested.get()
    numberOfRowsInUse = int(numberOfRowsInUse) if numberOfRowsInUse != '' else 0

    # less rows
    for i in range(numberOfRowsInUse, oldNumberOfRowsInUse):
        for j in range(0, 4):
            text = cells[(i, j)]
            text.grid_forget()

    # more rows
    for i in range(oldNumberOfRowsInUse, numberOfRowsInUse):
        # putting the Text Cell
        text = cells.get((i, 0), None)
        if text is None:
            text = tk.Text(tableFrame, width=16, height=1, bg="#A0A0A0")
            text.insert(tk.INSERT, excel_col(i))
            cells[(i, 0)] = text
        text.grid(row=i + 1, column=0)

        # putting the Value Cells
        for j in range(1, 4):
            text = cells.get((i, j), None)
            if text is None:
                text = tk.Text(tableFrame, width=16, height=1)
                text.insert(tk.INSERT, "0")
                cells[(i, j)] = text
            text.grid(row=i + 1, column=j)


def putFromClipBoard():
    clip = window.clipboard_get().strip("\n")
    line = [[float(f) for f in re.findall("(\d+\.\d|\d+)", l)] for l in clip.split("\n")]
    for i, l in enumerate(line):
        for j, f in zip(range(1, 4), l):
            text = cells[(i, j)]
            text.delete(1.0, tk.END)
            text.insert(tk.END, f)


createTableButton = tk.Button(rowsQuestionFrame, text="Create Table", command=genNewTable)
createTableButton.grid(row=1, column=0)

importTableButton = tk.Button(rowsQuestionFrame, text="Import Table From Clipboard", command=putFromClipBoard)
importTableButton.grid(row=1, column=1)


def getVariableEquations():
    # sorry for the one-liner but it just felt way more efficient than append xD
    try:
        l = [tuple([float(cells[(i, j)].get("1.0", 'end-1c')) for j in range(1, 4)]) for i in range(numberOfRowsInUse)]
        return [np.asarray([A - C, B - C, C]) for A, B, C in l]
    except ValueError:
        raise ValueError  # TODO better error here


def plotFunc():
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 1, .01)
    t2 = np.arange(1, 0, -.01)
    # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    sub = fig.add_subplot(111)
    sub.plot(t, t2, label="max", color="black")

    variableEq = getVariableEquations()
    cell_names = [cells[(i, 0)].get('1.0', 'end-1c') for i in range(numberOfRowsInUse)]
    for (y, x, c), i1, i2 in [(a - b, idx, idy) for idx, a in enumerate(variableEq) for idy, b in enumerate(variableEq[idx + 1:], idx + 1)]:
        if y != 0:
            sub.plot(t, -(x * t + c) / y, label=f"{cell_names[i1]}_{cell_names[i2]}")

    sub.set_xlim([0, 1])
    sub.set_ylim([0, 1])

    for widget in canvasFrame.winfo_children():
        widget.destroy()  # clean previous canvas

    canvas = FigureCanvasTkAgg(fig, master=canvasFrame)  # A tk.DrawingArea.
    sub.legend()
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, canvasFrame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


plotButton = tk.Button(window, text="Plot", command=plotFunc)
plotButton.grid(row=2, column=0)

window.mainloop()
