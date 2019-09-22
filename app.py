import os
import psycopg2

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
DATABASE = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return psycopg2.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    cursor = g.db.cursor()
    cursor.execute('select * from entries order by updated desc')

    entries = []
    for row in cursor:
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
