# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 23:43:38 2018

@author: felipe
"""

import sqlite3

dbname="gastos.sqlite"
conn = sqlite3.connect(dbname)

# creating general table:
tblgeneral = "CREATE TABLE IF NOT EXISTS general (id INTEGER PRIMARY KEY, action text, user text, category text, subcategory text, value REAL, date text);"
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
conn.execute("insert into category(category) values ('burocracia');")
conn.execute("insert into category(category) values ('compras');")

# Commiting
conn.commit()

# creating subcategory table:
tblscategory = "CREATE TABLE IF NOT EXISTS subcategory (id INTEGER PRIMARY KEY, catid integer, subcategory text, category text);"
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