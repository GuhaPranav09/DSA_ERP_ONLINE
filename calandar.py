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
    cur.execute("SELECT DISTINCT Site as site_number FROM expenditure")
    sites = cur.fetchall()
    return render_template('calendar.html', sites=sites)

@app.route('/calendar_events/<site_number>')
def calendar_events(site_number):
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('''SELECT date, SUM(total_amount) AS total_amount FROM (
                SELECT DOB AS date, SUM(Amount) AS total_amount FROM expenditure WHERE Site = %s GROUP BY DOB
                UNION ALL
                SELECT DOB AS date, SUM(Price) AS total_amount FROM purchase WHERE Site = %s GROUP BY DOB
              ) AS combined_data GROUP BY date''', (site_number, site_number))
    calendar = cur.fetchall()
    return jsonify(calendar)

if __name__ == "__main__":
    app.run(debug=True)
