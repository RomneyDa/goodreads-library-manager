# This is the main gui code for the goodreads project
import tkinter

window = tkinter.Tk()



#
window.title('Goodreads Library')
window.geometry('350x200')

# Label
Label = tkinter.Label(window, text = 'Hello World!').pack()

L1 = Label(window, text = "Dallin's first label", font = ("Arial Bold", 50))
L1.grid(column = 0, row = 0)

# Button

# Entry

# Combo Box

# Check Button

# Radio

# Scrolled Text

# Spin Box

# Menu Bar

# Notebook

# TO START THE GUI
window.mainloop()