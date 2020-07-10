# This is the main gui code for the goodreads project
import tkinter as TK

# Styles
S1 = {'fg':'black', 'bg':'green'}

# Window
window = TK.Tk()
window.title('Goodreads Library')
window.geometry('500x500')

# Frames
top_frame = TK.Frame(window)
bottom_frame = TK.Frame(window)

top_frame.pack(side = 'top')
bottom_frame.pack(side = 'bottom')

# Label
Label1 = TK.Label(top_frame, text="Dallin's first label", font = ("Arial Bold", 30), fg = S1['fg'], bg = S1['bg'])
Label1.grid(column = 0, row = 0)

# Buttons
def B1clicked():
    if textBox1.get() == '': txt = 'Nothing'
    else: txt = textBox1.get()
    Label1.configure(text = 'You typed ' + txt)
    
Button1 = TK.Button(bottom_frame, text="Click Me", command=B1clicked)
Button1.grid(column = 0, row = 1)

quitButton = TK.Button(bottom_frame, text="Quit", command=window.destroy)
quitButton.grid(column = 0, row = 12)

# Entry
textBox1 = TK.Entry(bottom_frame, width = 10)
textBox1.grid(column = 0, row = 2)

# Combo Box (Drop Down Menu) - Add options as a tuple
import tkinter.ttk as TTK
comboBox1 = TTK.Combobox(top_frame)
comboBox1['values'] = (1, 2, 3, 4, 5, "Hi")
comboBox1.current(3)
comboBox1.grid(column = 0, row = 3)

# Check Button
checkButtonState = TK.BooleanVar()
checkButtonState.set(True)

checkButton1 = TK.Checkbutton(top_frame, text = 'Select', var = checkButtonState)
checkButton1.grid(column = 0, row = 4)

# Radio buttons
radioButton1 = TK.Radiobutton(top_frame, text = 'Python', value = 1)
radioButton2 = TK.Radiobutton(top_frame, text = 'Python', value = 2)
radioButton3 = TK.Radiobutton(top_frame, text = 'Python', value = 3)

radioButton1.grid(column = 0, row = 5)
radioButton2.grid(column = 0, row = 6)
radioButton3.grid(column = 0, row = 7)

# Scrolled Text
import tkinter.scrolledtext as ST
scrolledText1 = ST.ScrolledText(top_frame, width = 40, height = 10)
scrolledText1.grid(column = 0, row = 8)
scrolledText1.insert(TK.INSERT,'Default Text')

# MessageBox
from tkinter import messagebox

def B2clicked():
    messagebox.showinfo('Message title', 'Message content')

Button2 = TK.Button(top_frame, text="MESSAGE", command=B2clicked)
Button2.grid(column = 0, row = 9)

# Spin Box (increment box)
spinBox1 = TK.Spinbox(top_frame, from_ = 0, to = 100, width = 5)
spinBox1.grid(column = 0, row = 10)

# USING EVENTS
def clickEvent(event):
    Label1.configure(text = 'You clicked on the button')
    
Button3 = TK.Button(bottom_frame, text = 'EVENT!')
Button3.grid(column = 0, row = 5)
Button3.bind('<Button-1>', clickEvent)

# Image
image1 = TK.PhotoImage(file = 'C:/pythontest/pngtest.png')
Label2 = TK.Label(bottom_frame, image = image1)
Label2.grid(column = 0, row = 4)
# Menu Bar

# Notebook

# 
# pack(block), grid(column, row) and place(coordinates) are used to arrange widgets


# TO START THE GUI
window.mainloop()

