import tkinter as tk

root = tk.Tk()
wa = root.clipboard_get().strip("\n")
print(wa)
a = [[float(f) for f in l.split("\t")] for l in wa.split("\n")]
print(a)
root.mainloop()
