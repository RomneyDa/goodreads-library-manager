# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 23:54:11 2020

@author: Dalli
"""


from PIL import Image, ImageTk # allows for image formats other than gif
from urllib.request import urlopen
import io
import tkinter as tk

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
        self.elems['Image'].bind('<Button-1>', self.clicked)
        self.pic = self.get_image(self.bookinfo['small_image_url'])
        self.elems['Image'].configure(image = self.pic)
        
        
        self.elems['Title'] = tk.Label(self, text = self.bookinfo['title']+' (ID: '+self.bookinfo['book_id']+')', font = self.title_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Title'].bind('<Button-1>', self.clicked)
            
        self.elems['Author'] = tk.Label(self, text = self.bookinfo['author']+' (ID: '+self.bookinfo['author_id']+')', font = self.author_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Author'].bind('<Button-1>', self.clicked)

        self.elems['Date_Rating'] = tk.Label(self, font = self.other_font, justify = tk.LEFT, bg = self.outcolor)
        self.elems['Date_Rating'].bind('<Button-1>', self.clicked)
        self.elems['Date_Rating'].configure(text = 'Published: '+self.bookinfo['date']+';\t'+'Rating: '+self.bookinfo['average_rating']+'/5')
        
       # self.elems['Rating'] = tk.Label(self, text = 'Rating: '+self.bookinfo['average_rating']+'/5', font = self.other_font, justify = tk.LEFT, bg = self.outcolor)
       # self.elems['Rating'].bind('<Button-1>', self.clicked)
        
        self.elems['Image'].grid(row = 0, rowspan = 10, column = 0, sticky = 'NESW')
        self.elems['Title'].grid(row = 0, column = 1, columnspan = 2, sticky = 'NSW')
        self.elems['Author'].grid(row = 1, column = 1, sticky = 'NSW')
        self.elems['Date_Rating'].grid(row = 2, column = 1, sticky = 'NSW')
        #self.elems['Rating'].grid(row = 2, column = 2, sticky = 'NSW')

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
        self.parent.clicked(self.bookinfo)
    
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


