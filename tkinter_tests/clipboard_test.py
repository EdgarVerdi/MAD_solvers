import tkinter as tk

root = tk.Tk()
text = tk.Text(height=6)
text.pack(side="top", fill="x")

for i in range(10):
    text.insert("end", "this is line #%d\n" % i)

entrys = []
for i in range(10):
    entry = tk.Entry(root)
    entry.pack(side="top", fill="x")
    entrys.append(entry)

def handle_clipboard(event):
    for entry in entrys:
        entry.delete(0, "end")

    lines = root.clipboard_get().split("\n")
    for entry, line in zip(entrys, lines):
        entry.insert(0, line)
    return "break"

root.bind_all("<<Paste>>", handle_clipboard)

root.mainloop()