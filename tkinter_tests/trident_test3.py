import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

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
        for j in range(3):
            text = cells[(i, j)]
            text.grid_forget()

    # more rows
    for i in range(oldNumberOfRowsInUse, numberOfRowsInUse):
        for j in range(3):
            text = cells.get((i, j), None)
            if text is None:
                text = tk.Text(tableFrame, width=16, height=1)
                text.insert(tk.INSERT, "0")
                cells[(i, j)] = text
            text.grid(row=i + 1, column=j)


createTableButton = tk.Button(rowsQuestionFrame, text="Create Table", command=genNewTable)
createTableButton.grid(row=1, column=0)


def getVariableEquations():
    # sorry for the one-liner but it just felt way more efficient than append xD
    try:
        l = [tuple([float(cells[(i, j)].get("1.0", 'end-1c')) for j in range(3)]) for i in range(numberOfRowsInUse)]
        return [np.asarray([A - C, B - C, C]) for A, B, C in l]
    except ValueError:
        raise ValueError  # TODO better error here


def plotFunc():
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 1, .01)
    t2 = np.arange(1, 0, -.01)
    # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    sub = fig.add_subplot(111)
    sub.plot(t, t2)

    variableEq = getVariableEquations()
    for y, x, c in [a - b for idx, a in enumerate(variableEq) for b in variableEq[idx + 1:]]:
        if y != 0:
            sub.plot(t, -(x * t + c) / y)

    sub.set_xlim([0, 1])
    sub.set_ylim([0, 1])

    for widget in canvasFrame.winfo_children():
        widget.destroy()  # clean previous canvas

    canvas = FigureCanvasTkAgg(fig, master=canvasFrame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, canvasFrame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


plotButton = tk.Button(window, text="Plot", command=plotFunc)
plotButton.grid(row=2, column=0)

window.mainloop()
