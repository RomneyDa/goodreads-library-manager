import tkinter

mainWindow = tkinter.Tk()

button1 = tkinter.Button(text = "quit", command = mainWindow.destroy).pack()

mainWindow.mainloop()