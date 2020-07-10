# SQL Functions for the Goodreads library
import sqlite3
import pandas as pd

def csvtosqlite(csvname, dbname, tablename):
    
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