import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Few configs
plt.style.use('ggplot')
plt.style.use('')
plt.rcParams.update({'figure.autolayout': True})
#plotwd = "plots"
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

# action/month
df_completo["action"].unique()
action_Month = df_completo[["action", "month", "value"]]
action_Month = action_Month.groupby(by = ["action", "month"], as_index=False).sum()
action_Month.head()
action_Month = action_Month.pivot_table(index="month", columns="action", values="value")
action_Month = action_Month.fillna(value = 0)
#pd.DataFrame(teste, index = "category")
#teste.set_index(["category"], inplace = True)
action_Month.plot()

# Category/month
gastos = df_completo.loc[df_completo["action"] == "gastos"]
cat_Month = df_general[["category", "month", "value"]]
cat_Month = cat_Month.groupby(by = ["category", "month"], as_index=False).sum()
cat_Month.head()
cat_Month = cat_Month.pivot_table(index="month", columns="category", values="value").fillna(value = 0)
cat_Month.plot()

# user/month
user_Month = df_general[["user", "month", "value"]]
user_Month = user_Month.groupby(by = ["user", "month"], as_index=False).sum()
user_Month.head()
user_Month = user_Month.pivot_table(index="month", columns="user", values="value").fillna(value = 0)
user_Month.plot()