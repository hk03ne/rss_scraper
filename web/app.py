# -*- coding: utf-8 -*-
"""
収集されたエントリの表示、およびフィードの登録・編集・削除を行う
"""
import os
from hashlib import sha256
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
SECRET_KEY = os.urandom(16)

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config.from_object(__name__)


def get_user(name):
    """
    ユーザの情報を取得する

    Parameters
    ----------
    name : str
        対象のユーザ名

    Returns
    -------
    取得したユーザ情報
    """
    query = 'select * from users where name = \'{}\''.format(name)

    cursor = g.db.cursor()
    cursor.execute(query)

    users = []
    for row in cursor:
        users.append(
            dict(
                id=row[0],
                password_digest=row[2]))

    if users == []:
        return None

    return users[0]


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    ログイン画面の表示、およびログインを行う

    GETメソッドでアクセスされた場合、ログイン画面を表示する

    POSTメソッドでアクセスされた場合、ユーザ名とパスワードをチェックし、
    登録済みのユーザであればトップページにリダイレクトする
    """
    if request.method == 'GET':
        return render_template('login.html')

    if request.form['name'] == '' or request.form['password'] == '':
        return 'Input name and password.'

    user = get_user(request.form['name'])
    if user is None:
        return 'Incorrect name or password.'

    hash = sha256(request.form['password'].encode()).hexdigest()

    id = user['id']

    if hash == user['password_digest']:
        user = User()
        user.id = id
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return 'Incorrect name or password.'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@login_manager.user_loader
def user_loader(id):
    user = User()
    user.id = id
    return user


def connect_db():
    """
    DBに接続する

    Returns
    -------
    DBとの接続情報
    """
    return psycopg2.connect(app.config['DATABASE'])

def select_entries(where=''):
    """
    エントリを取得する

    Parameters
    ----------
    where : str
        エントリの検索条件

    Returns
    -------
    取得したエントリのリスト
    """
    query = 'select * from view_entries ' + where + ' order by updated desc'
    cursor = g.db.cursor()
    cursor.execute(query)

    entries = []
    for row in cursor:
        updated = dateutil.parser.parse(row[6]).strftime('%Y/%m/%d %H:%M:%S')

        entries.append(
            dict(
                site_title=row[1],
                site_url=row[2],
                entry_title=row[3],
                entry_url=row[4],
                summary=row[5],
                updated=updated))

    return entries


def select_feeds(where=''):
    """
    フィードを取得する

    Parameters
    ----------
    where : str
        フィードの検索条件

    Returns
    -------
    取得したフィードのリスト
    """
    query = 'select * from feeds ' + where + ' order by id'
    print(query)
    cursor = g.db.cursor()
    cursor.execute(query)

    feeds = []
    for row in cursor:
        feeds.append(
            dict(
                id=row[0],
                site_title=row[2],
                site_url=row[3],
                feed_url=row[4]))

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
    """
    トップページを表示する
    """
    entries = select_entries('where user_id = {}'.format(flask_login.current_user.id))

    return render_template('show_entries.html', entries=entries)


@app.route('/update')
@flask_login.login_required
def update_entries():
    """
    エントリを更新する
    """
    scraper = RssScraper()
    scraper.save_entries()
    return redirect(url_for('index'))


@app.route('/test')
@flask_login.login_required
def show_test_page():
    return render_template('test.html')


@app.route('/search')
@flask_login.login_required
def search_entries():
    """
    エントリを検索する

    指定した文字列をタイトルまたはサマリに含むエントリを検索し、表示する
    """
    where = 'where user_id = {} and entry_title like \'%{}%\' or summary like \'%{}%\''.format(
        flask_login.current_user.id, request.args['text'], request.args['text'])

    entries = select_entries(where)

    return render_template('show_entries.html', entries=entries)


@app.route('/feeds/<int:post_id>', methods=["GET", "POST"])
@flask_login.login_required
def edit_feed(post_id):
    """
    フィードを編集する

    GETメソッドでアクセスされた場合、フィードの情報を表示する

    POSTメソッドでアクセスされた場合、フィードの更新または削除を行う
    （更新か削除かはformから受け取った"action"の値で判定する）
    """
    if request.method == "GET":
        feeds = select_feeds('where user_id = {} and id = {}'.format(flask_login.current_user.id, post_id))

        return render_template('update_feed.html', feed=feeds[0])
    else:
        if request.form["action"] == "update":
            cursor = g.db.cursor()

            cursor.execute('update feeds set site_title = %s, '
                           'site_url = %s, feed_url = %s where id = %s',
                           (request.form["site_title"],
                            request.form["site_url"],
                            request.form["feed_url"],
                            request.form["id"]))
            g.db.commit()

            feeds = select_feeds('where user_id = {} and id = {}'.format(flask_login.current_user.id, post_id))

            return render_template('update_feed.html', feed=feeds[0])
        elif request.form["action"] == "delete":
            cursor = g.db.cursor()

            cursor.execute('delete from entries where user_id = %s and feed_id = %s',
                           (flask_login.current_user.id, request.form["id"],))
            cursor.execute('delete from feeds where user_id = %s and id = %s',
                           (flask_login.current_user.id, request.form["id"],))
            g.db.commit()

            return manage_feeds()
        else:
            # TODO
            return ""


@app.route('/feeds')
@flask_login.login_required
def manage_feeds():
    """
    フィード管理画面を表示する
    """
    feeds = select_feeds('where user_id = {}'.format(flask_login.current_user.id))

    return render_template('feeds.html', feeds=feeds)


@app.route('/feeds/add', methods=["GET", "POST"])
@flask_login.login_required
def add_feeds():
    """
    フィードを追加する
    """
    if request.method == "GET":
        return render_template('add_feed.html')
    else:
        cursor = g.db.cursor()
        cursor.execute(
            'insert into feeds (user_id, site_title, site_url, feed_url) '
            'values (%s, %s, %s, %s)',
            (flask_login.current_user.id,
             request.form["site_title"],
             request.form["site_url"],
             request.form["feed_url"]))
        g.db.commit()
        return manage_feeds()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
