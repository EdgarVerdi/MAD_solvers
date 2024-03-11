import tkinter as tk

window = tk.Tk()
window.geometry("300x200")

rowsQuestionFrame = tk.Frame(window)
rowsQuestionFrame.grid(row=0, column=0)
tk.Label(rowsQuestionFrame, text="How many Rows?").grid(row=0, column=0)
numberOfRowsRequested = tk.StringVar()
tk.Entry(rowsQuestionFrame, textvariable=numberOfRowsRequested).grid(row=0, column=1)
numberOfRowsInUse = 0

tableFrame = tk.Frame(window)
tableFrame.grid(row=1, column=0)
cells = {}


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


button = tk.Button(rowsQuestionFrame, text="Create Table", command=genNewTable)
button.grid(row=1, column=0)

window.mainloop()
