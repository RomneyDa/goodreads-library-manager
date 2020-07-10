# Dallin Romney
# Goodreads Library

import json
import tkinter as tk

# Default Settings
settings_filename = "settings.json"

default_settings = '''{
        "users" : 0,
        "show_fields": ["Title", "Author", "My Rating", "Date Read", "Date Added"]
}'''
DBname = 'BOOKS.sqlite'
tablename = 'Library'

# Attempt to open settings file with json lib
try:
    with open(settings_filename, 'r') as sfile:
        contents = sfile.read()
        settings = json.loads(contents)
        
# If that fails, write the default settings to the settings file in json format
except:
    print("Invalid Settings File. Rewriting...")
    settings = json.loads(default_settings)
    
    with open(settings_filename, 'w') as sfile:
        json.dump(settings, sfile)


# Check for Users!
if settings["users"] == 0:
    #CreateUserGui()
    pass
else:
    # SelectUser
    pass

# =============================================================================
# class MainGUI():
#     def __init__():
#         main_window = tk.Tk()
#         
#         quit_button = tk.Button(text="Button", command = main_window.destroy)
#         quit_button.pack()
#         
#         main_window.mainloop()
#         
# 
# class CreateUserGUI():
#     def __init__():
#         tk.Toplevel(main_window)
#         
#         quit_button = tk.Button(text="Button", command = main_window.destroy)
#         quit_button.pack()
# 
# 
# =============================================================================
