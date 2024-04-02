import re
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure
import numpy as np


class TridentWidget(tk.Widget):
    LABEL_TXT_HOW_MANY_ROWS = "How many Rows?"
    LABEL_TXT_EDGE_LINE = "max"
    BUTTON_TXT_CREATE_TABLE = "Create Table"
    BUTTON_TXT_IMPORT_CLIPBOARD = "Import Table from Clipboard"
    BUTTON_TXT_EXPORT_CLIPBOARD = "Export Table to Clipboard"
    BUTTON_TXT_PLOT = "Plot"
    BUTTON_TXT_EXPORT_DESMOS = "Export to Desmos Equations"

    COLOR_TEXT_ROWS = "#A0A0A0"
    COLOR_EDGE_LINE = "black"

    def __init__(self, mainWindow: tk.Tk, frame: tk.Frame | None = None):
        """

        :param mainWindow: The main window for the tkinter to use.
        :param frame: The frame the trident displayer will be set on. If none then the main window will be used.
        """
        '''
        # Class Variables
        - mainWindow: : tk.Tk
        - mainFrame: tk.Tk | tk.Frame
        - rowsQuestionFrame, tableFrame, canvasFrame: tk.Frame
        - numberOfRowsRequested: StringVar
        - numberOfRowsInUse: int
        - cells: dict[tuple[int, int], tk.Text]
        
        # Local Variables
        - createTableButton, importTableButton, exportTableButton
          plotButton, desmosButtonFrame: tk.Button
        '''

        self.mainWindow: tk.Tk = mainWindow
        self.mainFrame: tk.Tk | tk.Frame = mainWindow if frame is None else frame
        self.rowsQuestionFrame: tk.Frame = tk.Frame(self.mainFrame)
        self.rowsQuestionFrame.grid(row=0, column=0)
        tk.Label(self.rowsQuestionFrame, text=self.LABEL_TXT_HOW_MANY_ROWS).grid(row=0, column=0)
        self.numberOfRowsRequested: tk.StringVar = tk.StringVar()
        tk.Entry(self.rowsQuestionFrame, textvariable=self.numberOfRowsRequested).grid(row=0, column=1)
        self.numberOfRowsInUse: int = 0

        self.tableFrame: tk.Frame = tk.Frame(self.mainFrame)
        self.tableFrame.grid(row=1, column=0)
        self.cells: dict[tuple[int, int], tk.Text] = {}

        self.canvasFrame: tk.Frame = tk.Frame(self.mainFrame)
        self.canvasFrame.grid(row=3, column=0)

        createTableButton: tk.Button = tk.Button(
            self.rowsQuestionFrame, text=self.BUTTON_TXT_CREATE_TABLE, command=self.genNewTableFunc
        )
        createTableButton.grid(row=1, column=0)

        importTableButton: tk.Button = tk.Button(
            self.rowsQuestionFrame, text=self.BUTTON_TXT_IMPORT_CLIPBOARD, command=self.putFromClipBoardFunc
        )
        importTableButton.grid(row=1, column=1)

        exportTableButton: tk.Button = tk.Button(
            self.rowsQuestionFrame, text=self.BUTTON_TXT_EXPORT_CLIPBOARD, command=self.exportTableToClipBoardFunc
        )
        exportTableButton.grid(row=1, column=2)

        self.equationValues: list[tuple[int, int, int, str, str]] = []

        buttonsFrame: tk.Frame = tk.Frame(self.mainFrame)
        buttonsFrame.grid(row=2, column=0)

        plotButton: tk.Button = tk.Button(buttonsFrame, text=self.BUTTON_TXT_PLOT, command=self.plotFunc)
        plotButton.grid(row=0, column=0)

        desmosButtonFrame: tk.Button = tk.Button(
            buttonsFrame, text=self.BUTTON_TXT_EXPORT_DESMOS, command=self.exportEquationsToDesmosFunc
        )
        desmosButtonFrame.grid(row=0, column=1)

    def excel_col(self, col):
        """
        Covert 0-relative column number to excel-style column label.
        inspired by: https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number
        """
        col += 1
        t = ''
        while col != 0:
            col, rem = divmod(col - 1, 26)
            t = chr(rem + ord('A')) + t
        return t

    def getValFromCell(self, i, j):
        return self.cells[(i, j)].get("1.0", 'end-1c')

    def putInClipBoard(self, s: str):
        self.mainWindow.clipboard_append(s)

    def genEquationValues(self) -> list[tuple[int, int, int, str, str]]:
        # sorry for the one-liner but it just felt way more efficient than append xD
        try:
            variableEq = [
                np.asarray([A - C, B - C, C])
                for A, B, C
                in [
                    tuple([
                        float(self.getValFromCell(i, j)) for j in range(1, 4)
                    ]) for i in range(self.numberOfRowsInUse)
                ]
            ]
        except ValueError:
            raise ValueError  # TODO better error here

        self.equationValues = [
            (y, x, c, i1, i2)
            for (y, x, c), i1, i2
            in [
                (a - b, idx, idy)
                for idx, a in enumerate(variableEq)
                for idy, b in enumerate(variableEq[idx + 1:], idx + 1)
            ]
            if y != 0
        ]
        return self.equationValues

    def genNewTableFunc(self):
        oldNumberOfRowsInUse = self.numberOfRowsInUse
        self.numberOfRowsInUse = self.numberOfRowsRequested.get()
        self.numberOfRowsInUse = int(self.numberOfRowsInUse) if self.numberOfRowsInUse != '' else 0

        # less rows
        for i in range(self.numberOfRowsInUse, oldNumberOfRowsInUse):
            for j in range(0, 4):
                text = self.cells[(i, j)]
                text.grid_forget()

        # more rows
        for i in range(oldNumberOfRowsInUse, self.numberOfRowsInUse):
            # putting the Text Cell
            text = self.cells.get((i, 0), None)
            if text is None:
                text = tk.Text(self.tableFrame, width=16, height=1, bg=self.COLOR_TEXT_ROWS)
                text.insert(tk.INSERT, self.excel_col(i))
                self.cells[(i, 0)] = text
            text.grid(row=i + 1, column=0)

            # putting the Value Cells
            for j in range(1, 4):
                text = self.cells.get((i, j), None)
                if text is None:
                    text = tk.Text(self.tableFrame, width=16, height=1)
                    text.insert(tk.INSERT, "0")
                    self.cells[(i, j)] = text
                text.grid(row=i + 1, column=j)

    def putFromClipBoardFunc(self):
        clip = self.mainWindow.clipboard_get().strip("\n")
        line = [[float(f) for f in re.findall("(\d+\.\d|\d+)", l)] for l in clip.split("\n")]
        for i, l in enumerate(line):
            for j, f in zip(range(1, 4), l):
                text = self.cells[(i, j)]
                text.delete(1.0, tk.END)
                text.insert(tk.END, f)

    def plotFunc(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 1, .01)
        t2 = np.arange(1, 0, -.01)
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        sub = fig.add_subplot(111)
        sub.plot(t, t2, label=self.LABEL_TXT_EDGE_LINE, color=self.COLOR_EDGE_LINE)

        cell_names = [self.getValFromCell(i, 0) for i in range(self.numberOfRowsInUse)]
        for (y, x, c, i1, i2) in self.genEquationValues():
            sub.plot(t, -(x * t + c) / y, label=f"{cell_names[i1]}_{cell_names[i2]}")

        sub.set_xlim([0, 1])
        sub.set_ylim([0, 1])

        for widget in self.canvasFrame.winfo_children():
            widget.destroy()  # clean previous canvas

        canvas = FigureCanvasTkAgg(fig, master=self.canvasFrame)  # A tk.DrawingArea.
        sub.legend()
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.canvasFrame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def exportEquationsToDesmosFunc(self):
        cell_names = [self.getValFromCell(i, 0) for i in range(self.numberOfRowsInUse)]
        self.putInClipBoard("\n".join([
            f"f_{{{cell_names[i1]}{cell_names[i2]}}}(x) = \\frac{{{x}x + {c}}}{{{-y}}}"
            for (y, x, c, i1, i2) in self.equationValues
        ]))

    def exportTableToClipBoardFunc(self):
        self.putInClipBoard("\n".join([
            "\t".join([
                self.getValFromCell(i, j) for j in range(1, 4)
            ]) for i in range(self.numberOfRowsInUse)
        ]))


if __name__ == '__main__':
    # This code won't run if this file is imported.
    window = tk.Tk()
    window.geometry("600x800")
    tridentDisplayer = TridentWidget(window)
    window.mainloop()
