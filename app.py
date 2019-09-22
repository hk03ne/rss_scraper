import sqlite3

from flask import (
    Flask, 
    request, 
    session, 
    g, 
    redirect, 
    url_for,
    abort, 
    render_template, 
    flash)
import dateutil.parser

from scraper import RssScraper

# configuration
DATABASE = 'production.sqlite3'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    cur = g.db.execute('select * from entries order by updated desc')

    entries = []
    for row in cur.fetchall():
        updated = dateutil.parser.parse(row[5]).strftime('%Y/%m/%d %H:%M:%S')

        entries.append(
            dict(
                site_title  = row[0], 
                site_url    = row[1], 
                entry_title = row[2], 
                entry_url   = row[3], 
                summary     = row[4], 
                updated     = updated))

    return render_template('show_entries.html', entries=entries)

@app.route('/update')
def update_entries():
    scraper = RssScraper('production')
    scraper.save_entries()
    return index()

@app.route('/test')
def show_test_page():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
