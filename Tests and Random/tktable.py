# Table for use in tkinter GUI
import tkinter as tk
import numpy as np
import pandas as pd
#from ClickableTable import ClickableTable
from ClickableTable2 import ClickableTable2

dfcolumns = ['A', 'B', 'C', 'D']
dfdata = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12],
          [13, 14, 15, 16],
          [17, 18, 19, 20]]

dfeasy = pd.DataFrame(data = dfdata, columns = dfcolumns) 
testdf = pd.DataFrame(np.random.randint(0, 1000000, size=(35, 10)), columns=['A', 'BC', 'DEF', 'GHIJ', 'KLMNO', 'PQRS', 'TUV', 'WX', 'Y', 'Z'])


class MainGUI:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg = 'black')
        
        #adjcol = tk.Button(self.frame, text = 'Adjust Columns', cursor = 'sb_h_double_arrow')
            
        adjrow = tk.Entry(self.frame)
        

        self.newTable = ClickableTable2(self.frame, testdf)
        self.newTable.grid(row = 1, column = 1, sticky = tk.N+tk.S+tk.E+tk.W, padx = 10, pady = 10)
        
        tk.Grid.columnconfigure(parent, 0, weight = 1)
        tk.Grid.rowconfigure(parent, 0, weight = 1)
        
        tk.Grid.columnconfigure(self.frame, 0, weight = 0)
        tk.Grid.columnconfigure(self.frame, 1, weight = 1)
        tk.Grid.rowconfigure(self.frame, 0, weight = 0)
        tk.Grid.rowconfigure(self.frame, 1, weight = 1)
        
        self.frame.grid(row = 0, column = 0, sticky = tk.N+tk.E+tk.S+tk.W)
        #adjcol.grid(row = 0, column = 0, columnspan = 2)
        adjrow.grid(row = 1, column = 0)
        
    
                
root = tk.Tk()
app = MainGUI(root)
root.mainloop()
