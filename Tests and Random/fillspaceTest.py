import tkinter as tk

#Create & Configure root 
root = tk.Tk()
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

#Create & Configure frame 
frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

#Create a 5x10 (rows x columns) grid of buttons inside the frame
for row_index in range(5):
    tk.Grid.rowconfigure(frame, row_index, weight=1)
    for col_index in range(10):
        tk.Grid.columnconfigure(frame, col_index, weight=1)
        btn = tk.Button(frame) #create a button inside frame 
        btn.grid(row=row_index, column=col_index, sticky=tk.N+tk.S+tk.E+tk.W)  

a = {'a':1, 'b':2, 'c':3}

if 'v' in a:
    print('hello')

root.mainloop()
