# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 23:43:38 2018

@author: felipe
"""

import sqlite3

dbname="gastos.sqlite"
conn = sqlite3.connect(dbname)

# creating general table:
tblgeneral = "CREATE TABLE IF NOT EXISTS general (id INTEGER PRIMARY KEY AUTOINCREMENT, action integer, user integer, category integer, subcategory integer, value REAL, date text, FOREIGN KEY (action) REFERENCES action(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY (category) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY (subcategory) REFERENCES subcategory(id) ON DELETE CASCADE ON UPDATE CASCADE);"
conn.execute(tblgeneral)
Indxgeneral = "CREATE INDEX indiceForeignKeys ON general (action, user, category, subcategory);"
conn.execute(Indxgeneral)
# Commiting
conn.commit()

# creating users table:
tblurs = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user text, chat text);"
conn.execute(tblurs)
conn.execute("insert into users(user) values ('gastos');")
conn.execute("insert into users(user) values ('receita');")

# Commiting
conn.commit()

# creating action table:
tblaction = "CREATE TABLE IF NOT EXISTS action (id INTEGER PRIMARY KEY AUTOINCREMENT, action text);"
conn.execute(tblaction)
conn.execute("insert into action(action) values ('gastos');")
conn.execute("insert into action(action) values ('receita');")

# Commiting
conn.commit()

# creating category table:
tblcategory = "CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY AUTOINCREMENT, category text);"
conn.execute(tblcategory)
conn.execute("insert into category(category) values ('alimentacao');")
conn.execute("insert into category(category) values ('casa');")
conn.execute("insert into category(category) values ('transporte');")
conn.execute("insert into category(category) values ('esporte');")
conn.execute("insert into category(category) values ('saude');")
conn.execute("insert into category(category) values ('burocracia');")
conn.execute("insert into category(category) values ('compras');")

# Commiting
conn.commit()

# creating subcategory table:
tblscategory = "CREATE TABLE IF NOT EXISTS subcategory (id INTEGER PRIMARY KEY AUTOINCREMENT, catid integer, subcategory text, category text, FOREIGN KEY (catid) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE);"
conn.execute(tblscategory)
conn.execute("insert into subcategory(catid, subcategory, category) values (1, 'restaurante', 'alimentacao');")
conn.execute("insert into subcategory(catid, subcategory, category) values (1, 'supermercado', 'alimentacao');")
conn.execute("insert into subcategory(catid, subcategory, category) values (2, 'internet', 'casa');")
conn.execute("insert into subcategory(catid, subcategory, category) values (2, 'luz', 'casa');")
conn.execute("insert into subcategory(catid, subcategory, category) values (2, 'condominio', 'casa');")
conn.execute("insert into subcategory(catid, subcategory, category) values (2, 'telefone', 'casa');")
conn.execute("insert into subcategory(catid, subcategory, category) values (2, 'aluguel', 'casa');")
conn.execute("insert into subcategory(catid, subcategory, category) values (2, 'manutencao', 'casa');")
conn.execute("insert into subcategory(catid, subcategory, category) values (3, 'onibus', 'transporte');")
conn.execute("insert into subcategory(catid, subcategory, category) values (3, 'gasolina', 'transporte');")
conn.execute("insert into subcategory(catid, subcategory, category) values (3, 'taxi', 'transporte');")
conn.execute("insert into subcategory(catid, subcategory, category) values (4, 'gym', 'esporte');")
conn.execute("insert into subcategory(catid, subcategory, category) values (5, 'exames', 'saude');")
conn.execute("insert into subcategory(catid, subcategory, category) values (5, 'farmacia', 'saude');")
conn.execute("insert into subcategory(catid, subcategory, category) values (6, 'monotributo', 'burocracia');")
conn.execute("insert into subcategory(catid, subcategory, category) values (0, 'outros', '');")

# Commiting
conn.commit()

print("All Done!")