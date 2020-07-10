# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 02:48:46 2020

@author: Dalli
"""

from PIL import Image, ImageTk # allows for image formats other than gif
import tkinter as tk
from urllib.request import urlopen


def get_image(loc):
        #print(loc)
        
        # open as a PIL image object
        #pil_image = Image.open(io.BytesIO(urlopen(loc).read()))
        pil_image = Image.open(loc)
        (w, h) = pil_image.size
        
        max_dim = 50
        if w > max_dim or h > max_dim:
            if w >= h:
                pil_image = pil_image.resize((max_dim, int(h*max_dim/w)))
            else:
                pil_image = pil_image.resize((int(w*max_dim/h), max_dim))
                
        #print(pil_image)
        
        # convert PIL image object to Tkinter PhotoImage object
        return ImageTk.PhotoImage(pil_image)
    
root = tk.Tk()

filename = image_filepath = 'del_button_image2.png'


# convert PIL image object to Tkinter PhotoImage object
tk_image = get_image(filename)

# put the image on a typical widget
label = tk.Label(root, image = tk_image) #, bg='white')
label.pack(padx=5, pady=5)
root.mainloop()