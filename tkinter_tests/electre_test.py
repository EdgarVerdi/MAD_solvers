import re
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np


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


class Electre(tk.Widget):
    LABEL_TXT_HOW_MANY_ROWS = "How many Rows and Columns?"
    BUTTON_TXT_CREATE_TABLE = "Create Table"
    BUTTON_TXT_IMPORT_CLIPBOARD = "Import Table from Clipboard"

    COLOR_TEXT_ROWS = "#A0A0A0"
    COLOR_TEXT_ROWS2 = "#C0C0C0"

    def __init__(self, mainWindow: tk.Tk, frame: tk.Frame | None = None):
        """

        :param mainWindow: The main window for the tkinter to use.
        :param frame: The frame the trident displayer will be set on. If none then the main window will be used.
        """
        self.mainWindow: tk.Tk = mainWindow
        self.mainFrame: tk.Tk | tk.Frame = mainWindow if frame is None else frame
        # self.mainFrame = tk.Toplevel(self.mainFrame)

        # self.scrollbar = tk.Scrollbar(self.mainFrame, orient="vertical")

        rowsQuestionFrame: tk.Frame = tk.Frame(self.mainFrame)
        rowsQuestionFrame.grid(row=0, column=0)
        tk.Label(rowsQuestionFrame, text=self.LABEL_TXT_HOW_MANY_ROWS).grid(row=0, column=0)
        self.numberOfRowsRequested: tk.StringVar = tk.StringVar()
        self.numberOfRowsRequested.set("1")
        self.numberOfColumnsRequested: tk.StringVar = tk.StringVar()
        self.numberOfColumnsRequested.set("1")
        tk.Entry(rowsQuestionFrame, textvariable=self.numberOfRowsRequested).grid(row=0, column=1)
        tk.Entry(rowsQuestionFrame, textvariable=self.numberOfColumnsRequested).grid(row=0, column=2)
        self.numberOfRowsInUse: int = 0
        self.numberOfColumnsInUse: int = 0

        self.tableFrame: tk.Frame = tk.Frame(self.mainFrame)
        self.tableFrame.grid(row=1, column=0)
        self.cells: dict[tuple[int, int], tk.Text] = {}
        self.limitsAndProbs: dict[tuple[int, int], tk.Text] = {}

        createTableButton: tk.Button = tk.Button(
            rowsQuestionFrame, text=self.BUTTON_TXT_CREATE_TABLE, command=self.genNewTableFunc
        )
        createTableButton.grid(row=1, column=0)

        importTableButton: tk.Button = tk.Button(
            rowsQuestionFrame, text=self.BUTTON_TXT_IMPORT_CLIPBOARD, command=self.putFromClipBoardFunc
        )
        importTableButton.grid(row=1, column=1)

    def putFromClipBoardFunc(self):
        clip = self.mainWindow.clipboard_get().strip("\n")
        line = [[float(f) for f in re.findall("(\-?\d+\.\d|\-?\d+)", l)] for l in clip.split("\n")]
        for i, l in enumerate(line):
            if i < 4:
                for j, f in zip(range(self.numberOfColumnsInUse), l):
                    text = self.limitsAndProbs[(i, j)]
                    text.delete(1.0, tk.END)
                    text.insert(tk.END, f)
            else:
                for j, f in zip(range(self.numberOfColumnsInUse), l):
                    text = self.cells[(i - 4, j + 1)]
                    text.delete(1.0, tk.END)
                    text.insert(tk.END, f)

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

    def getValFromLimitsCell(self, i, j):
        return self.limitsAndProbs[(i, j)].get("1.0", 'end-1c')

    def genNewTableFunc(self):
        oldNumberOfRowsInUse = self.numberOfRowsInUse
        self.numberOfRowsInUse = self.numberOfRowsRequested.get()
        self.numberOfRowsInUse = int(self.numberOfRowsInUse) if self.numberOfRowsInUse != '' else 0

        oldNumberOfColumnsInUse = self.numberOfColumnsInUse
        self.numberOfColumnsInUse = self.numberOfColumnsRequested.get()
        self.numberOfColumnsInUse = int(self.numberOfColumnsInUse) if self.numberOfColumnsInUse != '' else 0
        sep = 5

        for i, v in enumerate("Ivpq"):
            text = tk.Text(self.tableFrame, width=16, height=1, bg=self.COLOR_TEXT_ROWS)
            text.insert(tk.INSERT, v)
            text.grid(row=i, column=0)
            for j in range(self.numberOfColumnsInUse):
                text = self.limitsAndProbs.get((i, j), None)
                if text is None:
                    text = tk.Text(self.tableFrame, width=16, height=1)
                    text.insert(tk.INSERT, "0")
                    self.limitsAndProbs[(i, j)] = text
                text.grid(row=i, column=j + 1)

        for i in range(self.numberOfRowsInUse):
            text = self.cells.get((i, 0), None)
            if text is None:
                text = tk.Text(self.tableFrame, width=16, height=1, bg=self.COLOR_TEXT_ROWS2)
                text.insert(tk.INSERT, self.excel_col(i))
                self.cells[(i, 0)] = text
            text.grid(row=i + sep, column=0)

            for j in range(self.numberOfColumnsInUse):
                text = self.cells.get((i, j + 1), None)
                if text is None:
                    text = tk.Text(self.tableFrame, width=16, height=1)
                    text.insert(tk.INSERT, "0")
                    self.cells[(i, j + 1)] = text
                text.grid(row=i + sep, column=j + 1)

        print(self.matrixOfCells())
        self.calcOthers()

    def matrixOfCells(self):
        return [
            [
                float(self.getValFromCell(i, j + 1))
                for j in range(self.numberOfColumnsInUse)
            ]
            for i in range(self.numberOfRowsInUse)
        ]

    def getRelationValue(self, v1, v2, j):
        diff = v1 - v2
        sign = self.sign(diff)
        diff = abs(diff)
        if diff <= float(self.getValFromLimitsCell(3, j)):
            num = 0
        elif diff < float(self.getValFromLimitsCell(2, j)):
            num = 1
        elif diff < float(self.getValFromLimitsCell(1, j)):
            num = 2
        else:
            num = 3
        return sign * num

    def sign(self, v):
        if v > 0:
            return 1
        elif v < 0:
            return -1
        else:
            return 0

    def calcOthers(self):
        matCells = self.matrixOfCells()
        relValueTensor = [
            [
                [
                    self.getRelationValue(matCells[i][j], matCells[i2][j], j)
                    for i2 in range(self.numberOfRowsInUse)
                ]
                for i in range(self.numberOfRowsInUse)
            ]
            for j in range(self.numberOfColumnsInUse)
        ]
        for j in range(self.numberOfColumnsInUse):
            frame = self.frameOfMatrix(relValueTensor[j], self.mainFrame)
            frame.config(borderwidth=4)
            frame.grid(row=2, column=j)

        cell_names = [self.getValFromCell(i, 0) for i in range(self.numberOfRowsInUse)]
        vals = "IQPV"
        rulesFrame = tk.Frame(self.mainFrame)
        print(relValueTensor)
        for j in range(self.numberOfColumnsInUse):
            print(j)
            rulesText = ""
            for i1 in range(self.numberOfRowsInUse):
                for i2 in range(self.numberOfRowsInUse):
                    if i1 < i2:
                        v = relValueTensor[j][i1][i2]
                        sign = self.sign(v)
                        v = vals[abs(v)]
                        a, b = cell_names[i1], cell_names[i2]
                        if sign < 0:
                            a, b = b, a
                        rulesText += f" {a}{v}{b}"
            width = 2*self.numberOfRowsInUse*(self.numberOfRowsInUse - 1)
            rules = tk.Text(rulesFrame, height=1, width=width)
            rules.insert(tk.INSERT, rulesText[1:])
            rules.grid(row=j, column=0)
        rulesFrame.grid(row=3, column=0)




        concs: list[list[list[float]]] = []
        for j in range(self.numberOfColumnsInUse):
            concJ: list[list[float]] = [
                [
                    self.concordanceValue(ia, ib, matCells, relValueTensor[j], j)
                    for ia in range(self.numberOfRowsInUse)
                ]
                for ib in range(self.numberOfRowsInUse)
            ]
            concs.append(concJ)
            frame = self.frameOfMatrix(concJ, self.mainFrame)
            frame.config(borderwidth=4)
            frame.grid(row=4, column=j)

        importances: list[float] = [float(self.getValFromLimitsCell(0, j)) for j in range(self.numberOfColumnsInUse)]
        totalImp = sum(importances)
        conc: list[list[float]] = [
            [
                sum([
                    importances[j] * concs[j][i1][i2]
                    for j in range(self.numberOfColumnsInUse)
                ]) / totalImp
                for i2 in range(self.numberOfRowsInUse)
            ] for i1 in range(self.numberOfRowsInUse)
        ]
        frame = self.frameOfMatrix(conc, self.mainFrame)
        frame.config(borderwidth=4)
        frame.grid(row=5, column=0)

        discs: list[list[list[float]]] = []
        for j in range(self.numberOfColumnsInUse):
            discJ: list[list[float]] = [
                [
                    self.discordanceValue(ia, ib, matCells, relValueTensor[j], j)
                    for ia in range(self.numberOfRowsInUse)
                ]
                for ib in range(self.numberOfRowsInUse)
            ]
            discs.append(discJ)
            frame = self.frameOfMatrix(discJ, self.mainFrame)
            frame.config(borderwidth=4)
            frame.grid(row=6, column=j)

        disc = []
        for i1 in range(self.numberOfRowsInUse):
            line = []
            for i2 in range(self.numberOfRowsInUse):
                isBigger = []
                for j in range(self.numberOfColumnsInUse):
                    if discs[j][i1][i2] > conc[i1][i2]:
                        isBigger.append(j)
                val = conc[i1][i2]
                for j in isBigger:
                    val *= (1 - discs[j][i1][i2]) / (1 - conc[i1][i2])
                line.append(val)
            disc.append(line)

        frame = self.frameOfMatrix(disc, self.mainFrame)
        frame.config(borderwidth=4)
        frame.grid(row=7, column=0)

    def concordanceValue(self, ia, ib, matCells, relValueMatrix, j):
        if relValueMatrix[ia][ib] <= 0:
            return 1
        elif relValueMatrix[ia][ib] >= 2:
            return 0
        else:
            return (
                    float(self.getValFromLimitsCell(2, j)) + matCells[ib][j] - matCells[ia][j]
            ) / (
                    float(self.getValFromLimitsCell(2, j)) - float(self.getValFromLimitsCell(3, j))
            )

    def discordanceValue(self, ia, ib, matCells, relValueMatrix, j):
        if relValueMatrix[ia][ib] <= 2:
            return 0
        elif relValueMatrix[ia][ib] >= 3:
            return 1
        else:
            return (
                    matCells[ib][j] - matCells[ia][j] - float(self.getValFromLimitsCell(2, j))
            ) / (
                    float(self.getValFromLimitsCell(1, j)) - float(self.getValFromLimitsCell(1, j))
            )

    def frameOfMatrix(self, matrix, fatherFrame):
        """

        :param matrix: The matrix to be framed
        :param fatherFrame: An empty frame to be filled
        :return: the frame that was generated
        """
        frame = tk.Frame(fatherFrame, width=1, height=1)
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            for j in range(cols):
                cell = tk.Text(frame, width=7, height=1)
                cell.insert(tk.INSERT, matrix[i][j])
                cell.grid(row=i, column=j)
        return frame


window = tk.Tk()
window.geometry("600x800")
Electre(window)
window.mainloop()
