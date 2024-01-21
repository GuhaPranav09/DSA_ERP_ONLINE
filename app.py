from flask import Flask, render_template, request, session, url_for, redirect, flash
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
            return render_template('director_home.html', user=session['username'])
        else:
            msg = 'Incorrect username/password!'

    return render_template('director_login.html', msg=msg)


@app.route('/d_material_purchase', methods=['GET', 'POST','PUT'])
def d_material_purchase():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'purchase-date' in request.form and 'material-input' in request.form and 'quantity-input' in request.form and 'price-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        date = request.form['purchase-date']
        material = request.form['material-input']
        quantity = request.form['quantity-input']
        price = request.form['price-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.purchase WHERE DOB = %s AND Material=%s AND Site=%s', (date, material, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
            data = (sitenum,date,material,quantity,price)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('d_material_purchase.html',msg=msg)
        else:
            msg = 'Record with date and material exists!'
        
    return render_template('d_material_purchase.html',msg=msg)

@app.route('/m_material_purchase', methods=['GET', 'POST','PUT'])
def m_material_purchase():
    msg=''
    if request.method == 'POST' and 'purchase-date' in request.form and 'material-input' in request.form and 'quantity-input' in request.form and 'price-input' in request.form:
        date = request.form['purchase-date']
        material = request.form['material-input']
        quantity = request.form['quantity-input']
        price = request.form['price-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.purchase WHERE DOB = %s AND Material=%s AND Site=%s', (date, material, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
            data = (sitenum,date,material,quantity,price)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('m_material_purchase.html',msg=msg, Site=sitenum)
        else:
            msg = 'Record with date and material exists!'
        
    return render_template('m_material_purchase.html',msg=msg, Site=sitenum)


@app.route('/d_local_expenditure', methods=['GET', 'POST','PUT'])
def d_local_expenditure():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'exp-date' in request.form and 'activity-input' in request.form and 'amount-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        date = request.form['exp-date']
        activity = request.form['activity-input']
        amount = request.form['amount-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.expenditure WHERE DOB = %s AND Activity=%s AND Site=%s', (date, activity, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.expenditure (Site, DOB, Activity, Amount) values (%s, %s, %s, %s)"
            data = (sitenum,date,activity,amount)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('d_local_expenditure.html',msg=msg)
        else:
            msg = 'Record with date and activity exists!'
    
    return render_template('d_local_expenditure.html',msg=msg)

@app.route('/m_local_expenditure', methods=['GET', 'POST','PUT'])
def m_local_expenditure():
    msg=''
    if request.method == 'POST' and 'exp-date' in request.form and 'activity-input' in request.form and 'amount-input' in request.form:
        date = request.form['exp-date']
        activity = request.form['activity-input']
        amount = request.form['amount-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.expenditure WHERE DOB = %s AND Activity=%s AND Site=%s', (date, activity, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.expenditure (Site, DOB, Activity, Amount) values (%s, %s, %s, %s)"
            data = (sitenum,date,activity,amount)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('m_local_expenditure.html',msg=msg, Site=sitenum)
        else:
            msg = 'Record with date and activity exists!'
    
    return render_template('m_local_expenditure.html',msg=msg, Site=sitenum)

@app.route('/d_staff_salary', methods=['GET', 'POST','PUT'])
def d_staff_salary():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'name-input' in request.form and 'empid-input' in request.form and 'salary-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        name = request.form['name-input']
        empid = request.form['empid-input']
        salary = request.form['salary-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.salary WHERE EmpID=%s AND Site=%s', (empid, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.salary (Site, Name, EmpID, Salary) values (%s, %s, %s, %s)"
            data = (sitenum,name,empid,salary)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('d_staff_salary.html',msg=msg)
        else:
            msg = 'Record with date and Employee exists!'
        
    return render_template('d_staff_salary.html',msg=msg)

@app.route('/m_staff_salary', methods=['GET', 'POST','PUT'])
def m_staff_salary():
    msg=''
    if request.method == 'POST' and 'name-input' in request.form and 'empid-input' in request.form and 'salary-input' in request.form:
        name = request.form['name-input']
        empid = request.form['empid-input']
        salary = request.form['salary-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.salary WHERE EmpID=%s AND Site=%s', (empid, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.salary (Site, Name, EmpID, Salary) values (%s, %s, %s, %s)"
            data = (sitenum,name,empid,salary)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('m_staff_salary.html',msg=msg, Site=sitenum)
        else:
            msg = 'Record with date and Employee exists!'
        
    return render_template('m_staff_salary.html',msg=msg, Site=sitenum)

@app.route('/d_manager_accounts', methods=['GET', 'POST','PUT'])
def d_manager_accounts():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'username-input' in request.form and 'password-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        username = request.form['username-input']
        password = request.form['password-input']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Username=%s AND Site=%s', (username, sitenum))
        record = cursor.fetchone()
        if not record:
            insert_query = "insert into vitproject.login (Site, Username, Password) values (%s, %s, %s)"
            data = (sitenum,username,password)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful'
            return render_template('d_manager_accounts.html',msg=msg)
        else:
            msg = 'Record with date and Employee exists!'
        
    return render_template('d_manager_accounts.html',msg=msg)

@app.route('/d_labour', methods=['GET', 'POST','PUT'])
def d_labour():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'name-input' in request.form and 'empid-input' in request.form and 'joining-date' in request.form and 'gender-input' in request.form and 'address-input' in request.form and 'designation-input' in request.form:
        if 'languages-input' in request.form:
            global sitenum
            sitenum = request.form['site-num']
            name = request.form['name-input']
            empid = request.form['empid-input']
            joining_date = request.form['joining-date']
            gender = request.form['gender-input']
            languages = request.form.getlist('languages-input')
            address = request.form['address-input']
            designation = request.form['designation-input']
            choice = request.form['HiddenField']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM vitproject.labour WHERE Site=%s AND empid=%s', (sitenum, empid))
            record = cursor.fetchone()
            print(choice,choice,choice)
            if choice=='1':
                print('Hello')
                if not record:
                    insert_query = "INSERT INTO vitproject.labour (Site, Name, EmpID, DOB, Gender, Languages, Address, Designation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (sitenum, name, empid, joining_date, gender, ",".join(languages), address, designation)
                    cursor.execute(insert_query, data)
                    mysql.connection.commit()
                    msg = 'Insertion Successful'
                else:
                    msg = 'Record with Employee ID already exists!'
            else:
                if record:
                    update_query = "UPDATE vitproject.labour SET Site=%s AND Name=%s AND DOB=%s AND Gender=%s AND Languages=%s AND Address=%s AND Designation=%s WHERE EmpID=%s"
                    data = (sitenum, name, joining_date, gender, ",".join(languages), address, designation,empid)
                    cursor.execute(update_query, data)
                    mysql.connection.commit()
                    msg = 'Updation Successful'
                else:
                    msg = 'Record with Employee ID doesnt exist!'
        else:
            msg= 'Select atleast one language!'

    return render_template('d_labour.html', msg=msg)

@app.route('/m_labour', methods=['GET', 'POST','PUT'])
def m_labour():
    msg=''
    if request.method == 'POST' and 'name-input' in request.form and 'empid-input' in request.form and 'joining-date' in request.form and 'gender-input' in request.form and 'address-input' in request.form and 'designation-input' in request.form:
        if 'languages-input' in request.form: 
            name = request.form['name-input']
            empid = request.form['empid-input']
            joining_date = request.form['joining-date']
            gender = request.form['gender-input']
            languages = request.form.getlist('languages-input')
            address = request.form['address-input']
            designation = request.form['designation-input']
            print(gender)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM vitproject.labour WHERE Site=%s AND EmpID=%s', (sitenum,empid))
            record = cursor.fetchone()

            if not record:
                insert_query = "INSERT INTO vitproject.labour (Site, Name, EmpID, DOB, Gender, Languages, Address, Designation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (sitenum, name, empid, joining_date, gender, ",".join(languages), address, designation)
                cursor.execute(insert_query, data)
                mysql.connection.commit()
                msg = 'Insertion Successful'
            else:
                msg = 'Record with Employee ID already exists!'
        else:
            msg = 'Select atleast one language!'
        
    return render_template('m_labour.html', msg=msg, Site=sitenum)

@app.route('/view_table/<table_name>', methods=['GET', 'POST'])
def view_table(table_name):
    msg = ''
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM vitproject.{table_name}')
        data = cursor.fetchall()

        if request.method == 'POST':
            if 'delete-record' in request.form and 't-id-input' in request.form:
                t_id = request.form['t-id-input']
                delete_query = f'DELETE FROM vitproject.{table_name} WHERE T_ID = %s'
                cursor.execute(delete_query, (t_id,))
                mysql.connection.commit()
                msg = 'Record deleted!'

        if data:
            return render_template('view_table.html', table_name=table_name, data=data, msg=msg)
        else:
            msg = f'No data found in the {table_name} table.'
    except Exception as e:
        msg = f'Error: {str(e)}'

    return render_template('view_table.html', table_name=table_name, msg=msg)



if __name__ == '__main__':
    app.run(debug=True)