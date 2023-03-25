import sqlite3
import os

def toDictTransactions(t):
    ''' t is a tuple (rowid, item #, amount, category, date, description)'''
    # TODO The lesson 19 code came with this print line, I don't know if we want it or not
    # print('t='+str(t))
    # TODO check that this works
    transaction = {'item #': t[0], 'amount': t[1], 'category': t[2], 'date': t[3], 'description': t[4]}
    return transaction

def toDictCategories(c):
    ''' t is a tuple (rowid, item #, amount, category, date, description)'''
    # TODO The lesson 19 code came with this print line, I don't know if we want it or not
    # print('t='+str(t))
    # TODO check that this works
    category = { 'id': c[0], 'name': c[1] }
    return category

class Transaction:
    # initializes a transaction object. filename should lead to the db file we want this transaction object to be linked to
    def __init__(self, filename):
        self.filename = filename
        # ERROR HERE, I think there is a syntax error in this line?
        self.runQuery('''CREATE TABLE IF NOT EXISTS transactions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, amount real, category integer, date text, description text)''',())
        # This initializes an sql database that just has all of the categories for the main database
        # TODO check that this creates the correct table
        self.runCategoryQuery('''CREATE TABLE IF NOT EXISTS categories
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, name text)''',())
    
    # Run this method if you want to query through the catagory table
    def runCategoryQuery(self, query, tuple):
        con= sqlite3.connect(os.getenv('HOME') + "/" + self.filename)
        cur = con.cursor() 
        cur.execute(query,tuple)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        print(tuples)
        # TODO check that this returns the category names
        return [toDictCategories(c) for c in tuples]

    # Run this method if you want to query through the main table
    def runQuery(self,query,tuple):
        ''' return all of the transactions as a list of dicts.'''
        con= sqlite3.connect(os.getenv('HOME') + "/" + self.filename)
        cur = con.cursor()
        cur.execute(query,tuple)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return [toDictTransactions(t) for t in tuples]
    
    
################## MinSung ####################
    def add_transaction(self, details):
        ''' Add transaction entry '''
        return self.runQuery("INSERT INTO transactions (amount, category, date, description) VALUES(?,?,?,?);", (details["amount"], details["category"], details["date"], details["description"]))
    
    def check_category_exists(self, category):
        """ Check if category already exists in categories table """
        con= sqlite3.connect(os.getenv('HOME') + "/" + self.filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM categories WHERE name = ?", (category,))
        data = cur.fetchone()
        con.commit()
        con.close()
        if data is None:
            return False
        return True
        # exists = self.runQuery("SELECT EXISTS(SELECT 1 FROM categories WHERE name= ? );", (category))
        # return exists
    
    def add_category(self, category):
        """ Add category entry to categories table """
        return self.runQuery("INSERT INTO categories (name) VALUES (?);", (category,))
    
###############################################

#################### Rose #####################
    def show_transactions(self):
        return self.runQuery("SELECT * FROM transactions;", ())
    
    def show_categories(self):
        return self.runCategoryQuery("SELECT * FROM categories;", ())
###############################################
