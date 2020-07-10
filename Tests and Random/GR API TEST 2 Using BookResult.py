# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:32:08 2020

@author: Dalli
"""

import urllib.request
import xml.etree.ElementTree as ET
import ssl
import tkinter as tk
from SimpleScrollableFrameClam import SimpleScrollableFrame
from BookResult import BookResult

class AddBook:
    # Goodreads API Keys
    key = 'TNY6fDFILUDCTXZ739z56w'
    secret = 'k1CksvrhI3xOcTSDcQU9jCL2yw1HYYzft4fx9SRuB4'
    
    def __init__(self, parent):
        self.parent = parent
        self.results_list = list()
        
        self.container = tk.Frame(self.parent)
        self.results_area = SimpleScrollableFrame(self.container)
        self.results_area.frame.clicked = self.clicked
        
        self.title_label = tk.Label(self.container, text = 'ADD A BOOK', font = ('Times', 14, 'bold'))
        
        self.search_label = tk.Label(self.container, text = 'Enter search term: ', font = ('Times', 12))
        
        self.search_entry = tk.Entry(self.container)
        self.search_entry.bind("<Return>", self.search)
        
        self.search_button = tk.Button(self.container, text = 'Search', command = lambda: self.search(0))
        self.back_button = tk.Button(self.container, text = 'Back', command = self.parent.destroy)
        
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
        for result in self.results_list:
            result.grid_forget()
            result.destroy()
        self.results_list = []
 
        self.search_term = str(self.search_entry.get())
        #self.search_entry.delete(0, tk.END)
        search_url = 'https://www.goodreads.com/search.xml?key='+self.key+'&'+urllib.parse.urlencode({'q':self.search_term})
        xmldata = urllib.request.urlopen(search_url).read().decode()

        #self.xmloutput.write(xmldata)
        
        # Pull book names
        tree = ET.fromstring(xmldata)
        books_outer = tree.findall('search/results/work')
        
        self.results_area.grid(row = 2, column = 0, columnspan = 4, sticky = 'NESW')
        
        if len(books_outer) == 0:
            self.results_list.append(tk.Label(self.results_area.frame, text = 'No Results', font = ('Times', 14, 'bold')))
            self.results_list[0].grid(row = 0)
        
        else:
            i = 0
            for book in books_outer:
               # try: # prevents errors if the user clicks before all the results are loaded
    
                    book_inner = book.find('best_book')
                    author = book_inner.find('author')
                    
                    bookinfo = dict()
                    bookinfo['author'] = author.find('name').text
                    bookinfo['author_id'] = author.find('id').text
                    
                    bookinfo['book_id'] = book_inner.find('id').text
                    bookinfo['title'] = book_inner.find('title').text
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
                    
                    bookinfo['average_rating'] = book.find('average_rating').text
                    
                    self.results_list.append(BookResult(self.results_area.frame, bookinfo))
                    self.results_list[i].grid(row = i, column = 0, columnspan = 2, sticky = 'NESW')
                    self.results_area.frame.update()
                    i += 1
                    del bookinfo, author, book_inner, date, day
                    
              #  except:
              #      continue
                
            del search_url, xmldata, tree, books_outer
        
       # for book in books:
        #        BookResult(self, image = book)

    def ignore_ssl_errors(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
    def clicked(self, bookinfo):
        print(bookinfo['title'])
        self.parent.destroy()
        
# Create and start app
root = tk.Tk()
app = AddBook(root)
root.mainloop()


