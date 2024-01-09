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
        global sitenum
        sitenum = request.form['sitenum']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Site =%s AND username = %s AND password = %s', (sitenum, username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['password'] = account['password']
            session['username'] = account['username']
            return render_template('manager_home.html',msg=session['username'], site=sitenum)
        else:
            msg = 'Incorrect username/password!'
        
    return render_template('manager_login.html',msg=msg)

@app.route('/director_login', methods=['GET','POST'])
def director_login():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'sitenum' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Site = %s AND username = %s AND password = %s', (0, username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['password'] = account['password']
            session['username'] = account['username']
            return render_template('director_home.html',msg=session['username'])
        else:
            msg = 'Incorrect username/password!'

    return render_template('director_login.html',msg=msg)

@app.route('/d_material_purchase')
def d_material_purchase():
    return render_template('d_material_purchase.html')

if __name__ == '__main__':
    app.run(debug=True)