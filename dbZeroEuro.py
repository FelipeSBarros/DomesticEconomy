# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:14:01 2018

@author: felipe
"""
import sqlite3
import shutil
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime

class DBHelper:
    def __init__(self, dbname="gastos.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def insertuser(self, user, chat):
        tblstmt = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user text, chat integer)"
        #itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        #ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        #self.conn.execute(itemidx)
        #self.conn.execute(ownidx)
        self.conn.execute("insert into users(user, chat) values (?, ?);", (user, chat))
        self.conn.commit()
    
    def get_action(self):
        stmt = "SELECT distinct(action) FROM action"
        return [x[0] for x in self.conn.execute(stmt)]
    
    def get_users(self):
        stmt = "SELECT distinct(user) FROM users"
        return [x[0] for x in self.conn.execute(stmt)]
        
    def get_category(self):
        stmt = "SELECT distinct(category) FROM category"
        return [x[0] for x in self.conn.execute(stmt)]
    
    def get_subcategory(self, cat = None):
        if cat:
            stmt = "SELECT distinct(subcategory) FROM subcategory WHERE catid = (SELECT id from category where category = (?)) OR category = (?);"
            args = (cat, '')
            return [x[0] for x in self.conn.execute(stmt, args)]
        else:
            stmt = "SELECT distinct(subcategory) FROM subcategory"
            return [x[0] for x in self.conn.execute(stmt)]
    
    def insertExpenses(self, owner, category, subcategory, value, date):
        stmt = "INSERT INTO general(action, user, category, subcategory, value, date) VALUES ((SELECT id from action where action = 'gastos'), (select id from users where user = (?)), (select id from category where category = (?)), (select id from subcategory where subcategory = (?)), (?), (?));"
        args = (owner, category, subcategory, value, date)
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def insertIncome(self, owner, value, date):
        stmt = "INSERT INTO general(action, user, value, date) VALUES ((SELECT id from action where action = 'receita'), (select id from users where user = (?)), (?), (?));"
        args = (owner, value, date)
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def get_summary(self, param = None, month = None, year = None):
        if param == 'category':
            stmt = "SELECT category, total from view_catsummary where month = '{}' and year = '{}' ORDER BY 2 DESC".format(month, year)
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(results, columns = ('*Category*', '*Total*'))
            return results
        elif param == 'subcategory':
            stmt = "SELECT category, subcategory, total from view_scatsummary where month = '{}' and year = '{}' ORDER BY 2 DESC".format(month, year)
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(results, columns = ('*Category*', '*Subcategory*', '*Total*'))
            return results
        elif param == 'user':
            stmt = "SELECT user, total from view_usersummary where month = '{}' and year = '{}' ORDER BY 2 DESC".format(month, year)
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(results, columns = ('*User*', '*Total*'))
            return results
        else:
            msg = ["Not found: {}".format(param)]
            return msg
            
    def get_plots(self, param = None, month = None, year = None):
        plt.style.use('ggplot')
        plotwd = "plots"
        plt.rcParams.update({'figure.autolayout': True})
        if not os.path.exists(plotwd):
            os.makedirs(plotwd)
        if param == 'category':
            stmt = "SELECT category, total from view_catsummary WHERE month = '{}' and year = '{}' ORDER BY 2 DESC".format(month, year)
            res = self.conn.execute(stmt)
            res = res.fetchall()
            colnames = ("Categorias", "Value")
            res = pd.DataFrame(res, columns=colnames)
            res.plot.bar(x="Categorias", y="Value", legend = False, rot=7)
            path = os.path.join(os.getcwd(), plotwd) + '/Category_{}_{}.png'.format(month, year)
            plt.savefig(path)  # save the figure to file
            plt.close()
            return str(path)
        elif param == 'subcategory':
            stmt = "SELECT category, subcategory, total from view_scatsummary WHERE month = '{}' and year = '{}' ORDER BY 3 DESC".format(month, year)
            res = self.conn.execute(stmt)
            res = res.fetchall()
            colnames = ("Cat", "SubCat", "Value")
            res = pd.DataFrame(res, columns=colnames)
            res["SubCategorias"] = res.Cat + " " + res.SubCat
            res.plot.bar(x = "SubCategorias", y = "Value", legend = False, rot=90)
            path = os.path.join(os.getcwd(), plotwd) + '/SubCategory_{}_{}.png'.format(month, year)
            plt.savefig(path)  # save the figure to file
            plt.close()
            return str(path)
        elif param == 'user':
            stmt = "SELECT user, total from view_usersummary WHERE month = '{}' and year = '{}' ORDER BY 2 DESC".format(month, year)
            res = self.conn.execute(stmt)
            res = res.fetchall()
            colnames = ("User", "Value")
            res = pd.DataFrame(res, columns=colnames)
            res.plot.bar(x="User", y="Value", legend = False, rot=0)
            path = os.path.join(os.getcwd(), plotwd) + '/User_{}_{}.png'.format(month, year)
            plt.savefig(path)  # save the figure to file
            plt.close()
            return str(path)
        else:
            path = "Not found: {}".format(param)
            return str(path)

    # Database Backup function
    def sqlite3_backup(self, dbfile = 'gastos.sqlite', backupdir = './backup'):
        """Create timestamped database copy"""
    
        if not os.path.isdir(backupdir):
            os.makedirs(backupdir)
    
        backup_file = os.path.join(backupdir, os.path.basename(dbfile) + time.strftime("-%Y%m%d-%H%M%S"))
    
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()
    
        # Lock database before making a backup
        #cursor.execute('begin immediate')
        # Make new backup file
        shutil.copyfile(dbfile, backup_file)
        print ("\nCreating {}...".format(backup_file))
        # Unlock database
        #connection.rollback()
        #backupMail.send_mail(send_from = yauser, send_to = dba, text = backup_file, files = backup_file)
        #import backupMail  # function to send backup by email
        # Clean old backup function
    def clean_data(slef, backup_dir = './backup', NO_OF_DAYS = 7):
        """Delete files older than NO_OF_DAYS days"""
    
        print ("\n------------------------------")
        print ("Cleaning up old backups")
    
        for filename in os.listdir(backup_dir):
            backup_file = os.path.join(backup_dir, filename)
            if os.path.isfile(backup_file):
                if os.stat(backup_file).st_ctime < (time.time() - NO_OF_DAYS * 86400):
                    os.remove(backup_file)
                    print ("Deleting {}...".format(backup_file))
