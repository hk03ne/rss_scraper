import os
import psycopg2

from flask import (
    Flask, 
    request, 
    redirect,
    url_for,
    g, 
    render_template)
import dateutil.parser
import flask_login

from scraper import RssScraper
from user import User

# configuration
DATABASE = os.environ.get('DATABASE_URL')
SECRET_KEY = 'f31-Ad#w'

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config.from_object(__name__)

users = {'hk': {'password': 'secret'}}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']

    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

def connect_db():
    return psycopg2.connect(app.config['DATABASE'])

def select_entries(where=''):
    query = 'select * from view_entries ' + where + ' order by updated desc'
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

    return entries

def select_feeds(where=''):
    query = 'select * from feeds ' + where +  ' order by id'

    cursor = g.db.cursor()
    cursor.execute(query)

    feeds = []
    for row in cursor:
        feeds.append(
            dict(
                id          = row[0],
                site_title  = row[1], 
                site_url    = row[2], 
                feed_url    = row[3]))

    return feeds

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
@flask_login.login_required
def index():
    entries = select_entries()

    return render_template('show_entries.html', entries=entries)

@app.route('/update')
@flask_login.login_required
def update_entries():
    scraper = RssScraper('production')
    scraper.save_entries()
    return redirect(url_for('index'))

@app.route('/test')
@flask_login.login_required
def show_test_page():
    return render_template('test.html')

@app.route('/search')
@flask_login.login_required
def search_entries():
    where = 'where entry_title like \'%{}%\' or summary like \'%{}%\''.format(request.args['text'], request.args['text'])

    entries = select_entries(where)

    return render_template('show_entries.html', entries=entries)

@app.route('/feeds/<int:post_id>', methods=["GET", "POST"])
@flask_login.login_required
def edit_feed(post_id):
    if request.method == "GET":
        feeds = select_feeds('where id = {}'.format(post_id))

        return render_template('update_feed.html', feed=feeds[0])
    else:
        if request.form["action"] == "update":
            cursor = g.db.cursor()

            cursor.execute('update feeds set site_title = %s, site_url = %s, feed_url = %s where id = %s',
                (request.form["site_title"], request.form["site_url"], request.form["feed_url"], request.form["id"]))
            g.db.commit()

            feeds = select_feeds('where id = {}'.format(post_id))

            return render_template('update_feed.html', feed=feeds[0])
        elif request.form["action"] == "delete":
            cursor = g.db.cursor()

            cursor.execute('delete from feeds where id = %s',
                (request.form["id"],))
            g.db.commit()

            return manage_feeds()
        else:
            # TODO
            return ""

@app.route('/feeds')
@flask_login.login_required
def manage_feeds():
    feeds = select_feeds()

    return render_template('feeds.html', feeds=feeds)

@app.route('/feeds/add', methods=["GET", "POST"])
@flask_login.login_required
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
