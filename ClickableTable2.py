# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 23:54:11 2020

@author: Dalli
"""

import tkinter as tk
from tkinter import ttk
from SimpleScrollableFrameClam import SimpleScrollableFrame
from tkinter import font
import math
from PIL import Image, ImageTk # allows for image formats other than gif
import pandas as pd

class ClickableTable2(SimpleScrollableFrame):

    # DEFAULTS
    supported_types = ['str', 'int', 'float']

    editable = False
    shown_columns = list()
    last_deleted = list()
    col_adjustors = dict()
    table_frames = dict()
    headers = dict()
    delete_col_buttons = dict()
    types = dict()
    widths = dict()
    initial_widths = dict()
    values = dict()
    past_cols = list()

    header_clicked = True
    deleting = False
    del_button = False
    ascending = True

    last_sorted = 0
    history_limit = 10

    size_factor_limit = 15

    del_image_size = 10 # Default column delete button size, pixels
    del_image_filepath = 'del_button_image.png'

    def __init__(self, parent, **kwargs):
        SimpleScrollableFrame.__init__(self, parent)

        self.scroll_sensitivity = 3

        self.font = font.Font(family='Times', size = 11, weight='normal')
        self.char_width = self.font.measure('0')

        self.header_font = font.Font(family='Times', size = 12, weight='bold')
        self.header_char_width = self.header_font.measure('0')

        self.styleObj = ttk.Style()
        self.styleObj.theme_use('clam')
        self.styleObj.configure('tktable_header.TButton', font = self.header_font, background = 'gray', foreground = 'black')
        self.styleObj.map('tktable_header.TButton', foreground=[('disabled', 'gray'),('pressed', 'black'), ('active', '#382110')], background=[('pressed', '!disabled', '#BAAC9A'), ('active', 'white')], bordercolor = [('active', '#382110')])

        self.styleObj.configure("tktable_row0.TEntry", foreground = 'black', fieldbackground = 'white')
        self.styleObj.configure("tktable_row1.TEntry", foreground = 'black', fieldbackground = 'light gray')

        self.styleObj.configure("tktable_adjustors.TButton", padding = 0, highlightthickness = 0, width = -0, background = 'black', bordercolor = 'black', lightcolor = 'black', darkcolor = 'black')

        if 'df' in kwargs:
            self.df = kwargs['df']
            if 'columns' in kwargs:
                if 'types' in kwargs:
                    self.add_columns(kwargs['columns'], types = kwargs['types'])
                else:
                    self.add_columns(kwargs['columns'])
            else:
                if 'types' in kwargs:
                    self.add_columns(list(self.df.columns), types = kwargs['types'])
                else:
                    self.add_columns(list(self.df.columns))

        if 'del_col_button' in kwargs:
            self.add_del_buttons(kwargs['del_col_button'])
        else:
            try:
                self.add_del_buttons(self.del_image_filepath)
            except: pass

        if 'editable' in kwargs:
            if kwargs['editable'] in [True, False]:
                self.editable = kwargs['editable']
            else:
                raise ValueError('editable option must be True or False')

    def add_del_buttons(self, filepath):
        try:
            pil_image = Image.open(filepath)
            pil_image = pil_image.resize((self.del_image_size, self.del_image_size))
            self.button_image = ImageTk.PhotoImage(pil_image)
            self.del_button = True

            for column in self.shown_columns:
                if column in self.delete_col_buttons:
                    self.delete_col_buttons[column].grid_forget()
                    self.delete_col_buttons[column].destroy()

                self.make_del_button(column)

        except:
            raise ValueError('Invalid image filepath or failure to load image')

    def make_del_button(self, column):
        self.delete_col_buttons[column] = tk.Label(self.table_frames[column], image = self.button_image, height = self.del_image_size, width = self.del_image_size, cursor = 'X_cursor', bd = 0)
        self.delete_col_buttons[column].column = column
        self.delete_col_buttons[column].grid(row = 0, column = 0, sticky = tk.N+tk.E)
        self.delete_col_buttons[column].bind('<Button-1>', self.del_button_clicked)


    def del_columns(self, columns):
        for column in columns:
            if column not in self.shown_columns: continue

            self.table_frames[column].grid_forget()
            self.table_frames[column].destroy()
            #self.df = self.df.drop(columns = [column]) Messes up action memory
            col_pos = self.shown_columns.index(column)

            self.shown_columns.remove(column)

            for i in range(col_pos, len(self.shown_columns)):
                self.table_frames[self.shown_columns[i]].grid_forget()
                self.table_frames[self.shown_columns[i]].grid(row = 0, column = i)

            del self.col_adjustors[column]
            del self.headers[column]
            del self.types[column]
            del self.widths[column]
            del self.initial_widths[column]
            del self.values[column]

            self.set_size_factor()
            #print(self.shown_columns)
            del col_pos

    def add_columns(self, columns, **options):

        # Extract working dataframe using either self.df or given df
        if 'df' in options:
            if options['df'].shape[0] == self.df.shape[0]:
                working_df = options['df']
            else:
                raise ValueError("Number of rows in dataframe must match existing table dataframe")
        else:
            working_df = self.df

        #print(working_df.dtypes)

        # CHECK TYPES - DEFAULT TYPE IS STRING
        for column in columns:
            if column not in list(working_df.columns):
                raise ValueError('{} is not a column in the dataframe. Columns include {}'.format(columns, list(working_df.columns)))
            if str(column) == 'sort_col':
                raise ValueError('sort_col is a reserved column name for ClickableTable2')

        types = dict()
        if 'types' in options:
            #print(len(options['types']))
            for item in options['types']:
                if item not in self.supported_types:
                    raise ValueError('{} is not a supported type. Supported types are {}'.format(item, self.supported_types))
                    del types
                    return
            if len(options['types']) == 1:
                for column in columns:
                    types[column] = options['types'][0]
            elif len(options['types']) == len(columns):
                i = 0
                for column in columns:
                    types[column] = options['types'][i]
                    i += 1
                del i
            else:
                raise ValueError('Type must be of length 1 or the same length as the columns list')
                del types
                return
        else:
            for column in columns:
                types[column] = 'str'

        for column in columns.copy():
            if column in self.shown_columns:
                if 'replace' in options and options['replace'] == False:
                    columns.remove(column)
                    del types[column]
                else:
                    self.del_columns([column])
                    self.df[column] = working_df[column]

        # If no columns left to add, return
        if len(columns) == 0:
            del types, working_df
            return

        #if len(self.heights) == 0:
        #    self.heights = [0]*working_df.shape[0]

        for column in columns:

            self.values[column] = [None]*len(working_df[column])

            self.table_frames[column] = tk.Frame(self.frame)

            self.headers[column] = ttk.Button(self.table_frames[column], text = column, style = 'tktable_header.TButton')
            self.headers[column].configure(width = math.ceil(self.header_font.measure(column)/self.header_char_width))
            self.headers[column].column = column
            self.headers[column].grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.W+tk.E)
            self.headers[column].bind('<Button-1>', self.header_click)
            self.headers[column].bind('<B1-Motion>', self.swap_columns)
            self.headers[column].bind('<ButtonRelease-1>', self.sort_table)

            if self.del_button:
                self.make_del_button(column)

            self.col_adjustors[column] = tk.Button(self.table_frames[column], width = -0, padx = 0, bd = 0, highlightthickness = 0, cursor = 'sb_h_double_arrow', bg = 'white')
            self.col_adjustors[column].column = column
            self.col_adjustors[column].grid(row = 0, rowspan = working_df.shape[0]+1, column = 1, sticky = tk.N+tk.S+tk.E+tk.W)
            self.col_adjustors[column].bind('<Button-1>', self.adjust_clicked)
            self.col_adjustors[column].bind('<Double-Button-1>', self.reset_width)
            self.col_adjustors[column].bind('<B1-Motion>', self.resize_column)


            for row in list(working_df.index):

                if types[column] in ['str', 'int']:

                    self.create_value(row, column, working_df)

            self.table_frames[column].grid(row = 0, column = len(self.shown_columns), sticky = tk.N+tk.S+tk.E+tk.W)

            self.types[column] = types[column]
            self.shown_columns.append(column)

            self.headers[column].update()
            self.headers[column].configure(width = math.floor(self.headers[column].winfo_width()/self.header_char_width))
            self.widths[column] = self.headers[column].cget('width')
            self.initial_widths[column] = self.widths[column]

            if types[column] in ['str', 'int']:
                for item in self.values[column]:
                    item.configure(width = 1)

        del types, working_df
        self.set_size_factor()

    def create_value(self, row, column, df):
        self.values[column][row] = ttk.Entry(self.table_frames[column], font = self.font)
        self.values[column][row].configure(width = math.ceil(self.font.measure(str(df[column][row]))/self.char_width))
        if row%2 == 0: self.values[column][row].configure(style = 'tktable_row0.TEntry')
        if row%2 == 1: self.values[column][row].configure(style = 'tktable_row1.TEntry')

        # ENTRY OR TEXT (index = 1.0 for text field, 0 for entry)
        self.values[column][row].insert(0, str(df[column][row]))
        if not(self.editable): self.values[column][row].configure(state = 'readonly')

        self.values[column][row].bind("<Button-1>", self.value_click)
        self.values[column][row].bind ("<FocusIn>", self.value_click)
        self.values[column][row].bind ("<Return>", self.value_changed)
        self.values[column][row].bind ("<FocusOut>", self.value_changed)
        self.values[column][row].grid(row = row + 1, column = 0, sticky = tk.N+tk.S+tk.W+tk.E)

        self.values[column][row].row = row
        self.values[column][row].column = column

    def add_row(self, row_dict):
        row_list = list()
        for column in self.df.columns:
            if column in row_dict: row_list.append(row_dict[column])
            else: row_list.append(None)
        row = 0 if pd.isnull(self.df.index.max()) else self.df.index.max() + 1
        self.df.loc[row] = row_list
        for column in self.shown_columns:
            self.values[column].append(None)
            self.create_value(row, column, self.df)
            self.frame.update()

        del row_list, row


    def value_click(self, event):
        pass
        #if self.editable:
        #    event.widget.configure(state = 'normal')
        #else:
        #    event.widget.configure(state = 'readonly')
        #print('header:', event.widget.column, 'row:', event.widget.row, 'value:', self.df[event.widget.column][event.widget.row])

    def value_changed(self, event):
        #print('I changed the value to', event.widget.get())
        self.df.loc[event.widget.row, event.widget.column] = event.widget.get()
        #print(self.df.shape)

    def del_button_clicked(self, event):
        self.deleting = True
        self.del_columns([event.widget.column])

    def header_click(self, event):
        self.header_clicked = True
        #print(self.df.loc[:, event.widget.column])
        #print(self.df.shape)
        #self.header_click_pos = event.x

    def swap_columns(self, event):
        self.header_clicked = False # header dragged, not clicked

        change = event.x# - self.header_click_pos
        column = event.widget.column
        col_pos = self.shown_columns.index(column)

        #print(self.table_frames[self.shown_columns[col_pos + 1]].winfo_width())
        if col_pos < len(self.shown_columns)-1 and change > self.table_frames[self.shown_columns[col_pos + 1]].winfo_width() + self.table_frames[self.shown_columns[col_pos]].winfo_width():
            self.record()
            col_to_swap = self.shown_columns[col_pos + 1]

            self.table_frames[col_to_swap].grid_forget()
            self.table_frames[column].grid_forget()
            self.table_frames[column].grid(row = 0, column = col_pos + 1, sticky = tk.N+tk.S+tk.E+tk.W)
            self.table_frames[col_to_swap].grid(row = 0, column = col_pos, sticky = tk.N+tk.S+tk.E+tk.W)

            self.shown_columns[col_pos] = col_to_swap
            self.shown_columns[col_pos + 1] = column

            del col_to_swap

        elif col_pos > 0 and change < -self.table_frames[self.shown_columns[col_pos - 1]].winfo_width():
            self.record()
            col_to_swap = self.shown_columns[col_pos - 1]

            self.table_frames[col_to_swap].grid_forget()
            self.table_frames[column].grid_forget()
            self.table_frames[column].grid(row = 0, column = col_pos - 1, sticky = tk.N+tk.S+tk.E+tk.W)
            self.table_frames[col_to_swap].grid(row = 0, column = col_pos, sticky = tk.N+tk.S+tk.E+tk.W)

            self.shown_columns[col_pos] = col_to_swap
            self.shown_columns[col_pos - 1] = column

            del col_to_swap

        del change, col_pos, column

    def record(self):
         self.past_cols.append(self.shown_columns)
         if len(self.past_cols) > self.history_limit:
             del self.past_cols[0]

    def revert(self):
        pass

    def set_size_factor(self):
        self.size_factor = math.ceil(len(self.shown_columns)*self.df.shape[0]/100)
        if self.size_factor > self.size_factor_limit:
            self.size_factor = self.size_factor_limit

    # sort_table sorts the entire dataframe alphabetically, not just the columns shown in the gui
    def sort_table(self, event):

        if self.header_clicked and not(self.deleting):
            # This if/else statement allows for sorting in descending order by clicking a header twice
            if self.last_sorted == event.widget.column:
                self.ascending = not(self.ascending)
            else:
                self.ascending = True

            # Sort the dataframe and record which column it was sorted by
            self.df['sort_col'] = self.df[event.widget.column].str.upper()
            self.df.sort_values(by='sort_col', ascending = self.ascending, inplace=True)
            del self.df['sort_col']

            #self.df.sort_values(by = [event.widget.column], ascending = self.ascending, inplace = True)
            self.last_sorted = event.widget.column

            self.reassign_values() # Call function that runs through all table gui elements and reassigns text

        # This boolean allows the delete button image to overlay the header (since clicking it also clicks the header)
        self.deleting = False

    # reassign_values runs through all shown table gui elements and updates their text
    def reassign_values(self):
        for column in self.shown_columns:
            row = 0
            for df_index in list(self.df.index):
                # If the table is not currently editable we must temporary allow editing for the entry so we can update the text
                self.values[column][row].configure(state = 'normal')   # Enable editing
                self.values[column][row].delete(0, tk.END)                                    # Clear the entry
                self.values[column][row].insert(0, str(self.df[column][df_index]))            # Insert the new value from the datafram
                if not(self.editable): self.values[column][row].configure(state = 'readonly') # Disable editing

                # Reset the row attribute of each entry object based on sorted indexes and move on to the next row
                self.values[column][row].row = df_index
                row += 1
            del row

    def adjust_clicked(self, event):
        self.adj_click_pos = event.x

    def resize_column(self, event):
        column = event.widget.column

        pos = event.x - self.adj_click_pos
        if pos > self.header_char_width*self.size_factor + 5:
            self.widths[column] += self.size_factor
            self.headers[column].configure(width = self.widths[column])

        if pos < -self.header_char_width*self.size_factor - 5 and self.widths[column] > 1:# self.initial_widths[column]:
            self.widths[column] -= self.size_factor
            self.headers[column].configure(width = self.widths[column])

        del column, pos

    def reset_width(self, event):
        column = event.widget.column
        self.headers[column].configure(width = self.initial_widths[column])
        del column
