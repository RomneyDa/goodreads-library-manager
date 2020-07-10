# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:32:08 2020

@author: Dalli
"""

import urllib.request
import xml.etree.ElementTree as ET
import ssl
import tkinter as tk
import pandas as pd

from ClickableTable2 import ClickableTable2

class MainGUI:
    # Goodreads API Keys
    key = 'TNY6fDFILUDCTXZ739z56w'
    secret = 'k1CksvrhI3xOcTSDcQU9jCL2yw1HYYzft4fx9SRuB4'
    
    def __init__(self, parent):
        
        
        
        self.container = tk.Frame(parent)
        
        self.search_label = tk.Label(self.container, text = 'Enter search term: ', font = ('Times', 14, 'bold'))
        self.search_entry = tk.Entry(self.container)
        self.search_entry.bind("<Return>", self.search)
        
        self.ignore_ssl_errors()
        
        self.xmloutput = open('query_results.xml', 'w+')
        
        # Configure all rows and columns present to have the same weight (so they expand with the window)
        tk.Grid.columnconfigure(parent, 0, weight = 1)
        tk.Grid.rowconfigure(parent, 0, weight = 1)
        tk.Grid.columnconfigure(self.container, 0, weight = 0)
        tk.Grid.columnconfigure(self.container, 1, weight = 0)
        tk.Grid.columnconfigure(self.container, 2, weight = 1)
        tk.Grid.rowconfigure(self.container, 0, weight = 0)
        tk.Grid.rowconfigure(self.container, 1, weight = 1)
        
        
        # Add the frame and its elements
        self.search_label.grid(row = 0, column = 0)
        self.search_entry.grid(row = 0, column = 1)
        self.container.grid(row = 0, column = 0, sticky = tk.N+tk.E+tk.S+tk.W)
        
    def search(self, event):
        try:
            self.results_list.grid_forget()
            self.results_list.destroy()
        except:
            pass
        
        self.search_term = self.search_entry.get()
        self.search_entry.delete(0, tk.END)
        search_url = 'https://www.goodreads.com/search.xml?key='+self.key+'&'+urllib.parse.urlencode({'q':self.search_term})
        xmldata = urllib.request.urlopen(search_url).read().decode()

        self.xmloutput.write(xmldata)
        
        # Pull book names
        tree = ET.fromstring(xmldata)
        books_outer = tree.findall('search/results/work')
        books_inner = [book.find('best_book') for book in books_outer]
        authors = [book.find('author') for book in books_inner]

        outer_fields = [('original_publication_year', 'Original Publication Year'), 
                             ('original_publication_month', 'Original Publication Month'), 
                             ('original_publication_day', 'Original Publication Day'), 
                             ('average_rating', 'Average Rating')]
        inner_fields = [('id', 'Book id'), 
                             ('title', 'Title'), 
                             ('image_url', 'Image URL'), 
                             ('small_image_url', 'Small Image URL')]
        author_fields = [('id', 'Author id'), 
                              ('name', 'Author')]
        
        books_dict = {pair[1]:[None]*len(books_outer) for pair in outer_fields+inner_fields+author_fields}
        
        for author in range(len(authors)):
            for field in author_fields:
                books_dict[field[1]][author] = authors[author].find(field[0]).text
        
        for book in range(len(books_outer)):
            for field in outer_fields:
                books_dict[field[1]][book] = books_outer[book].find(field[0]).text
            
        for book in range(len(books_inner)):
            for field in inner_fields:
                books_dict[field[1]][book] = books_inner[book].find(field[0]).text
        
        books_dict['#'] = [i+1 for i in range(len(books_outer))]
        
        self.df = pd.DataFrame.from_dict(books_dict)
        self.df_to_show = self.df[['#', 'Title','Author', 'Image URL', 'Small Image URL']]
        
        del search_url, xmldata, tree, books_outer, books_inner, authors, outer_fields, inner_fields, author_fields, books_dict
        
        self.results_list = ClickableTable2(self.container, df = self.df_to_show)
        self.results_list.grid(row = 1, column = 0, columnspan = 3, sticky = tk.N+tk.W+tk.S+tk.E)

    def ignore_ssl_errors(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

# Create and start app
root = tk.Tk()
app = MainGUI(root)
root.mainloop()


