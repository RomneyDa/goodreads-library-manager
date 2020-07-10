# =============================================================================
# 
# cur.executescript('''
#      DROP TABLE IF EXISTS Library;
# 
#      CREATE TABLE Library (
#          id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#          goodreads_id               INTEGER,
#          title                      TEXT,
#          author                     TEXT,
#          author_lastfirst           TEXT,
#          additional_authors         TEXT,
#          ISBN                       TEXT,
#          ISBN13                     TEXT,
#          my_rating                  INTEGER,
#          average_rating             REAL,
#          publisher                  TEXT,
#          binding                    TEXT,
#          number_of_pages            INTEGER,
#          year_published             INTEGER,
#          original_publication_year  TEXT,
#          date_read                  TEXT,
#          date_added                 TEXT,
#          bookshelves                TEXT,
#          bookshelves_with_positions TEXT,
#          exclusive_shelf            TEXT,
#          review                     TEXT,
#          spoiler                    TEXT,
#          private_notes              TEXT,
#          read_count                 INTEGER,
#          recommended_for            TEXT,
#          recommended_by             TEXT,
#          owned_copies               INTEGER,
#          original_purchase_date     TEXT,
#          original_purchase_location TEXT,
#          condition                  TEXT,
#          condition_description      TEXT,
#          BCID                       TEXT
#      );
#  ''')
# =============================================================================

# AUTOMATIC MAPPING ===================================================
# with open(filename) as csvFile:
#     readCSV = csv.reader(csvFile, delimiter = ',')
#     firstRow = True
#     data = []
#     for row in readCSV:
#         if firstRow: 
#             headers = row
#             firstRow = False
#         else:
#             data.append(row)
# 
# print(headers)
# 
# headerDict = {'header':0 for header in headers}
# for field in headers:
#     try:
#         val = float(data[0][headers.index(field)])
#         headerDict[field] = 'NUM'
#     except:
#         headerDict[field] = 'TEXT'
# =====================================================================

# # MANUAL MAPPING ===================================================
# headers = {
#      'Book Id'                   : 'INTEGER',
#      'Title'                     : 'TEXT',
#      'Author'                    : 'TEXT',
#      'Author l-f'                : 'TEXT',
#      'Additional Authors'        : 'TEXT',
#      'ISBN'                      : 'TEXT',
#      'ISBN13'                    : 'TEXT',
#      'My Rating'                 : 'INTEGER',
#      'Average Rating'            : 'REAL',
#      'Publisher'                 : 'TEXT',
#      'Binding'                   : 'TEXT',
#      'Number of Pages'           : 'INTEGER',
#      'Year Published'            : 'INTEGER',
#      'Original Publication Year' : 'TEXT',
#      'Date Read'                 : 'TEXT',
#      'Date Added'                : 'TEXT',
#      'Bookshelves'               : 'TEXT',
#      'Bookshelves with positions': 'TEXT',
#      'Exclusive Shelf'           : 'TEXT',
#      'My Review'                 : 'TEXT',
#      'Spoiler'                   : 'TEXT',
#      'Private Notes'             : 'TEXT',
#      'Read Count'                : 'INTEGER',
#      'Recommended For'           : 'TEXT',
#      'Recommended By'            : 'TEXT',
#      'Owned Copies'              : 'INTEGER',
#      'Original Purchase Date    ': 'TEXT',
#      'Original Purchase Location': 'TEXT',
#      'Condition'                 : 'TEXT',
#      'Condition Description'     : 'TEXT',
#      'BCID'                      : 'TEXT'
#  }
#
# data = []
# with open(filename) as csvFile:
#     readCSV = csv.reader(csvFile, delimiter = ',')
#     firstRow = True
#     for row in readCSV:
#         if firstRow:
#             firstRow = False
#             continue
#         else:
#             data.append(row)
#
# # =====================================================================

