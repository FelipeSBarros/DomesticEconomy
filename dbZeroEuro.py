# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:14:01 2018

@author: felipe
"""
import sqlite3


class DBHelper:
    def __init__(self, dbname="gastos.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def insertuser(self, user, chat):
        tblstmt = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user text, chat integer)"
        #itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        #ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        #self.conn.execute(itemidx)
        #self.conn.execute(ownidx)
        self.conn.execute("insert into users(user, chat) values (?, ?);", (user, chat))
        self.conn.commit()
    
    def get_action(self):
        stmt = "SELECT distinct(action) FROM general"
        return [x[0] for x in self.conn.execute(stmt)]
    
    def get_users(self):
        stmt = "SELECT distinct(user) FROM users"
        return [x[0] for x in self.conn.execute(stmt)]
        
    def get_category(self):
        stmt = "SELECT distinct(category) FROM category"
        return [x[0] for x in self.conn.execute(stmt)]
    
    def get_subcategory(self, cat = None):
        if cat:
            stmt = "SELECT distinct(subcategory) FROM subcategory WHERE category = (?) OR category = (?);"
            args = (cat, '')
            return [x[0] for x in self.conn.execute(stmt, args)]
        else:
            stmt = "SELECT distinct(subcategory) FROM subcategory"
            return [x[0] for x in self.conn.execute(stmt)]
    
    def insertExpenses(self, owner, category, subcategory, value, date):
        stmt = "INSERT INTO general(action, user, category, subcategory, value, date) VALUES ('gasto', (?), (?), (?), (?), (?));"
        args = (owner, category, subcategory, value, date)
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def insertIncome(self, owner, value, date):
        stmt = "INSERT INTO general(action, user, value, date) VALUES ('receita', (?), (?), (?));"
        args = (owner, value, date)
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def get_summary(self, param = None, paramII = None):
        if param and paramII:
            stmt = "SELECT category, subcategory, sum(value) FROM general WHERE action = 'gasto' GROUP BY category, subcategory"
            return [x for x in self.conn.execute(stmt)]
        else:
            stmt = "SELECT {}, sum(value) FROM general WHERE action = 'gasto' GROUP BY {}".format(param, param)
            return [x for x in self.conn.execute(stmt)]