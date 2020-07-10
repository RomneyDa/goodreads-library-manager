<<<<<<< HEAD
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install('pandas')
install('Pillow')
install('rauth')

import tkinter as tk
import json
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
import tkinter.ttk as ttk
import webbrowser
import re
import pandas as pd
import sqlite3
import os
import socket
from ClickableTable2 import ClickableTable2
import threading
import time
import queue
import urllib.request
import xml.etree.ElementTree as ET
import ssl
from SimpleScrollableFrameClam import SimpleScrollableFrame
from rauth.service import OAuth1Service, OAuth1Session
from PIL import Image, ImageTk # allows for image formats other than gif
from urllib.request import urlopen
import io

#testdf = pd.DataFrame(np.random.randint(0, 1000000, size=(50, 10)), columns=['A', 'BC', 'DEF', 'GHIJ', 'KLMNO', 'PQRS', 'TUV', 'WX', 'Y', 'Z'])
#testdf = pd.read_csv('TinySample.csv')
testdf = pd.read_csv('goodreads_library_50.csv')#.to_string()
numCols = ['Book Id', 'ISBN13', 'My Rating', 'Average Rating', 'Number of Pages', 'Year Published', 'Original Publication Year', 'Read Count', 'Owned Copies']
#testdf[numCols] = testdf[numCols].apply(pd.to_numeric)
testdf = testdf[['Title', 'Author', 'Publisher', 'Number of Pages']]
#testdf.drop(columns = ['Book Id', 'Author l-f', 'Additional Authors', 'ISBN13', 'Read Count', 'My Review', 'My Rating', 'Average Rating','Date Read', 'Date Added', 'Bookshelves', 'Bookshelves with positions', 'Binding','Exclusive Shelf', 'ISBN', 'Original Publication Year','Spoiler', 'Private Notes','Recommended For', 'Recommended By', 'Owned Copies', 'Original Purchase Date', 'Original Purchase Location', 'Condition', 'Condition Description', 'BCID'], inplace = True )