# =============================================================================
#     
# cur.executescript('''
#     DROP TABLE IF EXISTS Books;
#     
#     CREATE TABLE Books (
#         id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#         name    TEXT UNIQUE
#     );
#     
#     CREATE TABLE Genre (
#         id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#         name    TEXT UNIQUE
#     );
#     
#     CREATE TABLE Album (
#         id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#         artist_id  INTEGER,
#         title   TEXT UNIQUE
#     );
#     
#     CREATE TABLE Track (
#         id  INTEGER NOT NULL PRIMARY KEY 
#             AUTOINCREMENT UNIQUE,
#         title TEXT  UNIQUE,
#         album_id  INTEGER,
#         genre_id  INTEGER,
#         len INTEGER, rating INTEGER, count INTEGER
#     )
# ''')
# =============================================================================
        


# =============================================================================
# headers = [
#     {'name':"goodreads_id",               'csv_name':'Book Id',                    'type':'INTEGER'},
#     {'name':"title",                      'csv_name':'Title',                      'type':'TEXT'},
#     {'name':"author",                     'csv_name':'Author',                     'type':'TEXT'},
#     {'name':"author_lastfirst",           'csv_name':'Author l-f',                 'type':'TEXT'},
#     {'name':"additional_authors",         'csv_name':'Additional Authors',         'type':'TEXT'},
#     {'name':"ISBN",                       'csv_name':'ISBN',                       'type':'TEXT'},
#     {'name':"ISBN13",                     'csv_name':'ISBN13',                     'type':'TEXT'},
#     {'name':"my_rating",                  'csv_name':'My Rating',                  'type':'INTEGER'},
#     {'name':"average_rating",             'csv_name':'Average Rating',             'type':'REAL'},
#     {'name':"publisher",                  'csv_name':'Publisher',                  'type':'TEXT'},
#     {'name':"binding",                    'csv_name':'Binding',                    'type':'TEXT'},
#     {'name':"number_of_pages",            'csv_name':'Number of Pages',            'type':'INTEGER'},
#     {'name':"year_published",             'csv_name':'Year Published',             'type':'INTEGER'},
#     {'name':"original_publication_year",  'csv_name':'Original Publication Year',  'type':'INTEGER'},
#     {'name':"date_read",                  'csv_name':'Date Read',                  'type':'TEXT'},
#     {'name':"date_added",                 'csv_name':'Date Added',                 'type':'TEXT'},
#     {'name':"bookshelves",                'csv_name':'Bookshelves',                'type':'TEXT'},
#     {'name':"bookshelves_with_positions", 'csv_name':'Bookshelves with positions', 'type':'TEXT'},
#     {'name':"exclusive_shelf",            'csv_name':'Exclusive Shelf',            'type':'TEXT'},
#     {'name':"review",                     'csv_name':'My Review',                  'type':'TEXT'},
#     {'name':"spoiler",                    'csv_name':'Spoiler',                    'type':'TEXT'},
#     {'name':"private_notes",              'csv_name':'Private Notes',              'type':'TEXT'},
#     {'name':"read_count",                 'csv_name':'Read Count',                 'type':'INTEGER'},
#     {'name':"recommended_for",            'csv_name':'Recommended For',            'type':'TEXT'},
#     {'name':"recommended_by",             'csv_name':'Recommended By',             'type':'TEXT'},
#     {'name':"owned_copies",               'csv_name':'Owned Copies',               'type':'INTEGER'},
#     {'name':"original_purchase_date",     'csv_name':'Original Purchase Date',     'type':'TEXT'},
#     {'name':"original_purchase_location", 'csv_name':'Original Purchase Location', 'type':'TEXT'},
#     {'name':"condition",                  'csv_name':'Condition',                  'type':'TEXT'},
#     {'name':"condition_description",      'csv_name':'Condition Description',      'type':'TEXT'},
#     {'name':"BCID",                       'csv_name':'BCID',                       'type':'TEXT'}
#     for header in headers:
#    cur.execute('ALTER TABLE Library ADD ? TEXT', (header['name'], ))
#
# ]
# =============================================================================