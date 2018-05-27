import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from API import email, password

# Few configs
plt.style.use('ggplot')
#plt.style.use('fivethirtyeight')
plt.rcParams.update({'figure.autolayout': True})
plotwd = "plots"
# db connection
dbname="gastos.sqlite"
conn = sqlite3.connect(dbname)

# Retrieving data
df_general = pd.read_sql("SELECT general.id, action.action, users.user, category.category, subcategory.subcategory, general.value, date  FROM general INNER JOIN action on action.id = general.action INNER JOIN users on users.id = general.user INNER JOIN category on category.id = general.category INNER JOIN subcategory on subcategory.id = general.subcategory;", conn)
df_receitas = pd.read_sql("SELECT general.id, action.action, users.user, general.category, general.subcategory, general.value, date  FROM general JOIN action on action.id = general.action JOIN users on users.id = general.user WHERE action.action = 'receita'", conn)
df_completo = df_general.append(df_receitas)

# few tests
df_completo.head()
df_completo.tail()
df_completo.info() # info da tabela com informacao de tipo de dado cada coluna
df_completo.describe # estat descritiva das colunas de valor numerico
df_completo.shape # estrutura general de la tabla
df_completo.columns # para saber las columnas
df_completo["category"].unique()
df_completo["action"].unique()
#df_general["date"].value_count()
pd.isnull(df_completo)
plt.style.available

# organizing data
df_completo["date"] = pd.to_datetime(df_completo["date"]) # convetiendo string to date timestamp
df_general["date"] = pd.to_datetime(df_general["date"])
df_completo['year'] = pd.DatetimeIndex(df_completo['date']).year
df_general['year'] = pd.DatetimeIndex(df_general['date']).year
df_completo['month'] = pd.DatetimeIndex(df_completo['date']).month
df_general['month'] = pd.DatetimeIndex(df_general['date']).month
#pd.to_datetime(resultspd["date"])
#resultspd["date"] = pd.Series([pd.to_datetime(date) for date in resultspd["date"]])
df_completo.set_index(["date"], inplace = True) # actualiza el idex reemplazando en el DF si True, creando nuevo DF si False
df_general.set_index(["date"], inplace = True)

df_completo["id"].dtype.kind
df_completo["id"].dtype
df_completo["id"].head()

# action/month - Balanco
df_completo["action"].unique()
action_Month = df_completo[["action", "month", "value"]]
action_Month = action_Month.groupby(by = ["action", "month"], as_index=False).sum()
action_Month.head()
action_Month = action_Month.pivot_table(index="month", columns="action", values="value")
action_Month = action_Month.fillna(value = 0)
#pd.DataFrame(teste, index = "category")
#teste.set_index(["category"], inplace = True)
action_Month.plot()
plt.legend(loc=2, ncol=2).get_frame().set_alpha(0)
Balanco_path = os.path.join(os.getcwd(), plotwd) + '/balanco.png'
plt.savefig(Balanco_path)  # save the figure to file
plt.close()

# Category/month
gastos = df_completo.loc[df_completo["action"] == "gastos"]
cat_Month = df_general[["category", "month", "value"]]
cat_Month = cat_Month.groupby(by = ["category", "month"], as_index=False).sum()
cat_Month.head()
cat_Month = cat_Month.pivot_table(index="month", columns="category", values="value").fillna(value = 0)
#plt.subplot(211)
cat_Month.plot()
plt.legend(loc=2, ncol=2).get_frame().set_alpha(0)
#plt.legend(bbox_to_anchor=(0., 1.02, 1., 0), mode="expand", loc=2, ncol=2).get_frame().set_alpha(0)
CatMonth_path = os.path.join(os.getcwd(), plotwd) + '/CatMonth.png'
plt.savefig(CatMonth_path)  # save the figure to file
plt.close()

# user/month
user_Month = df_general[["user", "month", "value"]]
user_Month = user_Month.groupby(by = ["user", "month"], as_index=False).sum()
user_Month.head()
user_Month = user_Month.pivot_table(index="month", columns="user", values="value").fillna(value = 0)
user_Month.plot()
plt.legend(loc=2, ncol=2).get_frame().set_alpha(0)
UsrMonth_path = os.path.join(os.getcwd(), plotwd) + '/UsrMonth_path.png'
plt.savefig(UsrMonth_path)  # save the figure to file
plt.close()

# user_Month.boxplot(by="month")
# user_Month.boxplot(x='month',data=user_Month,hue='fruits')

# Creating PDF

from jinja2 import Environment, FileSystemLoader
import pdfkit

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("Template.html")
month_name = datetime.date.today().strftime("%b")
template_vars = {"month_name": month_name, "year": datetime.date.today().strftime("%Y"), "title" : "Teste Felipe Report", "balanco": Balanco_path , "CatMonth": CatMonth_path, "UsrMonth": UsrMonth_path}

html_out = template.render(template_vars)

pdfkit.from_string(html_out, output_path="out.pdf")

# Sending Report by e-mail
use_tls = True
send_from = email
send_to = email
subject = 'Domestic Economy Report' + month_name
backup_file = os.path.join("./", os.path.basename("out.pdf"))
files = [backup_file]
server = 'smtp.gmail.com'
port = 587
message = "Olá, segue relatório de " + month_name
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = email
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject

msg.attach(MIMEText(message))

for path in files:
    part = MIMEBase('application', "octet-stream")
    with open(path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="{}"'.format(os.path.basename(path)))
    msg.attach(part)

smtp = smtplib.SMTP(server, port)
if use_tls:
    smtp.starttls()
smtp.login(email, password)
smtp.sendmail(send_from, send_to, msg.as_string())
smtp.quit()