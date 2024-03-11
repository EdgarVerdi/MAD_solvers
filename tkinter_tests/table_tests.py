from tkinter import *
import pandas as pd

# Create an instance of tkinter frame
window = Tk()

# Set the size of the tkinter window
window.geometry("300x200")

# Load data from source
# df = pd.read_excel("data.xlsx")

# Extract number of rows and columns
n_rows = 4
n_cols = 2

# Extracting columns from the data and
# creating text widget with some
# background color
column_names = "AB" # df.columns
i = 0
for j, col in enumerate(column_names):
    text = Text(window, width=16, height=1, bg="#9BC2E6")
    text.grid(row=i, column=j)
    text.insert(INSERT, col)

# adding all the other rows into the grid
for i in range(n_rows):
    for j in range(n_cols):
        text = Text(window, width=16, height=1)
        text.grid(row=i + 1, column=j)
        text.insert(INSERT, 10)

window.mainloop()
