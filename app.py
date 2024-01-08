from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'pass'

app.config['MYSQL_HOST'] = 'consultancysql.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'ConsultancyERP'
app.config['MYSQL_PASSWORD'] = 'AzureSQL123'
app.config['MYSQL_DB'] = 'vitproject'

mysql = MySQL(app)

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/manager_login', methods=['GET','POST'])
def manager_login():
    msg = ''
    if request.method == 'POST' and 'sitenum' in request.form and 'username' in request.form and 'password' in request.form:
        sitenum = request.form['sitenum']
        username = request.form['username']
        password = request.form['password']
        print(mysql.connection)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE sitenum =%s AND username = %s AND password = %s', (sitenum, username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['password'] = account['password']
            session['username'] = account['username']
            return 'Logged in successfully!'
        else:
            msg = 'Incorrect username/password!'
        
    return render_template('manager_login.html',msg=msg)

@app.route('/manager_register', methods=['GET','POST'])
def director_login():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'sitenum' in request.form:
        username = request.form['username']
        password = request.form['password']
        sitenum = request.form['sitenum']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[0-9]', sitenum):
            msg = 'Invalid site number!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not sitenum:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, sitenum,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('manager_register.html',msg=msg)

@app.route('/manager_home')
def manager_home():
    return render_template('manager_home.html', msg=session['sitenum'])

if __name__ == '__main__':
    app.run(debug=True)

