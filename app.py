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
    cursor.execute('select * from view_entries order by updated desc')

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

@app.route('/search')
def search_entries():
    query = 'select * from view_entries where entry_title like \'%{}%\' or summary like \'%{}%\' order by updated desc'.format(request.args['text'], request.args['text'])

    cursor = g.db.cursor()
    cursor.execute(query)

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

@app.route('/feeds/<int:post_id>', methods=["GET", "POST"])
def edit_feed(post_id):
    if request.method == "GET":
        cursor = g.db.cursor()
        cursor.execute('select * from feeds where id = %s', (post_id,))

        feeds = []
        for row in cursor:
            feeds.append(
                dict(
                    id          = row[0],
                    site_title  = row[1], 
                    site_url    = row[2], 
                    feed_url    = row[3]))

        return render_template('update_feed.html', feed=feeds[0])
    else:
        if request.form["action"] == "update":
            cursor = g.db.cursor()

            cursor.execute('update feeds set site_title = %s, site_url = %s, feed_url = %s where id = %s',
                (request.form["site_title"], request.form["site_url"], request.form["feed_url"], request.form["id"]))
            g.db.commit()

            cursor.execute('select * from feeds where id = %s', (post_id,))
            feeds = []
            for row in cursor:
                feeds.append(
                    dict(
                        id          = row[0],
                        site_title  = row[1], 
                        site_url    = row[2], 
                        feed_url    = row[3]))
            return render_template('update_feed.html', feed=feeds[0])
        elif request.form["action"] == "delete":
            cursor = g.db.cursor()

            cursor.execute('delete from feeds where id = %s',
                (request.form["id"],))
            g.db.commit()

            return manage_feed()
        else:
            # TODO
            return ""

@app.route('/feeds')
def manage_feeds():
    cursor = g.db.cursor()
    cursor.execute('select * from feeds order by id')

    feeds = []
    for row in cursor:
        feeds.append(
            dict(
                id          = row[0],
                site_title  = row[1], 
                site_url    = row[2], 
                feed_url    = row[3]))

    return render_template('feeds.html', feeds=feeds)

@app.route('/feeds/add', methods=["GET", "POST"])
def add_feeds():
    if request.method == "GET":
        return render_template('add_feed.html')
    else:
        cursor = g.db.cursor()
        cursor.execute('insert into feeds (site_title, site_url, feed_url) values (%s, %s, %s)', 
            (request.form["site_title"], request.form["site_url"], request.form["feed_url"]))
        g.db.commit()
        return manage_feeds()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
