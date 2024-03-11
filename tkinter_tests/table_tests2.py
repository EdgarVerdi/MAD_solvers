# import required modules
from tkinter import *
import pandas as pd

# Create an instance of tkinter frame
window = Tk()

# Set the size of the tkinter window
window.geometry("300x200")

# Load data from source
# df = pd.read_excel("data.xlsx")

# Extract number of rows and columns
n_rows = 2 # df.shape[0]
n_cols = 3 # df.shape[1]

# Extracting columns from the data and
# creating text widget with some
# background color
column_names = "ABC" # df.columns
i = 0
for j, col in enumerate(column_names):
    text = Text(window, width=16, height=1, bg="#9BC2E6")
    text.grid(row=i, column=j)
    text.insert(INSERT, col)

# Dictionary for storing the text widget
# references
cells = {}

# adding all the other rows into the grid
for i in range(n_rows):
    for j in range(n_cols):
        text = Text(window, width=16, height=1)
        text.grid(row=i + 1, column=j)
        text.insert(INSERT, 10)
        cells[(i, j)] = text


def do_something():
    """
    When user clicks the "Save" button, modified data
    will be saved in excel file
    """
    print(cells)
    for i in range(n_rows):
        for j in range(n_cols):
            strVal = cells[(i, j)].get("1.0",'end-1c')
            val = float(strVal)  # TODO bug fix this shit
            print(val)

    """
    for i in range(n_rows):
        for j in range(n_cols):
            if df.loc[i][j] != cells[(i, j)].get("1.0", "end-1c"):
                df.loc[[i], column_names[j]] = cells[(i, j)].get("1.0", "end-1c")
    df.to_excel("new_data.xlsx")
    """


save_button = Button(
    window, height=2,
    width=16,
    text="Save",
    command=lambda: do_something())
save_button.grid(row=7, column=0)
window.mainloop()