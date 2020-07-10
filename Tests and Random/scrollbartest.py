import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
yscrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
xscrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window = scrollable_frame, anchor="nw")

canvas.configure(xscrollcommand = xscrollbar.set)
canvas.configure(yscrollcommand = yscrollbar.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

tk.Grid.columnconfigure(root, 0, weight = 1)
tk.Grid.rowconfigure(root, 0, weight = 1)

tk.Grid.columnconfigure(container, 0, weight = 1)
tk.Grid.columnconfigure(container, 1, weight = 0)
tk.Grid.rowconfigure(container, 0, weight = 1)
tk.Grid.rowconfigure(container, 1, weight = 0)


container.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
canvas.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
xscrollbar.grid(row = 1, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
yscrollbar.grid(row = 0, column = 1,sticky = tk.N+tk.S+tk.E+tk.W)

#container.pack(fill = tk.BOTH, expand = True)
#xscrollbar.pack(side="bottom", fill = "x")
#canvas.pack(side="left", fill="both", expand=True)
#yscrollbar.pack(side="right", fill="y")


root.mainloop()