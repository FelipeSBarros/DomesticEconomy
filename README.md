# Zero Euro Bot: Chat Bot para controle financeiro
This project aims to develop a chatbot to easly save information of money spent;

### Setting up a virtualenv
```
sudo apt-get install python3-pip python3-dev python-virtualenv # for Python 3.n
virtualenv ZeroEuroBot -p python3 
source ZeroEuroBot/bin/activate
easy_install -U pip
pip install requests
sudo atp-get install python3-pandas
pip install matplotlib
```

## About Domestic Economy chatbot:  

* setup.py will create the database, tables and insert default values;  
* dbZeroEuro.py has all the functions related to the database;  
* economybot.py is the bot it self;  

### chatbot Functions
* `/start` will greeting the user, check if user is already registered in users table. If not, it will be registered;  
![start](img/start.png)  
* `/category` will show all categories already registered in the category table;  
![getting category](img/getcategory.png)  
* `/subcategory [category]` will show the subcategories related to a especific `category`;  
![getting sub category](img/getsubcat.png)  
* `/income [value]` will save the value assed as a income in the database  
![saving income](img/income.png)  
* `/expenses [value] [category] [subcategory]` will save the `value` with `category` and `subcategory` assigned in the database;  
![expenses](img/expenses.png)  
* `/summary [param] [paramII]` will return the summary of data saved on database groupping by `param`. If a second param is passed (`paramII`) the summary will be for `category` and `subcategory`;  
![expenses](img/summaryparamuser.png)  
![expenses](img/summarycategory.png)  
![expenses](img/summaryparamII.png)  
* `/plot [param]` will return a graphical (:bar_chart:) summary of data saved on database groupping by `param`.  
![plot user](img/plotuser.png)  
![plot category](img/plotcategory.png)  
![plot sub category](img/plotsubcategory.png)  

#### Useful Links  
Some links that was useful to develop this project and study python:
* [Python para impacientes](http://python-para-impacientes.blogspot.com.ar)
* [Python Anywhere](https://www.pythonanywhere.com)
* [SQLite3 Documentation](https://sqlite.org/docs.html)
* [SQLite3 Tutorials](http://www.sqlitetutorial.net/)
* [Building a telegram bot](https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay)
* [Matplotlib](https://stackoverflow.com/questions/32244019/how-to-rotate-x-axis-tick-labels-in-pandas-barplot)
* [cookbook-plotting](https://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook-plotting)
* [Pandas visualization](https://pandas.pydata.org/pandas-docs/stable/visualization.html#visualization-barplot)

### Todo list:
* make this bot availiable for group so a couple can follow what each other is inserting;
* :heavy_check_mark: make it possible to get summary/plot for a defined **month** and **year**;
* :heavy_check_mark: send backup file by e-mail;
* Change the interacion methods from comands to menus;