class MainGUI:

    settings_filename = "settings.json"
    noUser = "none"
    iconFilePath = 'bookicon.ico'
    goodreads_icon_filepath = 'GoodreadsIcon.png'

    default_settings = {
            "users" : {},
            "last_user" : "0",
            "show_fields": ["Title", "Author", "My Rating", "Date Read", "Date Added"],
            "dbname" : "GRLibrary.sqlite",
            "tbname" : "Library"
    }
    key = 'TNY6fDFILUDCTXZ739z56w'
    secret = 'k1CksvrhI3xOcTSDcQU9jCL2yw1HYYzft4fx9SRuB4'

    # display = wx.App(False) # the wx.App object must be created first.
    # display_size = print(wx.GetDisplaySize())  # returns a tuple
    # gr_image_size = int(display_size[0]/20)
    # del display
    gr_image_size = 50
    user_linked = False

    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(500, 350)
        self.parent.geometry("1000x500")
        self.parent.title("Library Manager")
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseApp)

        # FIRST: CHECK THE SETTINGS!
        self.CheckSettings()

        self.user_settings = {
                'style':{
                        'bg':'#F4F1EA',
                        'button':{'fg':'black',
                                  'bg':'white',
                                  'font':'Times',
                                  'size':12,
                                  'weight':'bold'},
                        'title':{'color':'black',
                                 'font':'Times',
                                 'size':17,
                                 'weight':'bold'},
                        'label':{'color':'black',
                                 'font':'Times',
                                 'size':11,
                                 'weight':'bold'}
                        }
        }

        self.styleObj = ttk.Style()
        s = self.user_settings['style']
        self.internetStatus = tk.StringVar()
        self.queue_delay = 500
        self.current_window = 'MainGUI'
        #self.styleObj.configure("button.TButton", highlightcolor = 'red', foreground = s['button']['fg'], background = s['button']['bg'], font = (s['button']['font'], s['button']['size'], s['button']['weight']))

        #362112 good color
        self.styleObj.theme_use('clam')
        self.styleObj.configure('button.TButton', font = (s['button']['font'], s['button']['size'], s['button']['weight']))
        self.styleObj.map('button.TButton', foreground=[('disabled', 'gray'),('pressed', 'black'), ('active', '#382110')], background=[('pressed', '!disabled', '#BAAC9A'), ('active', 'white')], bordercolor = [('active', '#382110')])
        self.styleObj.configure("title.TLabel", foreground = s['title']['color'], background = s['bg'], font = (s['title']['font'], s['title']['size'], s['title']['weight']))
        self.styleObj.configure("label.TLabel", foreground = s['label']['color'], background = s['bg'], font = (s['label']['font'], s['label']['size'], s['label']['weight']))
        self.styleObj.configure("error.TLabel", foreground = 'red', background = s['bg'], font = (s['label']['font'], s['label']['size'], s['label']['weight']))

        self.styleObj.configure("TFrame", background = s['bg'])
        self.styleObj.configure('cb.TCombobox', background = 'white', arrowsize = 25)
        self.parent.option_add("*TCombobox*Listbox*Font", font.Font(family="Times",size=12))
        self.parent.option_add("*TCombobox*Font", font.Font(family="Times",size=12))

        self.frame           = ttk.Frame(self.parent, style = 'TFrame')
        self.title_label     = ttk.Label(self.frame,  text = 'Library Manager', style = "title.TLabel")
        self.user_label      = ttk.Label(self.frame, style = "label.TLabel")
        self.gr_link         =  tk.Label(self.frame, height = self.gr_image_size, width = self.gr_image_size, cursor = 'hand1')
        self.gr_link.image   = ImageTk.PhotoImage(Image.open(self.goodreads_icon_filepath).resize((self.gr_image_size, self.gr_image_size)))
        self.gr_link.configure(image = self.gr_link.image)
        self.gr_link.bind('<Button-1>', self.open_goodreads)
        self.internet_status = ttk.Label(self.frame, style = "error.TLabel", textvariable = self.internetStatus)
        self.settings_button = ttk.Button(self.frame, text = 'Settings', command = lambda: self.Open(Settings), style = "button.TButton")
        self.db_button       = ttk.Button(self.frame, text = 'Manage Database', command = lambda: self.Open(ManageDatabase), style = "button.TButton")
        self.add_book_button = ttk.Button(self.frame, text = 'Add a Book', command = self.open_add_book, style = "button.TButton")
        self.user_button     = ttk.Button(self.frame, text = 'User',     command = lambda: self.Open(UserInfo), style = "button.TButton")
        self.online_button   = ttk.Button(self.frame, text = 'Online Stuff',     command = lambda: self.Open(OnlineStuff), style = "button.TButton")
        self.quit_button     = ttk.Button(self.frame, text = 'Quit',     command = self.CloseApp              , style = "button.TButton")
        self.table           = ClickableTable2(self.frame, df = testdf)#, editable = True)

        self.internet = False
        self.q = queue.Queue(maxsize = 1)
        self.check_internet = InternetThread(self)
        self.check_internet.start()
        self.check_queue()

        tk.Grid.columnconfigure(self.parent, 0, weight = 1)
        tk.Grid.rowconfigure(self.parent, 0, weight = 1)

        tk.Grid.columnconfigure(self.frame, 0, weight = 0)
        tk.Grid.columnconfigure(self.frame, 1, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 0, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 1, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 2, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 3, weight = 1)
        tk.Grid.rowconfigure(self.frame, 9, weight = 1)

        self.title_label.grid(row = 0, column = 0, columnspan = 2)
        self.gr_link.grid(row = 0, column = 1, sticky = tk.E)
        self.user_label.grid(row = 1, column = 0, sticky = tk.W, padx = 10, pady = 5)
        self.user_button.grid(row = 2, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.db_button.grid(row = 3, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.settings_button.grid(row = 4, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.add_book_button.grid(row = 5, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.online_button.grid(row = 6, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.internet_status.grid(row = 7, column = 0, sticky = tk.W, padx = 10, pady = 5)
        self.quit_button.grid(row = 10, column = 0, sticky = tk.S+tk.W+tk.E, padx = 10, pady = 10)
        self.table.grid(row = 1, rowspan = 10, column = 1, sticky = tk.N+tk.S+tk.E+tk.W, padx = 10, pady = 10)
        self.frame.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
        self.parent.iconbitmap(self.iconFilePath)

        # THEN: CHECK FOR USERS!
        if len(self.settings['users']) == 0:
            self.user = self.noUser
            self.UpdateUser()
            self.NonFatal('Welcome to Goodreads Library Manager. Create a User')
            self.Open(CreateEditUser, 'create')
        elif self.settings['last_user'] == '0':
            self.user = tuple(self.settings['users'].keys())[0]
            self.UpdateUser()
            self.Open(ManageUsers)
        elif self.settings['last_user'] not in self.settings['users'].keys():
            self.user = tuple(self.settings['users'].keys())[0]
            self.NonFatal('Last user not found in user list. Select existing user or create a new one.')
            self.UpdateUser()
            self.Open(ManageUsers)
        elif self.settings['last_user'] in self.settings['users'].keys():
            self.user = self.settings['last_user']
            self.UpdateUser()
            # LOAD THE DATABASE

        self.StartSession()

    def StartSession(self):
        if 'access_token' in self.settings['users'][self.user]:
            try:
                self.SubsequentSession()
            except:
                self.NewSession()
        else:
            ans = tk.messagebox.askquestion ('Link GoodReads', 'Do you want to connect to GoodReads?', icon = 'warning')
            if ans == 'yes':
                self.NewSession()
            else:
                self.user_linked = False
                return

    def NewSession(self):
        self.linker = OAuth1Service(
            consumer_key = self.key,
            consumer_secret = self.secret,
            #name = 'goodreads_link',
            request_token_url = 'https://www.goodreads.com/oauth/request_token',
            authorize_url = 'https://www.goodreads.com/oauth/authorize',
            access_token_url = 'https://www.goodreads.com/oauth/access_token',
            base_url = 'https://www.goodreads.com/'
        )
        request_token, request_token_secret = self.linker.get_request_token(header_auth = True)
        authorize_url = self.linker.get_authorize_url(request_token)
        webbrowser.open_new(authorize_url)

        ans = tk.messagebox.askquestion ('Waiting for Authorization', 'Have you authorized Library Manager in Goodreads?', icon = 'warning')

        self.user_linked = False
        while not self.user_linked:
            try:
                self.goodreads_link = self.linker.get_auth_session(request_token, request_token_secret)

                # Subsequent sessions
                self.settings['users'][self.user]['access_token'] = self.goodreads_link.access_token
                self.settings['users'][self.user]['access_token_secret'] = self.goodreads_link.access_token_secret
                self.user_linked = True
            except:
                ans = tk.messagebox.askretrycancel ('Authorization failed', 'Authorize the app in Goodreads and retry, or cancel.', icon = 'warning')
                if ans == True:
                    webbrowser.open_new(authorize_url)
                    continue
                else:
                    break

        del request_token, request_token_secret, authorize_url
        # if response.status_code != 201:
        #     raise Exception('Action failed: %s' % response.status_code)
        # else:
        #     print('Success!')

    def SubsequentSession(self):
        self.goodreads_link = OAuth1Session(
            consumer_key = self.key,
            consumer_secret = self.secret,
            access_token = self.settings['users'][self.user]['access_token'],
            access_token_secret = self.settings['users'][self.user]['access_token_secret'],
        )
        self.user_linked = True

    def CloseApp(self):
        try:
            self.settings['last_user'] = self.user
        except:
            print('Failed to update last user. No user exists')
        self.WriteSettings()
        self.check_internet.stop()
        self.parent.destroy()
        #quit()

    def open_goodreads(self, event):
        if self.internet:
            webbrowser.open_new('http://www.goodreads.com/')
        else:
            self.no_internet_msg()

    def open_add_book(self):
        if self.internet:
            self.Open(AddBook)
        else:
            self.no_internet_msg()

    def no_internet_msg(self):
        self.NonFatal('No Internet')

    def Open(self, window, *vargs):
        self.NewWindow = tk.Toplevel(self.parent)
        self.WindowObject = window(self.NewWindow, self, *vargs)
        self.current_window = re.findall("\.(.+)\'", str(window))[0]

    def Close(self):
        self.NewWindow.grab_release()
        self.NewWindow.destroy()
        self.current_window = 'MainGUI'

    def NonFatal(self, message):
        messagebox.showinfo('Message', message)

    def Fatal(self, message):
        messagebox.showinfo('Fatal Error', message)
        self.parent.destroy()

    def CheckSettings(self):
        # Attempt to open settings file with json lib
        try:
            with open(self.settings_filename, 'r') as sfile:
                contents = sfile.read()
                self.settings = json.loads(contents)
        # If that fails, write the default settings to the settings file in json format
        except:
            self.NonFatal("Invalid Settings File. Rewriting...")
            self.settings = self.default_settings

            self.WriteSettings()

    def UpdateUser(self):
        self.user_label.configure(text = 'User: ' + self.user)
        if self.user == self.noUser:
            self.user_label.configure(text = "No User Selected")

        if len(self.settings['users']) == 0:
            self.users = list(["No Users"])
        else:
            self.users = list(self.settings['users'].keys())

    def WriteSettings(self):
        with open(self.settings_filename, 'w') as sfile:
            json.dump(self.settings, sfile)

    def check_queue(self):
        if self.q.empty(): print('queue is empty')
        else:
            print('queue has', self.q.qsize(), 'items')
            self.internet = self.q.get()

            ### CONSTANT DEBUGGING
            print('User Linked', self.user_linked)
            #print(self.current_window)
            ###

            if self.internet:
                self.internetStatus.set('')
                self.styleObj.configure("link.TLabel", background = self.user_settings['style']['bg'], foreground = 'blue', font = ('Times', 11), cursor = 'hand2')
                self.add_book_button.configure(state = 'normal')
                if self.current_window == 'ManageDatabase':
                    self.WindowObject.new_db_button.configure(state = 'normal')
                if self.current_window == 'UserInfo':
                    if self.user != self.noUser and self.settings['users'][self.user]['site'] != '':
                        self.WindowObject.user_link.bind("<Button-1>", self.WindowObject.open_user_page)
                        self.WindowObject.user_link.grid(row = 3, column = 0, columnspan = 2)
            else:
                self.internetStatus.set('Internet is bad')
                self.styleObj.configure("link.TLabel", background = self.user_settings['style']['bg'], foreground = 'black', font = ('Times', 11), cursor = 'hand2')
                self.add_book_button.configure(state = 'disabled')
                if self.current_window == 'ManageDatabase':
                    self.WindowObject.new_db_button.configure(state = 'disabled')
                if self.current_window == 'UserInfo':
                    self.WindowObject.user_link.grid_forget()

        self.parent.after(self.queue_delay, self.check_queue)

class InternetThread (threading.Thread):
    delay = 3

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        print("Starting to check for internet")
        while self.running:
            self.CheckInternet()
            time.sleep(self.delay)

    def CheckInternet(self, host = "8.8.8.8", port = 53):
        # Checks google-public-dns-a.google.com for internet connection on 53/tcp
        try:
            socket.setdefaulttimeout(self.delay)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            self.parent.q.put(True)
        except:# socket.error as ex:
            self.parent.q.put(False)

class Settings:
    def __init__(self, parent, main):
        self.main = main

        self.parent = parent
        self.parent.title('Settings')
        self.parent.grab_set()
        self.parent.geometry("200x400+200+200")
        self.parent.resizable(False, False)
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseSettings)

        self.frame = ttk.Frame(self.parent, style = "TFrame")

        self.title_label = ttk.Label(self.frame, text = 'Settings', style = "title.TLabel")
        self.quit_button = ttk.Button(self.frame, text = "Back", command = self.CloseSettings, style = "button.TButton")

        self.title_label.pack()
        self.quit_button.pack()

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def CloseSettings(self):
        self.main.Close()

class UserInfo:
    def __init__(self, parent, main):
        self.main = main

        self.parent = parent
        self.parent.title('User Info')
        self.parent.grab_set()
        self.parent.protocol("WM_DELETE_WINDOW", self.parent.destroy)
        self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        if 'email' not in self.main.settings['users'][self.main.user]:
             self.main.settings['users'][self.main.user]['email'] = ''

        if 'site' not in self.main.settings['users'][self.main.user]:
             self.main.settings['users'][self.main.user]['site'] = ''

        self.title_label = ttk.Label(self.frame, text = 'User Info', style = 'title.TLabel')
        self.user_label = ttk.Label(self.frame, text = 'Name: ' + self.main.user, style = 'label.TLabel')
        self.user_link = ttk.Label(self.frame, text = "Profile on Goodreads", style = 'link.TLabel')
        self.email_label = ttk.Label(self.frame, text = 'Email: ' + self.main.settings['users'][self.main.user]['email'], style = 'label.TLabel')

        self.manage_button = ttk.Button(self.frame, text = 'Manage Users', command = self.OpenManageUsers, style = "button.TButton")
        self.quit_button = ttk.Button(self.frame, text = 'Back', command = self.parent.destroy, style = "button.TButton")

        self.title_label.grid(row = 0, column = 0, columnspan = 2)
        self.user_label.grid(row = 1, column = 0, columnspan = 2)

        if self.main.user != self.main.noUser and self.main.settings['users'][self.main.user]['email'] != '':
            self.email_label.grid(row = 2, column = 0, columnspan = 2)

        self.manage_button.grid(row = 4, column = 1, padx = 10, pady = 5)
        self.quit_button.grid(row = 4, column = 0, padx = 10, pady = 5)

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def OpenManageUsers(self):
        self.main.Close()
        self.main.Open(ManageUsers)

    def open_user_page(self, event):
        if self.main.internet:
            webbrowser.open_new('http://www.goodreads.com/' + self.main.settings['users'][self.main.user]['site'])

class ManageUsers:
    def __init__(self, parent, main):
        self.main = main

        self.parent = parent
        self.parent.grab_set()
        self.parent.title('Manage Users')
        #self.parent.geometry("200x200+200+200")
        self.parent.protocol("WM_DELETE_WINDOW", self.GoToUserInfo)
        self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        #self.title_label = ttk.Label(self.frame, text = 'Users', style = "title.TLabel")

        self.user_list_label = ttk.Label(self.frame, text = 'Select A User', style = "title.TLabel")
        self.user_list = ttk.Combobox(self.frame, state = 'readonly', style = 'cb.TCombobox')
        self.user_list.bind("<<ComboboxSelected>>", self.UserSelected)

        self.ResetUserList()

        self.switch_user_button = ttk.Button(self.frame, text = 'Switch To This User', command = self.SwitchUser, style = "button.TButton")
        self.edit_user_button = ttk.Button(self.frame, text = 'Edit This User', command = self.GoToEditUser, style = "button.TButton")
        self.create_user_button = ttk.Button(self.frame, text = 'Create New User', command = self.GoToCreateUser, style = "button.TButton")
        self.del_user_button = ttk.Button(self.frame, text = 'Delete This User', command = self.DeleteUser, style = "button.TButton")
        self.user_info_button = ttk.Button(self.frame, text = 'Back', command = self.GoToUserInfo, style = "button.TButton")
        self.quit_button = ttk.Button(self.frame, text ='Cancel', command = self.CloseManageUsers, style = "button.TButton")

        #self.title_label.grid(row = 0, column = 1)
        ttk.Frame(self.frame, height = 15).grid(row = 0, column = 0)
        self.user_list_label.grid(row = 1, column = 0, padx = 10, sticky = tk.W)
        self.user_list.grid(row = 2, column = 0, columnspan = 2, padx = 10, sticky = tk.W+tk.E)
        self.switch_user_button.grid(row = 1, column = 2, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.edit_user_button.grid(row = 2, column = 2, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.del_user_button.grid(row = 3, column = 2, padx = 10, pady = 2, sticky = tk.W+tk.E)
        ttk.Frame(self.frame, height = 50).grid(row = 4, column = 0)
        self.create_user_button.grid(row = 5, column = 2, padx = 10, pady = 10, sticky = tk.W+tk.E)
        self.user_info_button.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = tk.W+tk.E)
        self.quit_button.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = tk.W+tk.E)

        self.UserSelected(0)
        if self.main.user == self.main.noUser:
            self.user_info_button['state'] = 'disabled'

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)


    def DeleteUser(self):
        if len(self.main.settings['users']) == 0:
            self.main.NonFatal('There are no users to delete.')
        else:
            userToDel = str(self.user_list.get())
            if messagebox.askquestion('Delete User','Are you sure you want to delete ' + userToDel + '?', icon = 'warning') == 'yes':
                del[self.main.settings['users'][userToDel]]
                if len(self.main.settings['users']) == 0:
                    self.main.user = self.main.noUser
                else:
                    self.main.user = tuple(self.main.settings['users'].keys())[0]
                self.main.UpdateUser()
                self.ResetUserList()
            # else they said no so do nothing
            del userToDel
            self.UserSelected(0)

    def SwitchUser(self):
        self.main.user = self.user_list.get()
        self.main.WriteSettings()
        self.main.UpdateUser()
        self.main.StartSession()
        self.main.Close()

    def ResetUserList(self):
        if self.main.user == self.main.noUser:
            self.user_list['values'] = ('No Users',)
            self.user_list.current(0)
        else:
            self.user_list['values'] = tuple(self.main.users)
            self.user_list.current(self.main.users.index(self.main.user))

    def GoToUserInfo(self):
        self.main.Close()
        self.main.Open(UserInfo)

    def GoToCreateUser(self):
        self.main.Close()
        self.main.Open(CreateEditUser, 'create')

    def CloseManageUsers(self):
        self.main.Close()
        self.main.UpdateUser()

    def GoToEditUser(self):
        self.main.Close()
        self.main.Open(CreateEditUser, 'edit')

    def UserSelected(self, useless):
        self.main.selected_user = self.user_list.get()
        if self.main.selected_user == self.main.user or self.main.selected_user == 'No Users':
            self.switch_user_button['state'] = 'disabled'
        else:
            self.switch_user_button['state'] = 'enabled'
        if self.main.selected_user == 'No Users':
            self.edit_user_button['state'] = 'disabled'
            self.del_user_button['state'] = 'disabled'
        else:
            self.edit_user_button['state'] = 'enabled'
            self.del_user_button['state'] = 'enabled'

class CreateEditUser:
    def __init__(self, parent, main, state):
        self.main = main

        self.parent = parent
        self.parent.resizable(False, False)
        if state == 'create': self.parent.title('Create User')
        if state == 'edit': self.parent.title('Edit User')

        self.parent.grab_set()
        self.parent.protocol("WM_DELETE_WINDOW", self.BackToUsers)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        self.title_label = ttk.Label(self.frame, style = 'title.TLabel')
        if state == 'create': self.title_label.configure(text = 'Create New User')
        if state == 'edit':   self.title_label.configure(text = 'Edit User: ' + self.main.selected_user)

        self.name_label = ttk.Label(self.frame, style = "label.TLabel")
        if state == 'create': self.name_label.configure(text = 'Name (required)')
        if state == 'edit':   self.name_label.configure(text = 'New name (required)')
        self.name_entry = tk.Entry(self.frame, width = 20)

        self.email_label = ttk.Label(self.frame, style = "label.TLabel")
        if state == 'create': self.email_label.configure(text = 'Email: ')
        if state == 'edit':   self.email_label.configure(text = 'New email: ')
        self.email_entry = tk.Entry(self.frame, width = 20)

        self.site_label = ttk.Label(self.frame, style = "label.TLabel")
        if state == 'create': self.site_label.configure(text = 'Site: https://www.goodreads.com/')
        if state == 'edit':   self.site_label.configure(text = 'New site: https://www.goodreads.com/')
        self.site_entry = tk.Entry(self.frame, width = 20)

        if state == 'edit':
            self.name_entry.insert(0, self.main.selected_user)
            self.email_entry.insert(0, self.main.settings['users'][self.main.selected_user]['email'])
            self.site_entry.insert(0, self.main.settings['users'][self.main.selected_user]['site'])

        if state == 'create':
            self.make_button = ttk.Button(self.frame, text = 'Next', command = self.MakeUser, style = "button.TButton")
        if state == 'edit':
            self.make_button = ttk.Button(self.frame, text = 'Apply', command = self.MakeEdits, style = "button.TButton")

        self.quit_button = ttk.Button(self.frame, text = 'Back', command = self.BackToUsers, style = "button.TButton")

        self.title_label.grid(row = 0, columnspan = 4)
        self.name_label.grid(row = 1, column = 0, sticky = tk.E, pady = 5)
        self.name_entry.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.email_label.grid(row = 1, column = 2, sticky = tk.E, pady = 5)
        self.email_entry.grid(row = 1, column = 3, padx = 5, pady = 5)
        self.site_label.grid(row = 3, column = 0, columnspan = 2, sticky = tk.E, pady = 5)
        self.site_entry.grid(row = 3, column = 2, columnspan = 2, sticky = tk.W+tk.E, padx = 5, pady = 5)

        size = self.frame.grid_size()
        self.quit_button.grid(row = size[0], column = 0, sticky = tk.W, padx = 5, pady = 5)
        self.make_button.grid(row = size[0], column = size[1]-1, sticky = tk.E, padx = 5, pady = 5)
        self.frame.pack(fill = tk.BOTH, expand = True)
        del size

        self.parent.iconbitmap(self.main.iconFilePath)

    def MakeUser(self):

        name = self.name_entry.get()
        email = self.email_entry.get()
        site = self.site_entry.get()

        # Data verification
        if name == '':
            self.main.NonFatal('Name is required')
        elif name == 'No Users' or name == self.main.noUser:
            self.main.NonFatal("Name can't be '" + self.main.noUser + "' or 'No Users'")
        elif name in self.main.settings['users']:
            self.main.NonFatal('User already exists. Edit the existing user or delete and recreate it.')
        elif not (re.search('.+@.+\..+', email)) and email != '':
            self.main.NonFatal("Invalid email address.")
        else:
            # If data looks good, go ahead!
            self.main.settings['users'][name] = dict()
            self.main.settings['users'][name]['email'] = email
            self.main.settings['users'][name]['site']  = site

            self.main.user = name
            self.main.WriteSettings()
            self.main.UpdateUser()
            self.main.Close()

        del name, email, site

    def MakeEdits(self):

        name = self.name_entry.get()
        email = self.email_entry.get()
        site = self.site_entry.get()

        # Data verification
        if name == '':
            self.main.NonFatal('Name is required')
        elif name == 'No Users' or name == self.main.noUser:
            self.main.NonFatal("Name can't be '" + self.main.noUser + "' or 'No Users'")
        elif not (re.search('.+@.+\..+', email)) and email != '':
            self.main.NonFatal("Invalid email address.")
        elif name in self.main.settings['users'] and name != self.main.selected_user:
            self.main.NonFatal('New name for ' + self.main.selected_user + ' conflicts with existing user.')
        else:

            if name != self.main.selected_user: # If name changed, copy user settings to new name
                self.main.settings['users'][name] = self.main.settings['users'][self.main.selected_user]
                del self.main.settings['users'][self.main.selected_user]

            # Either way, update settings
            self.main.settings['users'][name]['email'] = email
            self.main.settings['users'][name]['site']  = site

            # If editing the current user, make sure to update user
            if self.main.selected_user == self.main.user:
                self.main.user = name
                self.main.UpdateUser()

            # Write settings and close
            self.main.WriteSettings()
            self.main.Close()
            self.main.Open(ManageUsers)

        del name, email, site

    def BackToUsers(self):
        self.main.Close()
        self.main.Open(ManageUsers)

class ManageDatabase:
    def __init__(self, parent, main):
        self.main = main
        self.parent = parent
        self.parent.grab_set()
        self.parent.title('Manage Database')
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseManageUsers)
        self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        self.title_label = ttk.Label(self.frame, text = 'Manage Database', style = "title.TLabel")



        #self.user_list_label = ttk.Label(self.frame, text = 'Select A User', style = "title.TLabel")
        #self.user_list = ttk.Combobox(self.frame, state = 'readonly', style = 'cb.TCombobox')
        #self.user_list.bind("<<ComboboxSelected>>", self.UserSelected)

        self.update_db_button  = ttk.Button(self.frame, text = 'Update Library',  command = lambda: print(self.update_file_val.get()),  style = "button.TButton")
        self.new_db_button = ttk.Button(self.frame, text = 'New Library', command = self.NewLibrary, style = "button.TButton")
        self.open_db_button = ttk.Button(self.frame, text = 'Open Library', command = lambda: print('Open Library'), style = "button.TButton")

        #self.edit_user_button = ttk.Button(self.frame, text = 'Edit This User', command = self.GoToEditUser, style = "button.TButton")
        #self.create_user_button = ttk.Button(self.frame, text = 'Create New User', command = self.GoToCreateUser, style = "button.TButton")
        #self.del_user_button = ttk.Button(self.frame, text = 'Delete This User', command = self.DeleteUser, style = "button.TButton")
        #self.user_info_button = ttk.Button(self.frame, text = 'Back', command = self.GoToUserInfo, style = "button.TButton")
        #self.quit_button = ttk.Button(self.frame, text ='Cancel', command = self.CloseManageUsers, style = "button.TButton")

        self.title_label.grid(row = 0, column = 0, columnspan = 3)
        self.update_db_button.grid(row = 1, column = 0, padx = 10, pady = 5)
        self.new_db_button.grid(row = 1, column = 1, padx = 10, pady = 5)
        self.open_db_button.grid(row = 1, column = 2, padx = 10, pady = 5)
        #self.UserSelected(0)
        #if self.main.user == self.main.noUser:
        #   self.user_info_button['state'] = 'disabled'

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def NewLibrary(self):
        #filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a CSV File", filetypes = (("Comma-Separated Value Files (.csv)","*.csv"), ))
        #filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select an SQLite database", filetypes = (("SQLite Databases (.sqlite)","*.sqlite"), ))

        filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a CSV or SQLite File", filetypes = (("Supported Files (.csv, .sqlite)",("*.csv", "*sqlite")),))#("SQLite Databases (.sqlite)","*.sqlite")))

        #print(self.replace_file_val.get())
        if re.search('^vsc.', filename[::-1]):
            print('This is a csv file. Loading', filename)
            del self.main.table
            self.main.table = ClickableTable2(self.main.frame, df = pd.read_csv(filename))#, editable = True)
            self.main.table.grid(row = 1, rowspan = 10, column = 1, sticky = tk.N+tk.S+tk.E+tk.W, padx = 10, pady = 10)
            self.CloseManageUsers()

        if re.search('^etilqs.', filename[::-1]):
            print('This is an sqlite file. Not supported yet')

    def CloseManageUsers(self):
        self.main.Close()

class DB():

    def __init__(self, main, _from, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()


        if _from == 'csv':
            self.csvtosqlite()

    def csvtosqlite(self, csvname, dbname, tablename):

        conn = sqlite3.connect(dbname) # Verify/open DB
        cur  = conn.cursor()           # Open connection to DB

        data = pd.read_csv(csvname)
        headers = list(data.columns.values)

        cur.execute('DROP TABLE IF EXISTS ' + tablename)
        cur.execute('CREATE TABLE ' + tablename + ' (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')

        valuesString = ' (' + str(headers).replace('[', '').replace(']', '').replace("'", '"') + ') '
        valuePlaceholders = 'VALUES(' + '?,'*(len(headers) - 1) + '?)'

        for column in headers:
            cur.execute('ALTER TABLE ' + tablename + ' ADD ' + "'" + column + "'" + ' TEXT')

        for i in range(len(data)):
            currentrow = list(data.loc[i])
            for j in range(len(currentrow)):
                if type(currentrow[j]) != str:
                    currentrow[j] = str(currentrow[j])

            cur.execute('INSERT INTO ' + tablename + valuesString + valuePlaceholders, tuple(currentrow))

        conn.commit()

        return headers

class OnlineStuff:

    def __init__(self, parent, main):
        self.main = main
        self.parent = parent
        self.parent.grab_set()
        self.parent.title('Online Stuff')
        self.parent.protocol("WM_DELETE_WINDOW", self.BackToMain)
        #self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        self.action_1_button = ttk.Button(self.frame, text = 'Add Book', command = self.AddBook, style = "button.TButton")
        self.action_2_button = ttk.Button(self.frame, text = 'Action 2', command = self.Action2, style = "button.TButton")
        self.action_3_button = ttk.Button(self.frame, text = 'Action 3', command = self.Action3, style = "button.TButton")
        self.action_4_button = ttk.Button(self.frame, text = 'Action 4', command = self.Action4, style = "button.TButton")
        self.action_5_button = ttk.Button(self.frame, text = 'Action 5', command = self.Action5, style = "button.TButton")
        self.quit_button = ttk.Button(self.frame, text ='Back', command = self.BackToMain, style = "button.TButton")

        #self.title_label.grid(row = 0, column = 1)
        self.action_1_button.grid(row = 1, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_2_button.grid(row = 2, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_3_button.grid(row = 3, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_4_button.grid(row = 4, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_5_button.grid(row = 5, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.quit_button.grid(row = 6, column = 0, padx = 10, pady = 10, sticky = tk.W+tk.E)

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def AddBook(self):
        print('Doing Action 1')
        #self.main.

    def Action2(self):
        print('Doing Action 2')

    def Action3(self):
        print('Doing Action 3')

    def Action4(self):
        print('Doing Action 4')

    def Action5(self):
        print('Doing Action 5')

    def BackToMain(self):
        self.main.Close()

class AddBook:
    # Goodreads API Keys
    def __init__(self, parent, main):
        self.parent = parent
        self.main = main
        self.parent.title('Add a Book')
        self.parent.grab_set()
        self.parent.protocol("WM_DELETE_WINDOW", self.BackToMain)

        self.results_list = list()

        self.container = tk.Frame(self.parent)
        self.results_area = SimpleScrollableFrame(self.container)
        self.results_area.frame.clicked = self.clicked

        self.title_label = tk.Label(self.container, text = 'ADD A BOOK', font = ('Times', 14, 'bold'))

        self.search_label = tk.Label(self.container, text = 'Enter search term: ', font = ('Times', 12))

        self.search_entry = tk.Entry(self.container)
        self.search_entry.bind("<Return>", self.search)

        self.search_button = tk.Button(self.container, text = 'Search', command = lambda: self.search(0))
        self.back_button = tk.Button(self.container, text = 'Back', command = self.BackToMain)

        self.ignore_ssl_errors()

        #self.xmloutput = open('query_results.xml', 'w+')

        # Configure all rows and columns present to have the same weight (so they expand with the window)
        tk.Grid.columnconfigure(self.parent, 0, weight = 1)
        tk.Grid.rowconfigure(self.parent, 0, weight = 1)
        tk.Grid.columnconfigure(self.container, 3, weight = 1)
        tk.Grid.rowconfigure(self.container, 2, weight = 1)

        # Add the frame and its elements
        self.title_label.grid(row = 0, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
        self.back_button.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.W, padx = 10, pady = 5)
        self.search_label.grid(row = 1, column = 0, sticky = tk.N+tk.E+tk.S+tk.W, pady = 5)
        self.search_entry.grid(row = 1, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 5)
        self.search_button.grid(row = 1, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, padx = 10, pady = 5)

        self.container.grid(row = 0, column = 0, sticky = tk.N+tk.E+tk.S+tk.W)

    def search(self, event):
        if not self.main.internet:
            self.main.no_internet_msg()
            self.BackToMain()

        for result in self.results_list:
            result.grid_forget()
            result.destroy()
        self.results_list = []

        self.search_term = str(self.search_entry.get())
        #self.search_entry.delete(0, tk.END)
        search_url = 'https://www.goodreads.com/search.xml?key='+self.main.key+'&'+urllib.parse.urlencode({'q':self.search_term})
        xmldata = urllib.request.urlopen(search_url).read().decode()

        #self.xmloutput.write(xmldata)

        # Pull book names
        tree = ET.fromstring(xmldata)
        books_outer = tree.findall('search/results/work')

        self.results_area.grid(row = 2, column = 0, columnspan = 4, sticky = 'NESW')

        try: # prevents errors if the user clicks before all the results are loaded

            if len(books_outer) == 0:
                self.results_list.append(tk.Label(self.results_area.frame, text = 'No Results', font = ('Times', 14, 'bold')))
                self.results_list[0].grid(row = 0)

            else:
                i = 0
                for book in books_outer:

                    book_inner = book.find('best_book')
                    author = book_inner.find('author')

                    bookinfo = dict()
                    bookinfo['Author'] = author.find('name').text
                    bookinfo['author_id'] = author.find('id').text

                    bookinfo['Book Id'] = book_inner.find('id').text
                    bookinfo['Title'] = book_inner.find('title').text
                    bookinfo['small_image_url'] = book_inner.find('small_image_url').text
                    bookinfo['image_url'] = book_inner.find('image_url').text

                    year = book.find('original_publication_year').text
                    month = book.find('original_publication_month').text
                    day = book.find('original_publication_day').text

                    months = {'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
                    date = ''
                    if month != None:
                        date += months[month] + ' '
                        if day != None:
                            date += day + ', '
                    if year != None:
                        date += year


                    #bookinfo['date'] = bookinfo['year'] + '-' + bookinfo['month'] + '-' + bookinfo['day']
                    bookinfo['date'] = date
                    bookinfo['Year Published'] = year
                    bookinfo['Original Publication Year'] = year

                    bookinfo['Average Rating'] = book.find('average_rating').text

                    self.results_list.append(BookResult(self.results_area.frame, bookinfo))
                    self.results_list[i].grid(row = i, column = 0, columnspan = 2, sticky = 'NESW')
                    self.results_area.frame.update()
                    i += 1
                    del bookinfo, author, book_inner, date, day

                del search_url, xmldata, tree, books_outer

        except:
            pass

    def ignore_ssl_errors(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    def clicked(self, bookinfo):
        self.main.lastbookadded = bookinfo
        self.main.table.add_row(bookinfo)
        #print('Adding ' + bookinfo['Title'] + ' to Table')
        self.parent.destroy()

    def BackToMain(self):
        self.main.Close()

class BookResult(tk.Frame):

    def __init__(self, parent, bookinfo):

        self.parent = parent
        self.bookinfo = bookinfo

        self.elems = dict()
        self.image_height = 75
        self.title_font = ('Times', 14, 'bold')
        self.author_font = ('Times', 12)
        self.other_font = ('Times', 10)

        self.incolor = '#BAAC9A'
        self.outcolor = 'white'

        tk.Frame.__init__(self, self.parent)
        self.configure(bg = self.outcolor)

        self.bind('<Button-1>', self.clicked)
        self.bind('<Enter>', self.entered)
        self.bind('<Leave>', self.exited)

        if 'image_height' in self.bookinfo:
            self.image_height = self.bookinfo['image_height']

        self.elems['Image'] = tk.Label(self, bd = 0, height = self.image_height)
        #self.elems['Image'].bind('<Button-1>', self.clicked)
        self.pic = self.get_image(self.bookinfo['small_image_url'])
        self.elems['Image'].configure(image = self.pic)


        self.elems['Title'] = tk.Label(self, text = self.bookinfo['Title']+' (ID: '+self.bookinfo['Book Id']+')', font = self.title_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Author'] = tk.Label(self, text = self.bookinfo['Author']+' (ID: '+self.bookinfo['author_id']+')', font = self.author_font, justify = tk.LEFT, bg = self.outcolor)

        self.elems['Date_Rating'] = tk.Label(self, font = self.other_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Date_Rating'].configure(text = 'Published: '+self.bookinfo['date']+';\t'+'Rating: '+self.bookinfo['Average Rating']+'/5')

        for element in self.elems:
            self.elems[element].bind('<Button-1>', self.clicked)

        self.elems['Image'].grid(row = 0, rowspan = 10, column = 0, sticky = 'NESW')
        self.elems['Title'].grid(row = 0, column = 1, columnspan = 2, sticky = 'NSW')
        self.elems['Author'].grid(row = 1, column = 1, sticky = 'NSW')
        self.elems['Date_Rating'].grid(row = 2, column = 1, sticky = 'NSW')

    def get_image(self, path):

        # Open as a PIL image object
        pil_image = Image.open(io.BytesIO(urlopen(path).read()))

        # Get size and resize
        (w, h) = pil_image.size
        pil_image = pil_image.resize((int(w*self.image_height/h), self.image_height))

        del w, h

        # convert PIL image object to Tkinter PhotoImage object
        return ImageTk.PhotoImage(pil_image)

    def clicked(self, event):
        try:
            self.parent.clicked(self.bookinfo)
        except:
            pass # Parent won't always have a clicked function

    def entered(self, event):
        #print('Entered', self.bookinfo['title'])
        self.configure(bg = self.incolor)
        for element in self.elems:
            self.elems[element].configure(bg = self.incolor)

    def exited(self, event):
        #print('Exited', self.bookinfo['title'])
        self.configure(bg = self.outcolor)
        for element in self.elems:
            self.elems[element].configure(bg = self.outcolor)


root = tk.Tk()
app = MainGUI(root)
root.mainloop()

# CREDITS
# GUI Window Switching: https://pythonprogramming.altervista.org/create-more-windows-with-tkinter/
=======
#import subprocess
#import sys
#
#def install(package):
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#install('pandas')
#install('Pillow')
#install('rauth')

import tkinter as tk
import json
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
import tkinter.ttk as ttk
import webbrowser
import re
import pandas as pd
import sqlite3
import os
import socket
from ClickableTable2 import ClickableTable2
import threading
import time
import queue
import urllib.request
import xml.etree.ElementTree as ET
import ssl
from SimpleScrollableFrameClam import SimpleScrollableFrame
from rauth.service import OAuth1Service, OAuth1Session
from PIL import Image, ImageTk # allows for image formats other than gif
from urllib.request import urlopen
import io

#testdf = pd.DataFrame(np.random.randint(0, 1000000, size=(50, 10)), columns=['A', 'BC', 'DEF', 'GHIJ', 'KLMNO', 'PQRS', 'TUV', 'WX', 'Y', 'Z'])
#testdf = pd.read_csv('TinySample.csv')
testdf = pd.read_csv('goodreads_library_100.csv')#.to_string()
numCols = ['Book Id', 'ISBN13', 'My Rating', 'Average Rating', 'Number of Pages', 'Year Published', 'Original Publication Year', 'Read Count', 'Owned Copies']
#testdf[numCols] = testdf[numCols].apply(pd.to_numeric)
testdf = testdf[['Title', 'Author', 'Publisher', 'Number of Pages']]
#testdf.drop(columns = ['Book Id', 'Author l-f', 'Additional Authors', 'ISBN13', 'Read Count', 'My Review', 'My Rating', 'Average Rating','Date Read', 'Date Added', 'Bookshelves', 'Bookshelves with positions', 'Binding','Exclusive Shelf', 'ISBN', 'Original Publication Year','Spoiler', 'Private Notes','Recommended For', 'Recommended By', 'Owned Copies', 'Original Purchase Date', 'Original Purchase Location', 'Condition', 'Condition Description', 'BCID'], inplace = True )


class MainGUI:

    settings_filename = "settings.json"
    noUser = "none"
    iconFilePath = 'bookicon.ico'
    goodreads_icon_filepath = 'GoodreadsIcon.png'

    default_settings = {
            "users" : {},
            "last_user" : "0",
            "show_fields": ["Title", "Author", "My Rating", "Date Read", "Date Added"],
            "dbname" : "GRLibrary.sqlite",
            "tbname" : "Library"
    }
    key = 'TNY6fDFILUDCTXZ739z56w'
    secret = 'k1CksvrhI3xOcTSDcQU9jCL2yw1HYYzft4fx9SRuB4'

    # display = wx.App(False) # the wx.App object must be created first.
    # display_size = print(wx.GetDisplaySize())  # returns a tuple
    # gr_image_size = int(display_size[0]/20)
    # del display
    gr_image_size = 50
    user_linked = False

    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(500, 350)
        self.parent.geometry("1000x500")
        self.parent.title("Library Manager")
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseApp)

        # FIRST: CHECK THE SETTINGS!
        self.CheckSettings()

        self.user_settings = {
                'style':{
                        'bg':'#F4F1EA',
                        'button':{'fg':'black',
                                  'bg':'white',
                                  'font':'Times',
                                  'size':12,
                                  'weight':'bold'},
                        'title':{'color':'black',
                                 'font':'Times',
                                 'size':17,
                                 'weight':'bold'},
                        'label':{'color':'black',
                                 'font':'Times',
                                 'size':11,
                                 'weight':'bold'}
                        }
        }

        self.styleObj = ttk.Style()
        s = self.user_settings['style']
        self.internetStatus = tk.StringVar()
        self.queue_delay = 500
        self.current_window = 'MainGUI'
        #self.styleObj.configure("button.TButton", highlightcolor = 'red', foreground = s['button']['fg'], background = s['button']['bg'], font = (s['button']['font'], s['button']['size'], s['button']['weight']))

        #362112 good color
        self.styleObj.theme_use('clam')
        self.styleObj.configure('button.TButton', font = (s['button']['font'], s['button']['size'], s['button']['weight']))
        self.styleObj.map('button.TButton', foreground=[('disabled', 'gray'),('pressed', 'black'), ('active', '#382110')], background=[('pressed', '!disabled', '#BAAC9A'), ('active', 'white')], bordercolor = [('active', '#382110')])
        self.styleObj.configure("title.TLabel", foreground = s['title']['color'], background = s['bg'], font = (s['title']['font'], s['title']['size'], s['title']['weight']))
        self.styleObj.configure("label.TLabel", foreground = s['label']['color'], background = s['bg'], font = (s['label']['font'], s['label']['size'], s['label']['weight']))
        self.styleObj.configure("error.TLabel", foreground = 'red', background = s['bg'], font = (s['label']['font'], s['label']['size'], s['label']['weight']))

        self.styleObj.configure("TFrame", background = s['bg'])
        self.styleObj.configure('cb.TCombobox', background = 'white', arrowsize = 25)
        self.parent.option_add("*TCombobox*Listbox*Font", font.Font(family="Times",size=12))
        self.parent.option_add("*TCombobox*Font", font.Font(family="Times",size=12))

        self.frame           = ttk.Frame(self.parent, style = 'TFrame')
        self.title_label     = ttk.Label(self.frame,  text = 'Library Manager', style = "title.TLabel")
        self.user_label      = ttk.Label(self.frame, style = "label.TLabel")
        self.gr_link         =  tk.Label(self.frame, height = self.gr_image_size, width = self.gr_image_size, cursor = 'hand1')
        self.gr_link.image   = ImageTk.PhotoImage(Image.open(self.goodreads_icon_filepath).resize((self.gr_image_size, self.gr_image_size)))
        self.gr_link.configure(image = self.gr_link.image)
        self.gr_link.bind('<Button-1>', self.open_goodreads)
        self.internet_status = ttk.Label(self.frame, style = "error.TLabel", textvariable = self.internetStatus)
        self.settings_button = ttk.Button(self.frame, text = 'Settings', command = lambda: self.Open(Settings), style = "button.TButton")
        self.db_button       = ttk.Button(self.frame, text = 'Manage Database', command = lambda: self.Open(ManageDatabase), style = "button.TButton")
        self.add_book_button = ttk.Button(self.frame, text = 'Add a Book', command = self.open_add_book, style = "button.TButton")
        self.user_button     = ttk.Button(self.frame, text = 'User',     command = lambda: self.Open(UserInfo), style = "button.TButton")
        self.online_button   = ttk.Button(self.frame, text = 'Online Stuff',     command = lambda: self.Open(OnlineStuff), style = "button.TButton")
        self.quit_button     = ttk.Button(self.frame, text = 'Quit',     command = self.CloseApp              , style = "button.TButton")
        self.table           = ClickableTable2(self.frame, df = testdf)#, editable = True)

        self.internet = False
        self.q = queue.Queue(maxsize = 1)
        self.check_internet = InternetThread(self)
        self.check_internet.start()
        self.check_queue()

        tk.Grid.columnconfigure(self.parent, 0, weight = 1)
        tk.Grid.rowconfigure(self.parent, 0, weight = 1)

        tk.Grid.columnconfigure(self.frame, 0, weight = 0)
        tk.Grid.columnconfigure(self.frame, 1, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 0, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 1, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 2, weight = 1)
        #tk.Grid.rowconfigure(self.frame, 3, weight = 1)
        tk.Grid.rowconfigure(self.frame, 9, weight = 1)

        self.title_label.grid(row = 0, column = 0, columnspan = 2)
        self.gr_link.grid(row = 0, column = 1, sticky = tk.E)
        self.user_label.grid(row = 1, column = 0, sticky = tk.W, padx = 10, pady = 5)
        self.user_button.grid(row = 2, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.db_button.grid(row = 3, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.settings_button.grid(row = 4, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.add_book_button.grid(row = 5, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.online_button.grid(row = 6, column = 0, sticky = tk.W+tk.E, padx = 10, pady = 5)
        self.internet_status.grid(row = 7, column = 0, sticky = tk.W, padx = 10, pady = 5)
        self.quit_button.grid(row = 10, column = 0, sticky = tk.S+tk.W+tk.E, padx = 10, pady = 10)
        self.table.grid(row = 1, rowspan = 10, column = 1, sticky = tk.N+tk.S+tk.E+tk.W, padx = 10, pady = 10)
        self.frame.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
        self.parent.iconbitmap(self.iconFilePath)

        # THEN: CHECK FOR USERS!
        if len(self.settings['users']) == 0:
            self.user = self.noUser
            self.UpdateUser()
            self.NonFatal('Welcome to Goodreads Library Manager. Create a User')
            self.Open(CreateEditUser, 'create')
        elif self.settings['last_user'] == '0':
            self.user = tuple(self.settings['users'].keys())[0]
            self.UpdateUser()
            self.Open(ManageUsers)
        elif self.settings['last_user'] not in self.settings['users'].keys():
            self.user = tuple(self.settings['users'].keys())[0]
            self.NonFatal('Last user not found in user list. Select existing user or create a new one.')
            self.UpdateUser()
            self.Open(ManageUsers)
        elif self.settings['last_user'] in self.settings['users'].keys():
            self.user = self.settings['last_user']
            self.UpdateUser()
            # LOAD THE DATABASE

        self.StartSession()

    def StartSession(self):
        if 'access_token' in self.settings['users'][self.user]:
            try:
                self.SubsequentSession()
            except:
                self.NewSession()
        else:
            ans = tk.messagebox.askquestion ('Link GoodReads', 'Do you want to connect to GoodReads?', icon = 'warning')
            if ans == 'yes':
                self.NewSession()
            else:
                self.user_linked = False
                return

    def NewSession(self):
        self.linker = OAuth1Service(
            consumer_key = self.key,
            consumer_secret = self.secret,
            #name = 'goodreads_link',
            request_token_url = 'https://www.goodreads.com/oauth/request_token',
            authorize_url = 'https://www.goodreads.com/oauth/authorize',
            access_token_url = 'https://www.goodreads.com/oauth/access_token',
            base_url = 'https://www.goodreads.com/'
        )
        request_token, request_token_secret = self.linker.get_request_token(header_auth = True)
        authorize_url = self.linker.get_authorize_url(request_token)
        webbrowser.open_new(authorize_url)

        ans = tk.messagebox.askquestion ('Waiting for Authorization', 'Have you authorized Library Manager in Goodreads?', icon = 'warning')

        self.user_linked = False
        while not self.user_linked:
            try:
                self.goodreads_link = self.linker.get_auth_session(request_token, request_token_secret)

                # Subsequent sessions
                self.settings['users'][self.user]['access_token'] = self.goodreads_link.access_token
                self.settings['users'][self.user]['access_token_secret'] = self.goodreads_link.access_token_secret
                self.user_linked = True
            except:
                ans = tk.messagebox.askretrycancel ('Authorization failed', 'Authorize the app in Goodreads and retry, or cancel.', icon = 'warning')
                if ans == True:
                    webbrowser.open_new(authorize_url)
                    continue
                else:
                    break

        del request_token, request_token_secret, authorize_url
        # if response.status_code != 201:
        #     raise Exception('Action failed: %s' % response.status_code)
        # else:
        #     print('Success!')

    def SubsequentSession(self):
        self.goodreads_link = OAuth1Session(
            consumer_key = self.key,
            consumer_secret = self.secret,
            access_token = self.settings['users'][self.user]['access_token'],
            access_token_secret = self.settings['users'][self.user]['access_token_secret'],
        )
        self.user_linked = True

    def CloseApp(self):
        try:
            self.settings['last_user'] = self.user
        except:
            print('Failed to update last user. No user exists')
        self.WriteSettings()
        self.check_internet.stop()
        self.parent.destroy()
        #quit()

    def open_goodreads(self, event):
        if self.internet:
            webbrowser.open_new('http://www.goodreads.com/')
        else:
            self.no_internet_msg()

    def open_add_book(self):
        if self.internet:
            self.Open(AddBook)
        else:
            self.no_internet_msg()

    def no_internet_msg(self):
        self.NonFatal('No Internet')

    def Open(self, window, *vargs):
        self.NewWindow = tk.Toplevel(self.parent)
        self.WindowObject = window(self.NewWindow, self, *vargs)
        self.current_window = re.findall("\.(.+)\'", str(window))[0]

    def Close(self):
        self.NewWindow.grab_release()
        self.NewWindow.destroy()
        self.current_window = 'MainGUI'

    def NonFatal(self, message):
        messagebox.showinfo('Message', message)

    def Fatal(self, message):
        messagebox.showinfo('Fatal Error', message)
        self.parent.destroy()

    def CheckSettings(self):
        # Attempt to open settings file with json lib
        try:
            with open(self.settings_filename, 'r') as sfile:
                contents = sfile.read()
                self.settings = json.loads(contents)
        # If that fails, write the default settings to the settings file in json format
        except:
            self.NonFatal("Invalid Settings File. Rewriting...")
            self.settings = self.default_settings

            self.WriteSettings()

    def UpdateUser(self):
        self.user_label.configure(text = 'User: ' + self.user)
        if self.user == self.noUser:
            self.user_label.configure(text = "No User Selected")

        if len(self.settings['users']) == 0:
            self.users = list(["No Users"])
        else:
            self.users = list(self.settings['users'].keys())

    def WriteSettings(self):
        with open(self.settings_filename, 'w') as sfile:
            json.dump(self.settings, sfile)

    def check_queue(self):
        if self.q.empty(): print('queue is empty')
        else:
            print('queue has', self.q.qsize(), 'items')
            self.internet = self.q.get()

            ### CONSTANT DEBUGGING
            print('User Linked', self.user_linked)
            #print(self.current_window)
            ###

            if self.internet:
                self.internetStatus.set('')
                self.styleObj.configure("link.TLabel", background = self.user_settings['style']['bg'], foreground = 'blue', font = ('Times', 11), cursor = 'hand2')
                self.add_book_button.configure(state = 'normal')
                if self.current_window == 'ManageDatabase':
                    self.WindowObject.new_db_button.configure(state = 'normal')
                if self.current_window == 'UserInfo':
                    if self.user != self.noUser and self.settings['users'][self.user]['site'] != '':
                        self.WindowObject.user_link.bind("<Button-1>", self.WindowObject.open_user_page)
                        self.WindowObject.user_link.grid(row = 3, column = 0, columnspan = 2)
            else:
                self.internetStatus.set('Internet is bad')
                self.styleObj.configure("link.TLabel", background = self.user_settings['style']['bg'], foreground = 'black', font = ('Times', 11), cursor = 'hand2')
                self.add_book_button.configure(state = 'disabled')
                if self.current_window == 'ManageDatabase':
                    self.WindowObject.new_db_button.configure(state = 'disabled')
                if self.current_window == 'UserInfo':
                    self.WindowObject.user_link.grid_forget()

        self.parent.after(self.queue_delay, self.check_queue)

class InternetThread (threading.Thread):
    delay = 3

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        print("Starting to check for internet")
        while self.running:
            self.CheckInternet()
            time.sleep(self.delay)

    def CheckInternet(self, host = "8.8.8.8", port = 53):
        # Checks google-public-dns-a.google.com for internet connection on 53/tcp
        try:
            socket.setdefaulttimeout(self.delay)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            self.parent.q.put(True)
        except:# socket.error as ex:
            self.parent.q.put(False)

class Settings:
    def __init__(self, parent, main):
        self.main = main

        self.parent = parent
        self.parent.title('Settings')
        self.parent.grab_set()
        self.parent.geometry("200x400+200+200")
        self.parent.resizable(False, False)
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseSettings)

        self.frame = ttk.Frame(self.parent, style = "TFrame")

        self.title_label = ttk.Label(self.frame, text = 'Settings', style = "title.TLabel")
        self.quit_button = ttk.Button(self.frame, text = "Back", command = self.CloseSettings, style = "button.TButton")

        self.title_label.pack()
        self.quit_button.pack()

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def CloseSettings(self):
        self.main.Close()

class UserInfo:
    def __init__(self, parent, main):
        self.main = main

        self.parent = parent
        self.parent.title('User Info')
        self.parent.grab_set()
        self.parent.protocol("WM_DELETE_WINDOW", self.parent.destroy)
        self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        if 'email' not in self.main.settings['users'][self.main.user]:
             self.main.settings['users'][self.main.user]['email'] = ''

        if 'site' not in self.main.settings['users'][self.main.user]:
             self.main.settings['users'][self.main.user]['site'] = ''

        self.title_label = ttk.Label(self.frame, text = 'User Info', style = 'title.TLabel')
        self.user_label = ttk.Label(self.frame, text = 'Name: ' + self.main.user, style = 'label.TLabel')
        self.user_link = ttk.Label(self.frame, text = "Profile on Goodreads", style = 'link.TLabel')
        self.email_label = ttk.Label(self.frame, text = 'Email: ' + self.main.settings['users'][self.main.user]['email'], style = 'label.TLabel')

        self.manage_button = ttk.Button(self.frame, text = 'Manage Users', command = self.OpenManageUsers, style = "button.TButton")
        self.quit_button = ttk.Button(self.frame, text = 'Back', command = self.parent.destroy, style = "button.TButton")

        self.title_label.grid(row = 0, column = 0, columnspan = 2)
        self.user_label.grid(row = 1, column = 0, columnspan = 2)

        if self.main.user != self.main.noUser and self.main.settings['users'][self.main.user]['email'] != '':
            self.email_label.grid(row = 2, column = 0, columnspan = 2)

        self.manage_button.grid(row = 4, column = 1, padx = 10, pady = 5)
        self.quit_button.grid(row = 4, column = 0, padx = 10, pady = 5)

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def OpenManageUsers(self):
        self.main.Close()
        self.main.Open(ManageUsers)

    def open_user_page(self, event):
        if self.main.internet:
            webbrowser.open_new('http://www.goodreads.com/' + self.main.settings['users'][self.main.user]['site'])

class ManageUsers:
    def __init__(self, parent, main):
        self.main = main

        self.parent = parent
        self.parent.grab_set()
        self.parent.title('Manage Users')
        #self.parent.geometry("200x200+200+200")
        self.parent.protocol("WM_DELETE_WINDOW", self.GoToUserInfo)
        self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        #self.title_label = ttk.Label(self.frame, text = 'Users', style = "title.TLabel")

        self.user_list_label = ttk.Label(self.frame, text = 'Select A User', style = "title.TLabel")
        self.user_list = ttk.Combobox(self.frame, state = 'readonly', style = 'cb.TCombobox')
        self.user_list.bind("<<ComboboxSelected>>", self.UserSelected)

        self.ResetUserList()

        self.switch_user_button = ttk.Button(self.frame, text = 'Switch To This User', command = self.SwitchUser, style = "button.TButton")
        self.edit_user_button = ttk.Button(self.frame, text = 'Edit This User', command = self.GoToEditUser, style = "button.TButton")
        self.create_user_button = ttk.Button(self.frame, text = 'Create New User', command = self.GoToCreateUser, style = "button.TButton")
        self.del_user_button = ttk.Button(self.frame, text = 'Delete This User', command = self.DeleteUser, style = "button.TButton")
        self.user_info_button = ttk.Button(self.frame, text = 'Back', command = self.GoToUserInfo, style = "button.TButton")
        self.quit_button = ttk.Button(self.frame, text ='Cancel', command = self.CloseManageUsers, style = "button.TButton")

        #self.title_label.grid(row = 0, column = 1)
        ttk.Frame(self.frame, height = 15).grid(row = 0, column = 0)
        self.user_list_label.grid(row = 1, column = 0, padx = 10, sticky = tk.W)
        self.user_list.grid(row = 2, column = 0, columnspan = 2, padx = 10, sticky = tk.W+tk.E)
        self.switch_user_button.grid(row = 1, column = 2, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.edit_user_button.grid(row = 2, column = 2, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.del_user_button.grid(row = 3, column = 2, padx = 10, pady = 2, sticky = tk.W+tk.E)
        ttk.Frame(self.frame, height = 50).grid(row = 4, column = 0)
        self.create_user_button.grid(row = 5, column = 2, padx = 10, pady = 10, sticky = tk.W+tk.E)
        self.user_info_button.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = tk.W+tk.E)
        self.quit_button.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = tk.W+tk.E)

        self.UserSelected(0)
        if self.main.user == self.main.noUser:
            self.user_info_button['state'] = 'disabled'

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)


    def DeleteUser(self):
        if len(self.main.settings['users']) == 0:
            self.main.NonFatal('There are no users to delete.')
        else:
            userToDel = str(self.user_list.get())
            if messagebox.askquestion('Delete User','Are you sure you want to delete ' + userToDel + '?', icon = 'warning') == 'yes':
                del[self.main.settings['users'][userToDel]]
                if len(self.main.settings['users']) == 0:
                    self.main.user = self.main.noUser
                else:
                    self.main.user = tuple(self.main.settings['users'].keys())[0]
                self.main.UpdateUser()
                self.ResetUserList()
            # else they said no so do nothing
            del userToDel
            self.UserSelected(0)

    def SwitchUser(self):
        self.main.user = self.user_list.get()
        self.main.WriteSettings()
        self.main.UpdateUser()
        self.main.StartSession()
        self.main.Close()

    def ResetUserList(self):
        if self.main.user == self.main.noUser:
            self.user_list['values'] = ('No Users',)
            self.user_list.current(0)
        else:
            self.user_list['values'] = tuple(self.main.users)
            self.user_list.current(self.main.users.index(self.main.user))

    def GoToUserInfo(self):
        self.main.Close()
        self.main.Open(UserInfo)

    def GoToCreateUser(self):
        self.main.Close()
        self.main.Open(CreateEditUser, 'create')

    def CloseManageUsers(self):
        self.main.Close()
        self.main.UpdateUser()

    def GoToEditUser(self):
        self.main.Close()
        self.main.Open(CreateEditUser, 'edit')

    def UserSelected(self, useless):
        self.main.selected_user = self.user_list.get()
        if self.main.selected_user == self.main.user or self.main.selected_user == 'No Users':
            self.switch_user_button['state'] = 'disabled'
        else:
            self.switch_user_button['state'] = 'enabled'
        if self.main.selected_user == 'No Users':
            self.edit_user_button['state'] = 'disabled'
            self.del_user_button['state'] = 'disabled'
        else:
            self.edit_user_button['state'] = 'enabled'
            self.del_user_button['state'] = 'enabled'

class CreateEditUser:
    def __init__(self, parent, main, state):
        self.main = main

        self.parent = parent
        self.parent.resizable(False, False)
        if state == 'create': self.parent.title('Create User')
        if state == 'edit': self.parent.title('Edit User')

        self.parent.grab_set()
        self.parent.protocol("WM_DELETE_WINDOW", self.BackToUsers)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        self.title_label = ttk.Label(self.frame, style = 'title.TLabel')
        if state == 'create': self.title_label.configure(text = 'Create New User')
        if state == 'edit':   self.title_label.configure(text = 'Edit User: ' + self.main.selected_user)

        self.name_label = ttk.Label(self.frame, style = "label.TLabel")
        if state == 'create': self.name_label.configure(text = 'Name (required)')
        if state == 'edit':   self.name_label.configure(text = 'New name (required)')
        self.name_entry = tk.Entry(self.frame, width = 20)

        self.email_label = ttk.Label(self.frame, style = "label.TLabel")
        if state == 'create': self.email_label.configure(text = 'Email: ')
        if state == 'edit':   self.email_label.configure(text = 'New email: ')
        self.email_entry = tk.Entry(self.frame, width = 20)

        self.site_label = ttk.Label(self.frame, style = "label.TLabel")
        if state == 'create': self.site_label.configure(text = 'Site: https://www.goodreads.com/')
        if state == 'edit':   self.site_label.configure(text = 'New site: https://www.goodreads.com/')
        self.site_entry = tk.Entry(self.frame, width = 20)

        if state == 'edit':
            self.name_entry.insert(0, self.main.selected_user)
            self.email_entry.insert(0, self.main.settings['users'][self.main.selected_user]['email'])
            self.site_entry.insert(0, self.main.settings['users'][self.main.selected_user]['site'])

        if state == 'create':
            self.make_button = ttk.Button(self.frame, text = 'Next', command = self.MakeUser, style = "button.TButton")
        if state == 'edit':
            self.make_button = ttk.Button(self.frame, text = 'Apply', command = self.MakeEdits, style = "button.TButton")

        self.quit_button = ttk.Button(self.frame, text = 'Back', command = self.BackToUsers, style = "button.TButton")

        self.title_label.grid(row = 0, columnspan = 4)
        self.name_label.grid(row = 1, column = 0, sticky = tk.E, pady = 5)
        self.name_entry.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.email_label.grid(row = 1, column = 2, sticky = tk.E, pady = 5)
        self.email_entry.grid(row = 1, column = 3, padx = 5, pady = 5)
        self.site_label.grid(row = 3, column = 0, columnspan = 2, sticky = tk.E, pady = 5)
        self.site_entry.grid(row = 3, column = 2, columnspan = 2, sticky = tk.W+tk.E, padx = 5, pady = 5)

        size = self.frame.grid_size()
        self.quit_button.grid(row = size[0], column = 0, sticky = tk.W, padx = 5, pady = 5)
        self.make_button.grid(row = size[0], column = size[1]-1, sticky = tk.E, padx = 5, pady = 5)
        self.frame.pack(fill = tk.BOTH, expand = True)
        del size

        self.parent.iconbitmap(self.main.iconFilePath)

    def MakeUser(self):

        name = self.name_entry.get()
        email = self.email_entry.get()
        site = self.site_entry.get()

        # Data verification
        if name == '':
            self.main.NonFatal('Name is required')
        elif name == 'No Users' or name == self.main.noUser:
            self.main.NonFatal("Name can't be '" + self.main.noUser + "' or 'No Users'")
        elif name in self.main.settings['users']:
            self.main.NonFatal('User already exists. Edit the existing user or delete and recreate it.')
        elif not (re.search('.+@.+\..+', email)) and email != '':
            self.main.NonFatal("Invalid email address.")
        else:
            # If data looks good, go ahead!
            self.main.settings['users'][name] = dict()
            self.main.settings['users'][name]['email'] = email
            self.main.settings['users'][name]['site']  = site

            self.main.user = name
            self.main.WriteSettings()
            self.main.UpdateUser()
            self.main.Close()

        del name, email, site

    def MakeEdits(self):

        name = self.name_entry.get()
        email = self.email_entry.get()
        site = self.site_entry.get()

        # Data verification
        if name == '':
            self.main.NonFatal('Name is required')
        elif name == 'No Users' or name == self.main.noUser:
            self.main.NonFatal("Name can't be '" + self.main.noUser + "' or 'No Users'")
        elif not (re.search('.+@.+\..+', email)) and email != '':
            self.main.NonFatal("Invalid email address.")
        elif name in self.main.settings['users'] and name != self.main.selected_user:
            self.main.NonFatal('New name for ' + self.main.selected_user + ' conflicts with existing user.')
        else:

            if name != self.main.selected_user: # If name changed, copy user settings to new name
                self.main.settings['users'][name] = self.main.settings['users'][self.main.selected_user]
                del self.main.settings['users'][self.main.selected_user]

            # Either way, update settings
            self.main.settings['users'][name]['email'] = email
            self.main.settings['users'][name]['site']  = site

            # If editing the current user, make sure to update user
            if self.main.selected_user == self.main.user:
                self.main.user = name
                self.main.UpdateUser()

            # Write settings and close
            self.main.WriteSettings()
            self.main.Close()
            self.main.Open(ManageUsers)

        del name, email, site

    def BackToUsers(self):
        self.main.Close()
        self.main.Open(ManageUsers)

class ManageDatabase:
    def __init__(self, parent, main):
        self.main = main
        self.parent = parent
        self.parent.grab_set()
        self.parent.title('Manage Database')
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseManageUsers)
        self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        self.title_label = ttk.Label(self.frame, text = 'Manage Database', style = "title.TLabel")



        #self.user_list_label = ttk.Label(self.frame, text = 'Select A User', style = "title.TLabel")
        #self.user_list = ttk.Combobox(self.frame, state = 'readonly', style = 'cb.TCombobox')
        #self.user_list.bind("<<ComboboxSelected>>", self.UserSelected)

        self.update_db_button  = ttk.Button(self.frame, text = 'Update Library',  command = lambda: print(self.update_file_val.get()),  style = "button.TButton")
        self.new_db_button = ttk.Button(self.frame, text = 'New Library', command = self.NewLibrary, style = "button.TButton")
        self.open_db_button = ttk.Button(self.frame, text = 'Open Library', command = lambda: print('Open Library'), style = "button.TButton")

        #self.edit_user_button = ttk.Button(self.frame, text = 'Edit This User', command = self.GoToEditUser, style = "button.TButton")
        #self.create_user_button = ttk.Button(self.frame, text = 'Create New User', command = self.GoToCreateUser, style = "button.TButton")
        #self.del_user_button = ttk.Button(self.frame, text = 'Delete This User', command = self.DeleteUser, style = "button.TButton")
        #self.user_info_button = ttk.Button(self.frame, text = 'Back', command = self.GoToUserInfo, style = "button.TButton")
        #self.quit_button = ttk.Button(self.frame, text ='Cancel', command = self.CloseManageUsers, style = "button.TButton")

        self.title_label.grid(row = 0, column = 0, columnspan = 3)
        self.update_db_button.grid(row = 1, column = 0, padx = 10, pady = 5)
        self.new_db_button.grid(row = 1, column = 1, padx = 10, pady = 5)
        self.open_db_button.grid(row = 1, column = 2, padx = 10, pady = 5)
        #self.UserSelected(0)
        #if self.main.user == self.main.noUser:
        #   self.user_info_button['state'] = 'disabled'

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def NewLibrary(self):
        #filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a CSV File", filetypes = (("Comma-Separated Value Files (.csv)","*.csv"), ))
        #filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select an SQLite database", filetypes = (("SQLite Databases (.sqlite)","*.sqlite"), ))

        filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a CSV or SQLite File", filetypes = (("Supported Files (.csv, .sqlite)",("*.csv", "*sqlite")),))#("SQLite Databases (.sqlite)","*.sqlite")))

        #print(self.replace_file_val.get())
        if re.search('^vsc.', filename[::-1]):
            print('This is a csv file. Loading', filename)
            del self.main.table
            self.main.table = ClickableTable2(self.main.frame, df = pd.read_csv(filename))#, editable = True)
            self.main.table.grid(row = 1, rowspan = 10, column = 1, sticky = tk.N+tk.S+tk.E+tk.W, padx = 10, pady = 10)
            self.CloseManageUsers()

        if re.search('^etilqs.', filename[::-1]):
            print('This is an sqlite file. Not supported yet')

    def CloseManageUsers(self):
        self.main.Close()

class DB():

    def __init__(self, main, _from, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()


        if _from == 'csv':
            self.csvtosqlite()

    def csvtosqlite(self, csvname, dbname, tablename):

        conn = sqlite3.connect(dbname) # Verify/open DB
        cur  = conn.cursor()           # Open connection to DB

        data = pd.read_csv(csvname)
        headers = list(data.columns.values)

        cur.execute('DROP TABLE IF EXISTS ' + tablename)
        cur.execute('CREATE TABLE ' + tablename + ' (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')

        valuesString = ' (' + str(headers).replace('[', '').replace(']', '').replace("'", '"') + ') '
        valuePlaceholders = 'VALUES(' + '?,'*(len(headers) - 1) + '?)'

        for column in headers:
            cur.execute('ALTER TABLE ' + tablename + ' ADD ' + "'" + column + "'" + ' TEXT')

        for i in range(len(data)):
            currentrow = list(data.loc[i])
            for j in range(len(currentrow)):
                if type(currentrow[j]) != str:
                    currentrow[j] = str(currentrow[j])

            cur.execute('INSERT INTO ' + tablename + valuesString + valuePlaceholders, tuple(currentrow))

        conn.commit()

        return headers

class OnlineStuff:

    def __init__(self, parent, main):
        self.main = main
        self.parent = parent
        self.parent.grab_set()
        self.parent.title('Online Stuff')
        self.parent.protocol("WM_DELETE_WINDOW", self.BackToMain)
        #self.parent.resizable(False, False)

        self.frame = ttk.Frame(self.parent, style = 'TFrame')

        self.action_1_button = ttk.Button(self.frame, text = 'Add Book', command = self.AddBook, style = "button.TButton")
        self.action_2_button = ttk.Button(self.frame, text = 'Action 2', command = self.Action2, style = "button.TButton")
        self.action_3_button = ttk.Button(self.frame, text = 'Action 3', command = self.Action3, style = "button.TButton")
        self.action_4_button = ttk.Button(self.frame, text = 'Action 4', command = self.Action4, style = "button.TButton")
        self.action_5_button = ttk.Button(self.frame, text = 'Action 5', command = self.Action5, style = "button.TButton")
        self.quit_button = ttk.Button(self.frame, text ='Back', command = self.BackToMain, style = "button.TButton")

        #self.title_label.grid(row = 0, column = 1)
        self.action_1_button.grid(row = 1, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_2_button.grid(row = 2, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_3_button.grid(row = 3, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_4_button.grid(row = 4, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.action_5_button.grid(row = 5, column = 0, padx = 10, pady = 2, sticky = tk.W+tk.E)
        self.quit_button.grid(row = 6, column = 0, padx = 10, pady = 10, sticky = tk.W+tk.E)

        self.frame.pack(fill = tk.BOTH, expand = True)
        self.parent.iconbitmap(self.main.iconFilePath)

    def AddBook(self):
        print('Doing Action 1')
        #self.main.

    def Action2(self):
        print('Doing Action 2')

    def Action3(self):
        print('Doing Action 3')

    def Action4(self):
        print('Doing Action 4')

    def Action5(self):
        print('Doing Action 5')

    def BackToMain(self):
        self.main.Close()

class AddBook:
    # Goodreads API Keys
    def __init__(self, parent, main):
        self.parent = parent
        self.main = main
        self.parent.title('Add a Book')
        self.parent.grab_set()
        self.parent.protocol("WM_DELETE_WINDOW", self.BackToMain)

        self.results_list = list()

        self.container = tk.Frame(self.parent)
        self.results_area = SimpleScrollableFrame(self.container)
        self.results_area.frame.clicked = self.clicked

        self.title_label = tk.Label(self.container, text = 'ADD A BOOK', font = ('Times', 14, 'bold'))

        self.search_label = tk.Label(self.container, text = 'Enter search term: ', font = ('Times', 12))

        self.search_entry = tk.Entry(self.container)
        self.search_entry.bind("<Return>", self.search)

        self.search_button = tk.Button(self.container, text = 'Search', command = lambda: self.search(0))
        self.back_button = tk.Button(self.container, text = 'Back', command = self.BackToMain)

        self.ignore_ssl_errors()

        #self.xmloutput = open('query_results.xml', 'w+')

        # Configure all rows and columns present to have the same weight (so they expand with the window)
        tk.Grid.columnconfigure(self.parent, 0, weight = 1)
        tk.Grid.rowconfigure(self.parent, 0, weight = 1)
        tk.Grid.columnconfigure(self.container, 3, weight = 1)
        tk.Grid.rowconfigure(self.container, 2, weight = 1)

        # Add the frame and its elements
        self.title_label.grid(row = 0, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
        self.back_button.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.W, padx = 10, pady = 5)
        self.search_label.grid(row = 1, column = 0, sticky = tk.N+tk.E+tk.S+tk.W, pady = 5)
        self.search_entry.grid(row = 1, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 5)
        self.search_button.grid(row = 1, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, padx = 10, pady = 5)

        self.container.grid(row = 0, column = 0, sticky = tk.N+tk.E+tk.S+tk.W)

    def search(self, event):
        if not self.main.internet:
            self.main.no_internet_msg()
            self.BackToMain()

        for result in self.results_list:
            result.grid_forget()
            result.destroy()
        self.results_list = []

        self.search_term = str(self.search_entry.get())
        #self.search_entry.delete(0, tk.END)
        search_url = 'https://www.goodreads.com/search.xml?key='+self.main.key+'&'+urllib.parse.urlencode({'q':self.search_term})
        xmldata = urllib.request.urlopen(search_url).read().decode()

        #self.xmloutput.write(xmldata)

        # Pull book names
        tree = ET.fromstring(xmldata)
        books_outer = tree.findall('search/results/work')

        self.results_area.grid(row = 2, column = 0, columnspan = 4, sticky = 'NESW')

        try: # prevents errors if the user clicks before all the results are loaded

            if len(books_outer) == 0:
                self.results_list.append(tk.Label(self.results_area.frame, text = 'No Results', font = ('Times', 14, 'bold')))
                self.results_list[0].grid(row = 0)

            else:
                i = 0
                for book in books_outer:

                    book_inner = book.find('best_book')
                    author = book_inner.find('author')

                    bookinfo = dict()
                    bookinfo['Author'] = author.find('name').text
                    bookinfo['author_id'] = author.find('id').text

                    bookinfo['Book Id'] = book_inner.find('id').text
                    bookinfo['Title'] = book_inner.find('title').text
                    bookinfo['small_image_url'] = book_inner.find('small_image_url').text
                    bookinfo['image_url'] = book_inner.find('image_url').text

                    year = book.find('original_publication_year').text
                    month = book.find('original_publication_month').text
                    day = book.find('original_publication_day').text

                    months = {'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
                    date = ''
                    if month != None:
                        date += months[month] + ' '
                        if day != None:
                            date += day + ', '
                    if year != None:
                        date += year


                    #bookinfo['date'] = bookinfo['year'] + '-' + bookinfo['month'] + '-' + bookinfo['day']
                    bookinfo['date'] = date
                    bookinfo['Year Published'] = year
                    bookinfo['Original Publication Year'] = year

                    bookinfo['Average Rating'] = book.find('average_rating').text

                    self.results_list.append(BookResult(self.results_area.frame, bookinfo))
                    self.results_list[i].grid(row = i, column = 0, columnspan = 2, sticky = 'NESW')
                    self.results_area.frame.update()
                    i += 1
                    del bookinfo, author, book_inner, date, day

                del search_url, xmldata, tree, books_outer

        except:
            pass

    def ignore_ssl_errors(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    def clicked(self, bookinfo):
        self.main.lastbookadded = bookinfo
        self.main.table.add_row(bookinfo)
        #print('Adding ' + bookinfo['Title'] + ' to Table')
        self.parent.destroy()

    def BackToMain(self):
        self.main.Close()

class BookResult(tk.Frame):

    def __init__(self, parent, bookinfo):

        self.parent = parent
        self.bookinfo = bookinfo

        self.elems = dict()
        self.image_height = 75
        self.title_font = ('Times', 14, 'bold')
        self.author_font = ('Times', 12)
        self.other_font = ('Times', 10)

        self.incolor = '#BAAC9A'
        self.outcolor = 'white'

        tk.Frame.__init__(self, self.parent)
        self.configure(bg = self.outcolor)

        self.bind('<Button-1>', self.clicked)
        self.bind('<Enter>', self.entered)
        self.bind('<Leave>', self.exited)

        if 'image_height' in self.bookinfo:
            self.image_height = self.bookinfo['image_height']

        self.elems['Image'] = tk.Label(self, bd = 0, height = self.image_height)
        #self.elems['Image'].bind('<Button-1>', self.clicked)
        self.pic = self.get_image(self.bookinfo['small_image_url'])
        self.elems['Image'].configure(image = self.pic)


        self.elems['Title'] = tk.Label(self, text = self.bookinfo['Title']+' (ID: '+self.bookinfo['Book Id']+')', font = self.title_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Author'] = tk.Label(self, text = self.bookinfo['Author']+' (ID: '+self.bookinfo['author_id']+')', font = self.author_font, justify = tk.LEFT, bg = self.outcolor)

        self.elems['Date_Rating'] = tk.Label(self, font = self.other_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Date_Rating'].configure(text = 'Published: '+self.bookinfo['date']+';\t'+'Rating: '+self.bookinfo['Average Rating']+'/5')

        for element in self.elems:
            self.elems[element].bind('<Button-1>', self.clicked)

        self.elems['Image'].grid(row = 0, rowspan = 10, column = 0, sticky = 'NESW')
        self.elems['Title'].grid(row = 0, column = 1, columnspan = 2, sticky = 'NSW')
        self.elems['Author'].grid(row = 1, column = 1, sticky = 'NSW')
        self.elems['Date_Rating'].grid(row = 2, column = 1, sticky = 'NSW')

    def get_image(self, path):

        # Open as a PIL image object
        pil_image = Image.open(io.BytesIO(urlopen(path).read()))

        # Get size and resize
        (w, h) = pil_image.size
        pil_image = pil_image.resize((int(w*self.image_height/h), self.image_height))

        del w, h

        # convert PIL image object to Tkinter PhotoImage object
        return ImageTk.PhotoImage(pil_image)

    def clicked(self, event):
        try:
            self.parent.clicked(self.bookinfo)
        except:
            pass # Parent won't always have a clicked function

    def entered(self, event):
        #print('Entered', self.bookinfo['title'])
        self.configure(bg = self.incolor)
        for element in self.elems:
            self.elems[element].configure(bg = self.incolor)

    def exited(self, event):
        #print('Exited', self.bookinfo['title'])
        self.configure(bg = self.outcolor)
        for element in self.elems:
            self.elems[element].configure(bg = self.outcolor)


root = tk.Tk()
app = MainGUI(root)
root.mainloop()

# CREDITS
# GUI Window Switching: https://pythonprogramming.altervista.org/create-more-windows-with-tkinter/
>>>>>>> 863758138b84a6f949ff07d574df24c5fed820ad
