# Zero Euro Bot: Chat Bot para controle financeiro
This project aims to develop a chatbot to easly save information of money spent;

### Setting up a virtualenv
```
sudo apt-get install python3-pip python3-dev python-virtualenv # for Python 3.n
virtualenv ZeroEuroBot -p python3 
source ZeroEuroBot/bin/activate
easy_install -U pip
pip install requests
```

## About Domestic Economy chatbot:  

* setup.py will create the database, tables and insert default values;  
* dbZeroEuro.py has all the functions related to the database;  
* economibot.py is the bot it self;  

### chatbot Functions
`/start` will greeting the user, check if user is already registered in users table. If not, it will be registered;  
![start](img/start.png)
`/category` will show all categories already registered in the category table;  
`/subcategory` will do the same for subcategory table;  

**NOTE:** The database is note relational yet. I need to work on that too. All data are saved on general table
