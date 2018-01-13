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
        tblstmt = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, user text, chat integer)"
        #itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        #ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        #insertvalues = 
        self.conn.execute(tblstmt)
        #self.conn.execute(itemidx)
        #self.conn.execute(ownidx)
        #self.conn.execute(insertvalues)
        self.conn.execute("insert into user(user, chat) values (?, ?);", (user, chat))
        self.conn.commit()
    
    def setup(self):    
        
        
        # creating general table:
        tblgeneral = "CREATE TABLE IF NOT EXISTS general (id INTEGER PRIMARY KEY, action text, user text, category text, value integer, desconto integer, data text);"
        self.conn.execute(tblgeneral)

        # creating action table:
        tblaction = "CREATE TABLE IF NOT EXISTS action (id INTEGER PRIMARY KEY, action text);"
        self.conn.execute(tblaction)
        self.conn.execute("insert into action(action) values ('gastos');")
        self.conn.execute("insert into action(action) values ('receita');")
        
        # creating category table:
        tblaction = "CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY, category text);"
        self.conn.execute(tblaction)
        self.conn.execute("insert into category(category) values ('alimentação');")
        self.conn.execute("insert into category(category) values ('casa');")
        self.conn.execute("insert into category(category) values ('transporte');")
        self.conn.execute("insert into category(category) values ('esporte');")
        self.conn.execute("insert into category(category) values ('saude');")
        
        # Commiting
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_action(self):
        stmt = "SELECT action FROM action"
        return [x[0] for x in self.conn.execute(stmt)]
        
    def get_category(self):
        stmt = "SELECT category FROM category"
        return [x[0] for x in self.conn.execute(stmt)]
    
    def insertIncome(self, owner, value):
        stmt = "INSERT INTO general(action, user, category, value, desconto, data) VALUES ('receita', (?), 'inser categoria', (?), 0, '31/12/2018');"
        args = (owner, value)
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def insertExpenses(self, owner, value, cat):
        stmt = "INSERT INTO general(action, user, category, value, desconto, data) VALUES ('receita', (?), (?), (?), 0, '31/12/2018');"
        args = (owner, value)
        self.conn.execute(stmt, args)
        self.conn.commit()