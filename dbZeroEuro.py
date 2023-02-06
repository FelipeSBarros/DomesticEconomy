# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:14:01 2018

@author: felipe
"""
import os
import shutil
import smtplib
import sqlite3
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import dotenv_values

EMAIL = dotenv_values()["email"]
PASSWORD = dotenv_values()["password"]


class DBHelper:
    def __init__(self, dbname="gastos.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def insertuser(self, user, chat):
        tblstmt = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user text, chat integer)"
        # itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        # ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        # self.conn.execute(itemidx)
        # self.conn.execute(ownidx)
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

    def get_subcategory(self, cat=None):
        if cat:
            stmt = "SELECT distinct(subcategory) FROM subcategory WHERE catid = (SELECT id from category where category = (?)) OR category = (?);"
            args = (cat, "")
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

    def get_summary(self, param=None, month=None, year=None):
        if param == "category":
            stmt = "SELECT category, total from view_catsummary where month = '{}' and year = '{}' ORDER BY 2 DESC".format(
                month, year
            )
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(results, columns=("*Category*", "*Total*"))
            return results
        elif param == "subcategory":
            stmt = "SELECT category, subcategory, total from view_scatsummary where month = '{}' and year = '{}' ORDER BY 2 DESC".format(
                month, year
            )
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(
                results, columns=("*Category*", "*Subcategory*", "*Total*")
            )
            return results
        elif param == "user":
            stmt = "SELECT user, total from view_usersummary where month = '{}' and year = '{}' ORDER BY 2 DESC".format(
                month, year
            )
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(results, columns=("*User*", "*Total*"))
            return results
        elif param == "balance":
            stmt = "SELECT action, total from view_action where month = '{}' and year = '{}' ORDER BY 2 DESC".format(
                month, year
            )
            results = self.conn.execute(stmt).fetchall()
            results = pd.DataFrame(results, columns=("*Movimento*", "*Total*"))
            return results
        else:
            msg = ["Not found: {}".format(param)]
            return msg

    def get_plots(self, param=None, month=None, year=None):
        # Few configs
        plt.style.use("ggplot")
        # plt.style.use('fivethirtyeight')
        plotwd = "plots"
        plt.rcParams.update({"figure.autolayout": True})
        if not os.path.exists(plotwd):
            os.makedirs(plotwd)
        if param == "category":
            CatPlot = pd.read_sql(
                "SELECT category, total from view_catsummary WHERE month = '{}' and year = '{}' ORDER BY 2 DESC".format(
                    month, year
                ),
                self.conn,
            )
            CatPlot.plot.bar(x="category", y="total", legend=False, rot=7)
            path = os.path.join(os.getcwd(), plotwd) + "/Category_plot.png"
            plt.savefig(path)  # save the figure to file
            plt.close()
            return str(path)
        elif param == "subcategory":
            SubCatPlot = pd.read_sql(
                "SELECT category, subcategory, total from view_scatsummary WHERE month = '{}' and year = '{}' ORDER BY 3 DESC".format(
                    month, year
                ),
                self.conn,
            )
            SubCatPlot["SubCategorias"] = (
                SubCatPlot.category + " " + SubCatPlot.subcategory
            )
            SubCatPlot.plot.bar(x="SubCategorias", y="total", legend=False, rot=90)
            path = os.path.join(os.getcwd(), plotwd) + "/SubCategory_plot.png"
            plt.savefig(path)  # save the figure to file
            plt.close()
            return str(path)
        elif param == "user":
            UserPlot = pd.read_sql(
                "SELECT user, total from view_usersummary WHERE month = '{}' and year = '{}' ORDER BY 2 DESC".format(
                    month, year
                ),
                self.conn,
            )
            UserPlot.pivot_table(columns="user").plot.bar(legend=True, rot=0)
            path = os.path.join(os.getcwd(), plotwd) + "/User_plot.png"
            plt.savefig(path)  # save the figure to file
            plt.close()
            return str(path)
        elif param == "historico":
            # Retrieving data
            df_general = pd.read_sql(
                "SELECT general.id, action.action, users.user, category.category, subcategory.subcategory, general.value, date  FROM general INNER JOIN action on action.id = general.action INNER JOIN users on users.id = general.user INNER JOIN category on category.id = general.category INNER JOIN subcategory on subcategory.id = general.subcategory;",
                self.conn,
            )
            df_receitas = pd.read_sql(
                "SELECT general.id, action.action, users.user, general.category, general.subcategory, general.value, date  FROM general JOIN action on action.id = general.action JOIN users on users.id = general.user WHERE action.action = 'receita'",
                self.conn,
            )
            df_completo = df_general.append(df_receitas)

            # organizing data
            df_completo["date"] = pd.to_datetime(df_completo["date"])
            df_general["date"] = pd.to_datetime(df_general["date"])
            df_completo["year"] = pd.DatetimeIndex(df_completo["date"]).year
            df_general["year"] = pd.DatetimeIndex(df_general["date"]).year
            df_completo["month"] = pd.DatetimeIndex(df_completo["date"]).month
            df_general["month"] = pd.DatetimeIndex(df_general["date"]).month
            df_completo.set_index(["date"], inplace=True)
            df_general.set_index(["date"], inplace=True)

            # Domestic Balance
            action_Month = df_completo[["action", "month", "value"]]
            action_Month = action_Month.groupby(
                by=["action", "month"], as_index=False
            ).sum()
            action_Month = action_Month.pivot_table(
                index="month", columns="action", values="value"
            ).fillna(value=0)
            action_Month.plot()
            plt.legend(loc=2, ncol=2).get_frame().set_alpha(0)
            Balanco_path = os.path.join(os.getcwd(), plotwd) + "/balanco.png"
            plt.savefig(Balanco_path)  # save the figure to file
            plt.close()

            # Category/month
            cat_Month = df_general[["category", "month", "value"]]
            cat_Month = cat_Month.groupby(
                by=["category", "month"], as_index=False
            ).sum()
            cat_Month = cat_Month.pivot_table(
                index="month", columns="category", values="value"
            ).fillna(value=0)
            cat_Month.plot()
            plt.legend(loc=2, ncol=3).get_frame().set_alpha(0)
            CatMonth_path = os.path.join(os.getcwd(), plotwd) + "/CatMonth.png"
            plt.savefig(CatMonth_path)  # save the figure to file
            plt.close()

            # user/month
            user_Month = df_general[["user", "month", "value"]]
            user_Month = user_Month.groupby(by=["user", "month"], as_index=False).sum()
            user_Month = user_Month.pivot_table(
                index="month", columns="user", values="value"
            ).fillna(value=0)
            user_Month.plot()
            plt.legend(loc=2, ncol=2).get_frame().set_alpha(0)
            UsrMonth_path = os.path.join(os.getcwd(), plotwd) + "/UsrMonth_path.png"
            plt.savefig(UsrMonth_path)  # save the figure to file
            plt.close()
            return [Balanco_path, CatMonth_path, UsrMonth_path]
        else:
            path = "Not found: {}".format(param)
            return str(path)

    # Function to mannage SQL from message
    def sql(self, sql):
        if sql.upper().startswith("ALTER TABLE"):
            msg = "ALTER TABLE NOT ALLOWED BY MSG"
            return msg
        elif sql.upper().startswith("DROP"):
            msg = "DROP [TABLE/VIEW] NOT ALLOWED BY MSG"
            return msg
        elif sql.upper().startswith("SELECT"):
            res = self.conn.execute(sql).fetchall()
            res = pd.DataFrame(res)
            return res
        else:
            self.conn.execute(sql)
            self.conn.commit()
            msg = "All done!"
            return msg

            # Database Backup function

    def sqlite3_backup(
        self, dbfile="gastos.sqlite", backupdir="./backup", use_tls=True
    ):
        # Create backupdir if not exist
        if not os.path.isdir(backupdir):
            os.makedirs(backupdir)
        # Create timestamped database copy
        backup_file = os.path.join(
            backupdir, os.path.basename(dbfile) + time.strftime("-%Y%m%d-%H%M%S")
        )

        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Lock database before making a backup
        # cursor.execute('begin immediate')
        # Make new backup file
        shutil.copyfile(dbfile, backup_file)
        print("\nCreating {}...".format(backup_file))
        # Unlock database
        # connection.rollback()
        # backupMail.send_mail(send_from = yauser, send_to = dba, text = backup_file, files = backup_file)
        # import backupMail  # function to send backup by email
        # Clean old backup function

        # sending backup by email
        send_from = EMAIL
        send_to = EMAIL
        subject = "BACKUP_" + os.path.basename(backup_file)
        files = [backup_file]
        server = "smtp.gmail.com"
        port = 587
        message = backup_file
        """Compose and send email with provided info and attachments.
    
        Args:
            send_from (str): from name
            send_to (str): to name
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            server (str): mail server host name
            port (int): port number
            username (str): server auth username
            password (str): server auth password
            use_tls (bool): use TLS mode
            src: https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
        """
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase("application", "octet-stream")
            with open(path, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                'attachment; filename="{}"'.format(os.path.basename(path)),
            )
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(EMAIL, PASSWORD)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()

    # Function to remove old backupfiles
    def clean_data(slef, backup_dir="./backup", NO_OF_DAYS=7):
        """Delete files older than NO_OF_DAYS days"""

        print("\n------------------------------")
        print("Cleaning up old backups")

        for filename in os.listdir(backup_dir):
            backup_file = os.path.join(backup_dir, filename)
            if os.path.isfile(backup_file):
                if os.stat(backup_file).st_ctime < (time.time() - NO_OF_DAYS * 86400):
                    os.remove(backup_file)
                    print("Deleting {}...".format(backup_file))
