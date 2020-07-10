import tkinter as tk
import json
from tkinter import messagebox
import tkinter.ttk as ttk

class MainGUI:
    
    # STYLES
    #button_style = ttk.Style()
    #button_style.configure("button.TButton", foreground = "red", background = "black")
    #title_style = ttk.Style()
    #title_style.configure("title.TLabel", font = ("Helvetica", 16))
    #label_style = ttk.Style()
    #label_style.configure("label.TLabel", foreground = "black")
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.geometry("400x400")
        self.parent.title("Goodreads Library Manager")
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseApp)
        self.frame = tk.Frame(self.parent)       
        
        self.style = ttk.Style()
        self.style.configure("button.TButton", foreground = "red", background = "black")
        self.style.configure("title.TLabel", foreground = "blue")
        
        self.bg = 'black'
        self.fg = 'red'
        self.tit = ("Helvetica", 16)
        
        self.title_label = ttk.Label(self.frame, text = 'Goodreads Library Manager', style = "title.TLabel")
        self.user_label      = ttk.Label(self.frame, text = 'Hello')
        self.settings_button = ttk.Button(self.frame, text = 'Settings', command = lambda: self.Open(Settings), style = "button.TButton")
        self.quit_button     = ttk.Button(self.frame, text = 'Quit',     command = self.CloseApp              )#, style = "button.TButton")
        
        self.title_label.pack()
        self.user_label.pack()
        self.settings_button.pack()
        self.quit_button.pack()        

        self.frame.pack()
        
    def CloseApp(self):
        self.parent.destroy()

    def Open(self, window):
        self.newTopLevel = tk.Toplevel(self.parent)
        window(self.newTopLevel, self)   
        
    def NonFatal(self, message):
        messagebox.showinfo('Message', message)
        
    def Fatal(self, message):
        messagebox.showinfo('Fatal Error', message)
        self.parent.destroy()
    
        
class Settings:
    def __init__(self, parent, main):
        self.main = main
        
        self.parent = parent
        self.parent.title('Settings')
        self.parent.grab_set()
        self.parent.geometry("200x400+200+200")
        self.parent.resizable(False, False)
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseSettings)
        
        self.frame = tk.Frame(self.parent)
        
        self.title_label = ttk.Label(self.frame, text = 'Settings')        
        self.quit_button = ttk.Button(self.frame, text = "Back", command = self.CloseSettings, style = "button.TButton")
        
        self.title_label.pack()
        self.quit_button.pack()
        
        self.frame.pack()
        
    def CloseSettings(self):
        self.parent.destroy()
        self.parent.grab_release()
        
    
root = tk.Tk()
app = MainGUI(root)
root.mainloop()

# CREDITS
# GUI Window Switching: https://pythonprogramming.altervista.org/create-more-windows-with-tkinter/