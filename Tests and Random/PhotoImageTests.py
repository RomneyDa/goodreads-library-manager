# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 01:37:50 2020

@author: Dalli
"""

import io
from PIL import Image, ImageTk # allows for image formats other than gif
import tkinter as tk
from urllib.request import urlopen

root = tk.Tk()

url = 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1408303130l/375802._SY160_.jpg'

pil_image = Image.open(io.BytesIO(urlopen(url).read()))
# open as a PIL image object
#pil_image = Image.open(data_stream)
(w, h) = pil_image.size

max_dim = 100
if w >= h:
    resize_factor = max_dim/w
    pil_image = pil_image.resize((max_dim, int(h*max_dim/w)))
else:
    pil_image = pil_image.resize((int(w*max_dim/h), max_dim))

# convert PIL image object to Tkinter PhotoImage object
tk_image = ImageTk.PhotoImage(pil_image)

# put the image on a typical widget
label = tk.Label(root, image=tk_image, bg='brown')
label.pack(padx=5, pady=5)
root.mainloop()