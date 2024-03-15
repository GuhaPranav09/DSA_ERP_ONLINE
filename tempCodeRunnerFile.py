@app.route('/')
def index():
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT DISTINCT Site as site_number FROM expenditure")
    sites = cur.fetchall()
    return render_template('calendar.html', sites=sites)