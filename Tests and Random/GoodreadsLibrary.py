# Dallin Romney
# Goodreads Library Organizer

import tkinter as tk
from tkinter import filedialog
import re
from SQLFunctions import csvtosqlite

mainWindow = tk.Tk()
mainWindow.title('Goodreads Library')
    
filename = 'goodreads_library_50.csv'
DBname = 'BOOKS.sqlite'
tablename = 'Library'


from tkinter import messagebox
def NonFatal(message):
    messagebox.showinfo('Nonfatal Error', message)
def Fatal(message):
    messagebox.showinfo('Fatal Error', message)
    mainWindow.destroy()
    
#cur.execute('SELECT id FROM Album WHERE title = ?'                        , (album, ))
#album_id = cur.fetchone()[0]
    
####################### SETTINGS ###########################
settingsFile = 'settings.dat'

# Default settings
defaultSettings = {
    'Fields':('Title', 'Author', 'My Rating', 'Date Read', 'Date Added'),
    'Colors':('Red', 'Yellow', 'Blue', 'Green')
}
settings = defaultSettings.copy()
headers = list(settings['Fields'])

# This attempts to read any settings from file as name followed by ': " and a tuple
# If it fails, then it simply writes the default settings above to a new file
try:
    with open(settingsFile, 'r') as SETTINGS:
        contents = SETTINGS.read()
        for setting in settings:
            settings[setting] = tuple(re.findall(setting + ': (.*?)\n', contents)[0].replace("', '", '|').replace("','", '|').replace("('", '').replace("')", '').split("|"))
except:
    with open(settingsFile, 'w+') as SETTINGS:
        for setting, values in settings.items():
            SETTINGS.write(setting + ': ' + str(values) + '\n')
        NonFatal('Settings file missing or incorrectly formatted. Defaults restored')

def GetFile():
    return filedialog.askopenfilename(initialdir = "/", title = "Select a CSV File", filetypes = (("Comma-Separated Value Files (.csv)","*.csv"), ))

def SaveFile():
    return tk.asksaveasfilename(initialdir = "/",title = "Choose Save Location",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

def NewDB():
    csvfile = GetFile();
    headers = csvtosqlite(csvfile, DBname, tablename)

    fieldDict = {headers[j]:{'val':tk.BooleanVar(), 'order':j} for j in range(len(headers))}

    ### Fields
    for field in settings['Fields']:
        try: fieldDict[field]['val'].set(True)
        except: NonFatal('The "' + field + '" field doesn\'t exist in the CSV file. Check the settings.dat file or the CSV.')

#################################################################


def OpenSettings():
    settingsWindow = tk.Toplevel(mainWindow)
    def CloseSettings():
        with open(settingsFile, 'r') as SETTINGS:
            contents = SETTINGS.read()
        with open(settingsFile, 'w+') as SETTINGS:
            SETTINGS.write(re.sub('Fields: .*?\n', 'Fields: ' + str(tuple([key for key, val in fieldDict.items() if val['val'].get() == True])) + '\n', contents))
            settingsWindow.destroy()
            
    tk.Button(settingsWindow, text = 'Back', command = CloseSettings).grid(row = 1, column = 0)
    tk.Label(settingsWindow, text  ='Settings').grid(row = 0, column = 0)
    [tk.Checkbutton(settingsWindow, text = key, var = val['val']).grid(column = 1, row = val['order'], sticky = tk.W) for key, val in field.items()]


######################### MAIN GUI ################################

mainTitle = tk.Label(mainWindow, text = 'Goodreads Library').grid(row = 0, column = 0)
toSettings = tk.Button(mainWindow, text = 'Settings', command = OpenSettings).grid(row = 1, column = 0)


# Scrolled Text
def updateBools():
    scrolledText1.insert(tk.INSERT, str([val['val'].get() for key, val in fieldDict.items()]))
    #scrolledText1.insert(tk.INSERT, str(mainCheck.get()))
    
import tkinter.scrolledtext as ST
scrolledText1 = ST.ScrolledText(mainWindow, width = 40, height = 10)
scrolledText1.grid(column = 0, row = 2)
tk.Button(mainWindow, text = 'Update', command = updateBools).grid(row = 3, column = 0)

mainCheck = tk.BooleanVar()

tk.Checkbutton(mainWindow, text = 'Test', var = mainCheck).grid(column = 0, row = 4)
             
# Buttons
#def B1clicked():
#    if textBox1.get() == '': txt = 'Nothing'
#    else: txt = textBox1.get()
#    Label1.configure(text = 'You typed ' + txt)
    
#Button1 = TK.Button(bottom_frame, text="Click Me", command=B1clicked)
#Button1.grid(column = 0, row = 1)

### SETTINGS - 
# Check Button

#CBperframe = 10
#numFrames = ceil(len(headerDict)/CBperframe)

#for cb in checkButtons
# Entry
#textBox1 = tk.Entry(bottom_frame, width = 10).grid(column = 0, row = 2)


    

openFileButton = tk.Button(mainWindow, text = "Load New Database", command = NewDB).grid(row = 9, column = 0)
quitButton = tk.Button(mainWindow, text = "Quit", command = mainWindow.destroy).grid(row = 10, column = 0)

mainWindow.mainloop()



