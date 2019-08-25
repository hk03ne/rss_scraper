"""
RSSからエントリを収集する
"""
import sys
import feedparser
import json
import datetime
import sqlite3

class RssScraper:
  """
  RSSからエントリの収集を行う
  """
  def __init__(self, mode):
    """
    Parameters
    ----------
    mode : str
      エントリを保存するDBのモード
      "test"       : テスト用のDB
      "production" : 本番環境用のDB
    """
    self.dbManager = DbManager(mode)
    self.result = 0

  def get_site_list(self):
    """
    本スクリプトと同じディレクトリに置かれた 'rss.json' から RSS のリストを取得する

    Notes
    -----
    rss.json の形式は以下の通り
    {
      "RSS名（何でもよい）":{
        "url":"RSSへのURL",
        "title":"RSSのタイトル"
      }
    }

    Example: 
    {
      "site1":{
        "url":"https://hoge.jp/feed/atom",
        "title":"Hoge News"
      }
    }
    """
    f = open('./rss.json')
    d = json.load(f)
    return d

  def save_entries(self):
    """
    RSSのリストからエントリを取得してDBに格納する
    """
    self.dbManager.connect_db()
    sites = self.get_site_list()
    self.result = 0

    for site in sites.values():
      siteTitle = site['title']
      siteUrl   = site['url']
  
      # DB に保存されている最新のエントリの日付
      recentUpdated = self.dbManager.search_recent_updated(siteUrl)

      feed = feedparser.parse(siteUrl)
      for entry in feed.entries:
        # 古いエントリはスキップ
        if entry.updated <= recentUpdated:
          continue

        query = 'INSERT INTO entries (site_title, site_url, entry_title, entry_url, summary, updated) VALUES (?, ?, ?, ?, ?, ?)'
        self.dbManager.execute_query(
          query,
          (
            siteTitle, 
            siteUrl, 
            entry.title, 
            entry.link, 
            entry.summary, 
            entry.updated
          )
        )
        self.result = self.result + 1
    # 後始末
    self.dbManager.commit_db()
    self.dbManager.close_db()

  def del_entries(self):
    """
    DBに保存されているエントリを全削除する（テスト用）
    """
    self.dbManager.connect_db()
    self.dbManager.execute_query('DELETE FROM entries', '')
    self.dbManager.commit_db()
    #self.dbManager.close_db()

class DbManager:
  def __init__(self, mode):
    """
    Parameters
    ----------
    mode : str
      エントリを保存するDBのモード
      "test"       : テスト用のDB
      "production" : 本番環境用のDB
    """
    if mode == 'test':
      self.dbName = 'test.sqlite3'
    elif mode == 'production':
      self.dbName = 'production.sqlite3'
    else:
      # TODO
      pass
    self.conn = None
    self.cursor = None

  def connect_db(self):
    """
    DBに接続する
    """
    self.conn = sqlite3.connect(self.dbName)
    self.cursor = self.conn.cursor()

  def close_db(self):
    """
    DBを切断する
    """
    self.conn.close()

  def search_recent_updated(self, siteUrl):
    """
    DBに保存されている最も新しい更新日付を取得する

    Parameters
    ----------
    siteUrl : str
      対象サイトのURL
    Returns
    -------
    recentUpdated : str
      DBに保存されている最も新しい更新日付
      保存されている記事がなかった場合、空文字を返す
    """
    self.cursor.execute('SELECT updated FROM entries where site_url = ? order by updated desc limit 1;', (siteUrl,))
    result = self.cursor.fetchone()
    # 検索結果なしのとき
    if result == None:
      return ""

    recentUpdated = result[0]
    return recentUpdated

  def execute_query(self, statement, parameters):
    """
    SQLクエリを実行する

    Parameters
    ----------
    statement : str
      プレースホルダを利用したSQLクエリ
    parameters : str
      statementのプレースホルダに代入するパラメータのタプル
    """
    self.cursor.execute(statement, parameters)
  
  def commit_db(self):
    """
    DBに変更をコミットする
    """
    self.conn.commit()

class TestCase:
  """
  テスト実行用クラス

  """
  def __init__(self, name):
    """
    Parameters
    ----------
    name : str
      実行する関数名
    """
  
    self.name = name
  def setUp(self):
    """
    テストの前準備を行う
    """
    pass
  def tearDown(self):
    """
    テストの後始末を行う
    """
    pass
  def run(self):
    """
    テストを実行する
    """
    self.setUp()
    method = getattr(self, self.name)
    method()
    self.tearDown()

class TestRssScraper(TestCase):
  def setUp(self):
    self.test = RssScraper('test')
    self.test.del_entries()
  def test_init(self):
    assert(self.test.dbManager)
  def tearDown(self):
    self.test.del_entries()

  def test_save_entries(self):
    self.test.save_entries()
    assert(self.test.result > 0)

  def test_save_only_new_enrty(self):
    # 新しい記事のみ取得する
    # （瞬時に二回実行しても件数が変化しければOKとする）
    self.test.save_entries()
    dbManager = DbManager('test')
    dbManager.connect_db()
    dbManager.cursor.execute("SELECT COUNT(*) FROM entries")
    c = dbManager.cursor.fetchone()
  
    # 実行前の件数
    count = c[0]

    self.test.save_entries()
    dbManager.cursor.execute("SELECT COUNT(*) FROM entries")
    c = dbManager.cursor.fetchone()
    assert(count == c[0])
    dbManager.cursor.close()

class TestDbManager(TestCase):
  def setUp(self):
    self.test = DbManager('test')
    self.test.connect_db()
  def test_connect_db(self):
    assert(self.test.conn != None)
    assert(self.test.cursor != None)

TestDbManager("test_connect_db").run()
TestRssScraper("test_init").run()
TestRssScraper("test_save_entries").run()
TestRssScraper("test_save_only_new_enrty").run()

RssScraper('test').save_entries()
RssScraper('production').save_entries()
