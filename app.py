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
            return render_template('manager_home.html',user=session['username'], site=sitenum)
        else:
            msg = 'Incorrect username/password!'
        
    return render_template('manager_login.html',msg=msg)

@app.route('/director_login', methods=['GET', 'POST'])
def director_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Site = %s AND username = %s AND password = %s', (0, username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['password'] = account['password']
            session['username'] = account['username']
            return render_template('director_home.html')
        else:
            msg = 'Incorrect username/password!'

    return render_template('director_login.html', msg=msg)


@app.route('/director_home')
def director_home():
    return render_template('director_home.html',user="GP")

@app.route('/d_material_purchase')
def d_material_purchase():
    msg=''
    if request.method == 'PUT' and 'site-num' in request.form and 'purchase-date' in request.form and 'material-input' in request.form and 'quantity-input' in request.form and 'price-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        date = request.form['purchase-date']
        material = request.form['material-input']
        quantity = request.form['material-input']
        price = request.form['material-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE DOB = %s AND Material=%s AND Site=%s', (date, material, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
            data = (sitenum,date,material,quantity,price)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('d_material_purchase.html',msg=msg)
        else:
            msg = 'Record with date and material exists!'

    
    return render_template('d_material_purchase.html',msg=msg)



if __name__ == '__main__':
    app.run(debug=True)