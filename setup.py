# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 23:43:38 2018

@author: felipe
"""

import sqlite3

dbname="gastos.sqlite"
conn = sqlite3.connect(dbname)

# creating general table:
tblgeneral = "CREATE TABLE IF NOT EXISTS general (id INTEGER PRIMARY KEY, action text, user text, category text, subcategory text, value integer, date text);"
conn.execute(tblgeneral)

# Commiting
conn.commit()

# creating action table:
tblurs = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user text, chat text);"
conn.execute(tblurs)
#conn.execute("insert into action(user) values ('gastos');")
#conn.execute("insert into action(user) values ('receita');")

# Commiting
conn.commit()

# creating action table:
tblaction = "CREATE TABLE IF NOT EXISTS action (id INTEGER PRIMARY KEY, action text);"
conn.execute(tblaction)
conn.execute("insert into action(action) values ('gastos');")
conn.execute("insert into action(action) values ('receita');")

# Commiting
conn.commit()

# creating category table:
tblcategory = "CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY, category text);"
conn.execute(tblcategory)
conn.execute("insert into category(category) values ('alimentação');")
conn.execute("insert into category(category) values ('casa');")
conn.execute("insert into category(category) values ('transporte');")
conn.execute("insert into category(category) values ('esporte');")
conn.execute("insert into category(category) values ('saude');")

# Commiting
conn.commit()

# creating subcategory table:
tblscategory = "CREATE TABLE IF NOT EXISTS subcategory (id INTEGER PRIMARY KEY, subcategory text);"
conn.execute(tblscategory)
conn.execute("insert into subcategory(subcategory) values ('restaurante');")
conn.execute("insert into subcategory(subcategory) values ('supermercado');")
conn.execute("insert into subcategory(subcategory) values ('internet');")
conn.execute("insert into subcategory(subcategory) values ('luz');")
conn.execute("insert into subcategory(subcategory) values ('condominio');")
conn.execute("insert into subcategory(subcategory) values ('manutencao');")
conn.execute("insert into subcategory(subcategory) values ('onibus');")
conn.execute("insert into subcategory(subcategory) values ('gasolina');")
conn.execute("insert into subcategory(subcategory) values ('outros');")
conn.execute("insert into subcategory(subcategory) values ('gym');")
conn.execute("insert into subcategory(subcategory) values ('exames');")

# Commiting
conn.commit()

print("All Done!")