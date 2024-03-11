import tkinter as tk

# --- functions ---

def generate():
    try:
        result = float(num1.get()) + float(num2.get())
    except Exception as ex:
        print(ex)
        result = 'error'

    num3.set(result)

# --- main ---

root = tk.Tk()

num1 = tk.StringVar()
num2 = tk.StringVar()
num3 = tk.StringVar()
frame = tk.Frame(root)
tk.Label(frame, text="Number 1:").grid(row=0, column=0)
tk.Label(frame, text="Number 2:").grid(row=1, column=0)
tk.Label(frame, text="Number 3:").grid(row=2, column=0)
tk.Label(frame, text="Number 4:").grid(row=3, column=0)



tk.Entry(frame, textvariable=num1).grid(row=0, column=1)
frame.grid(row=0, column=0)

def func():
    frame.grid_forget()

button = tk.Button(root, text="Calculate", command=func)
button.grid(row=3, column=1)

root.mainloop()