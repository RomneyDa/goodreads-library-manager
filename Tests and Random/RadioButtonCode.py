# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:06:09 2020

@author: Dalli
"""

        self.replace_file_val = tk.IntVar(self.parent) 
        self.update_file_val = tk.IntVar(self.parent)
        
        self.update_radio_csv = ttk.Radiobutton(self.frame, text = 'From CSV', variable = self.update_file_val, value = 0)
        self.update_radio_db = ttk.Radiobutton(self.frame, text = 'From SQLITE', variable = self.update_file_val, value = 1)
        self.update_radio_csv.invoke()
        
        self.replace_radio_csv = ttk.Radiobutton(self.frame, text = 'From CSV',   variable = self.replace_file_val, value = 0)
        self.replace_radio_db = ttk.Radiobutton(self.frame, text = 'From SQLITE', variable = self.replace_file_val, value = 1)
        self.replace_radio_csv.invoke()
        self.update_radio_csv.grid(row = 2, column = 0, padx = 10, pady = 5,sticky = tk.W)
        self.update_radio_db.grid(row = 3, column = 0, padx = 10, pady = 5,sticky = tk.W)
        self.replace_radio_csv.grid(row = 2, column = 1, padx = 10, pady = 5,sticky = tk.W)
        self.replace_radio_db.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = tk.W)