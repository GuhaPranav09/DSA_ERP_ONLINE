from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

app.secret_key = "company-website"

DB_HOST = "consultancysql.mysql.database.azure.com"
DB_USER = "ConsultancyERP"
DB_PASS = "AzureSQL123"
DB_NAME = "vitproject"

conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

@app.route('/')
def index():
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT Dateofspent as date, SUM(Amount) AS total_amount FROM expenditure GROUP BY Dateofspent")
    calendar = cur.fetchall()
    return render_template('index.html', calendar=calendar)

if __name__ == "__main__":
    app.run(debug=True)