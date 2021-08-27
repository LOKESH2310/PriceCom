from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from autoscraper import AutoScraper
import pandas as pd
import time



# creating object and loading
amazon_scraper = AutoScraper()
amazon_scraper.load('amazon.json')

app = Flask(__name__, template_folder="clients/templates", static_folder="clients/static")

app.secret_key = 'pycharm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MSlokesh23'
app.config['MYSQL_DB'] = 'pricecomparisionlogin'

mysql = MySQL(app)

# @app.route('/')
# def upload_file():
#     return render_template("index.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			# change = username
			return render_template('login.html')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)

@app.route("/", methods=['GET'])
def home():
    # when user search it
    if request.args.get('search'):
        # inputs
        search = request.args.get('search')
        sortby = request.args.get('sortby', 'relevanceblender')

        # call function to retrieve data
        search_data, original_url = searchquery(search, sortby)

        data_length = len(search_data)

        # show to user
        return render_template("index.html", data={'original_url': original_url, 'query': search, 'sortby': sortby,
                                                   'searchData': search_data, 'totalRecords': data_length})

        # default data_length when no search
    data_length = -1
    return render_template("index.html", data={'query': "", 'searchData': "d", 'totalRecords': data_length})

def searchquery(search, sortby):
    # load library

    # define url
    amazon_url = "https://www.amazon.in/s?k={}&s={}".format(search, sortby)

    # get data
    data = amazon_scraper.get_result_similar(amazon_url, group_by_alias=True)

    # combine data into tuple to show it to user
    search_data = tuple(zip(data['Title'], data['ImageUrl'], data['Price']))

    # creating dataframe so that user can download it in csv format
    df = pd.DataFrame(columns=['Query', 'Title', 'Price', 'ImageUrl'])
    for i in range(len(search_data)):
        df.loc[len(df)] = [search, search_data[i][0], search_data[i][2], search_data[i][1]]
    df.to_csv("clients/static/searchedData.csv", index=False)

    # returing data
    return search_data, amazon_url


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
