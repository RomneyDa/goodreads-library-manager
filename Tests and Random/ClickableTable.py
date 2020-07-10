# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 23:54:11 2020

@author: Dalli
"""

import tkinter as tk
from tkinter import ttk

class ClickableTable(tk.Frame):
    
    # DEFAULTS
    editable = True
    
    def __init__(self, parent, df, **kwargs):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self)
        
        self.yscrollbar = ttk.Scrollbar(self, orient = 'vertical', command = self.canvas.yview)
        self.xscrollbar = ttk.Scrollbar(self, orient = 'horizontal', command = self.canvas.xview)
       
        self.frame = ttk.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        
        self.canvas.bind('<Enter>', self.EnterFrame)
        self.canvas.bind('<Leave>', self.LeaveFrame)
        
        self.canvas.create_window((0, 0), window = self.frame, anchor = "nw")
        self.canvas.configure(yscrollcommand = self.yscrollbar.set)
        self.canvas.configure(xscrollcommand = self.xscrollbar.set)
        
        self.df = df
        self.size = [self.df.shape[0], self.df.shape[1]]
        self.past_dfs = list()
        self.ascending = True
        self.history_limit = 10
        self.last_sorted = 0
        self.drag_threshold = 7
        self.dynamic_limit = 51
        self.font = ('Times', 11)
        self.scroll_sensitivity = 3
        self.adjust_sensitivity = 0.2
        self.header_font = ('Times', 12, 'bold')
        
        self.styleObj = ttk.Style()
        self.styleObj.theme_use('clam')
        self.styleObj.configure('tktable_header.TButton', font = self.header_font, background = 'gray', foreground = 'black')
        self.styleObj.map('tktable_header.TButton', foreground=[('disabled', 'gray'),('pressed', 'black'), ('active', '#382110')], background=[('pressed', '!disabled', '#BAAC9A'), ('active', 'white')], bordercolor = [('active', '#382110')])
        
        #self.styleObj.configure("tktable_row0.TEntry", foreground = 'black', fieldbackground = 'white')
        #self.styleObj.configure("tktable_row1.TEntry", foreground = 'black', fieldbackground = 'light gray')
        
        self.styleObj.configure("tktable_row0.TLabel", foreground = 'black', background = 'white')
        self.styleObj.configure("tktable_row1.TLabel", foreground = 'black', background = 'light gray')
        
        self.styleObj.configure("tktable_adjustors.TButton", padding = 0, highlightthickness = 0, width = -0, background = 'black', bordercolor = 'black', lightcolor = 'black', darkcolor = 'black')

        #headers = list()
        #for header in self.df.columns:
        #    pass
        
        self.headers = {header:ttk.Button(self.frame, text = header, style = 'tktable_header.TButton') for header in self.df.columns}
        self.widths = {header:max([len(str(val)) for val in self.df[header]]) for header in self.df.columns}
        self.initial_widths = self.widths.copy()
        self.values = {header:[None]*self.size[0] for header in self.df.columns}
        self.col_adjustors = {header:tk.Button(self.frame, width = -0, padx = 0, bd = 0, highlightthickness = 0, cursor = 'sb_h_double_arrow', bg = 'white') for header in self.df.columns}
        #self.col_adjustors = {header:ttk.Button(self.frame, cursor = 'sb_h_double_arrow', style = 'tktable_adjustors.TButton') for header in self.df.columns}

        col = 0
        for header in self.headers:
            self.headers[header].bind('<Button-1>', self.header_click)
            self.headers[header].grid(row = 0, column = 2*col, sticky = tk.N+tk.S+tk.E+tk.W)
            self.headers[header].header = header
            
            self.col_adjustors[header].grid(row = 0, rowspan = self.size[0]+1, column = 2*col+1, sticky = tk.N+tk.S+tk.E+tk.W)
            self.col_adjustors[header].bind('<Button-1>', self.Click_pos)
            if self.size[0] > self.dynamic_limit: 
                self.col_adjustors[header].bind('<ButtonRelease-1>', self.Release_pos)
            else:
                self.col_adjustors[header].bind('<B1-Motion>', self.Current_pos)
            self.col_adjustors[header].bind('<Double-Button-1>', self.Reset_width)
            self.col_adjustors[header].header = header
            
            for row in list(self.df.index):
                # LABEL FIELD
                #self.values[header][row] = ttk.Label(self.frame, width = self.widths[header], text = str(self.df[header][row]))
                #if row%2 == 0: self.values[header][row].configure(style = 'tktable_row0.TLabel')
                #if row%2 == 1: self.values[header][row].configure(style = 'tktable_row1.TLabel')
                
                # TEXT FIELD
                #if row%2 == 0: self.values[header][row] = tk.Text(self.frame,height = 1, borderwidth = 0,wrap = tk.WORD,width = self.widths[header],font = self.font, bg = 'white')
                #if row%2 == 1: self.values[header][row] = tk.Text(self.frame,height = 1,borderwidth = 0,wrap = tk.WORD,width = self.widths[header],font = self.font, bg = 'light gray')
                
                # ENTRY
                self.values[header][row] = ttk.Entry(self.frame, width = self.widths[header])
                if row%2 == 0: self.values[header][row].configure(style = 'tktable_row0.TEntry')
                if row%2 == 1: self.values[header][row].configure(style = 'tktable_row1.TEntry')
                
                # ENTRY OR TEXT (index = 1.0 for text field, 0 for entry)
                self.values[header][row].insert(0, str(self.df[header][row]))
                if not(self.editable): self.values[header][row].configure(state = 'readonly')
                self.values[header][row].configure(width = self.widths[header])
                
                self.values[header][row].row = row
                self.values[header][row].header = header
                self.values[header][row].bind("<Button-1>", self.value_click)
                self.values[header][row].bind ("<Return>", self.value_changed)
                self.values[header][row].bind ("<FocusOut>", self.value_changed)
                self.values[header][row].grid(row = row + 1, column = col*2, sticky = tk.N+tk.S+tk.E+tk.W)
                
            col += 1
        del col

        self.canvas.grid(row = 0, column = 0,     sticky = tk.S+tk.E+tk.N+tk.W)
        self.yscrollbar.grid(row = 0, column = 1, sticky = tk.S+tk.E+tk.N+tk.W)
        self.xscrollbar.grid(row = 1, column = 0, sticky = tk.S+tk.E+tk.N+tk.W)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 0)
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 0)
        
        tk.Grid.rowconfigure(self.frame, 0, weight = 1)
        tk.Grid.rowconfigure(self.frame, 0, weight = 1)

    def MouseWheel(self, event):
        self.canvas.yview_scroll(-1*int(event.delta*self.scroll_sensitivity/360), "units")

    def EnterFrame(self, event):
        self.frame.bind_all("<MouseWheel>", self.MouseWheel)   

    def LeaveFrame(self, event):
        self.frame.unbind_all("<MouseWheel>")   
            
    def value_click(self, event):
        print('header:', event.widget.header, 'row:', event.widget.row, 'value:', self.df[event.widget.header][event.widget.row])
        
    def value_changed(self, event):
        print('I changed the value to', event.widget.get())
        self.df.at[event.widget.row, event.widget.header] = event.widget.get()
        
    def header_click(self, event):
        #print('Sorting by', event.widget.header)
        if self.last_sorted == event.widget.header:
            self.ascending = not(self.ascending)
        else: 
            self.ascending = True
        
        self.past_dfs.append(self.df)
        if len(self.past_dfs) > self.history_limit:
            self.past_dfs.pop(0)
        
        self.df.sort_values(by = [event.widget.header], ascending = self.ascending, inplace = True)
        self.last_sorted = event.widget.header
        self.ReassignValues()
        
    def ReassignValues(self):
        for header in self.df.columns:
            row = 0
            for df_index in list(self.df.index):
                # LABEL
                #self.values[header][row].configure(text = str(self.df[header][df_index]))
                
                # TEXT OR ENTRY (index = 0 for entry, 1.0 for text field)
                if not(self.editable): self.values[header][row].configure(state = 'normal')
                self.values[header][row].delete(0, tk.END)
                self.values[header][row].insert(0, str(self.df[header][df_index]))
                if not(self.editable): self.values[header][row].configure(state = 'readonly')
                
                self.values[header][row].row = df_index
                row += 1
            del row
        
    def Click_pos(self, event):
        self.click_pos = event.x
        
    def Release_pos(self, event):
        change = int((event.x - self.click_pos)*self.adjust_sensitivity)
        header = event.widget.header
        if abs(change) >= self.widths[header] and change < 0:
            self.widths[header] = 1
        else:
            self.widths[header] += change
            
        self.values[header][self.size[0]-1].configure(width = self.widths[header])
        del header, change
    
    def Current_pos(self, event):
        header = event.widget.header
        pos = event.x - self.click_pos
        if pos > self.drag_threshold:
            self.widths[header] += 1
            #self.values[header][-1].configure(width = self.widths[header])
            self.values[header][-1].configure(width = self.widths[header])
        if pos < -self.drag_threshold and self.widths[header] > 1: # and self.widths[header] >= self.initial_widths[header]:
            self.widths[header] -= 1
            self.values[header][-1].configure(width = self.widths[header])
            
        del header, pos
        #self.headers[event.widget.header].configure(width =  self.widths[event.widget.header])
        #print('Mouse is at', event.x - self.click_pos, 'from', event.widget.header) 
        #print('Initial width of', event.widget.header, 'was', self.initial_widths[event.widget.header])
        #print('Current width of', event.widget.header, 'is', self.headers[event.widget.header].cget('width'))
    
    def Reset_width(self, event):
        header = event.widget.header
        self.values[header][self.size[0]-1].configure(width = self.initial_widths[header])
        del header