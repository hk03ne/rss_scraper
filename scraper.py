"""
RSSからエントリを収集する
"""
import sys
import feedparser
import json
import datetime
import sqlite3
import dateutil.parser

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

  def save_entries(self):
    """
    RSSのリストからエントリを取得してDBに格納する
    """
    self.dbManager.connect_db()
    sites = self.dbManager.get_feed_list()
    self.result = 0

    for site in sites:
      siteTitle = site['siteTitle']
      feedUrl   = site['feedUrl']
  
      # DB に保存されている最新のエントリの日付
      recentUpdated = self.dbManager.search_recent_updated(feedUrl)

      feed = feedparser.parse(feedUrl)
      for entry in feed.entries:
        update = dateutil.parser.parse(entry.updated).isoformat()

        # 古いエントリはスキップ
        if update <= recentUpdated:
          continue

        query = 'INSERT INTO entries (site_title, site_url, entry_title, entry_url, summary, updated) VALUES (?, ?, ?, ?, ?, ?)'
        self.dbManager.execute_query(
          query,
          (
            siteTitle, 
            feedUrl, 
            entry.title, 
            entry.link, 
            entry.summary, 
            update
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

  def get_feed_list(self):
    """
    DBからフィードのリストを取得する

    Returns
    -------
      feeds : list
    """
    feeds = []

    for result in self.cursor.execute('SELECT * FROM feeds;'):
      feed = {'siteTitle':result[1], 'siteUrl':result[2], 'feedUrl':result[3]}
      feeds.append(feed)

    return feeds
  
  def search_recent_updated(self, feedUrl):
    """
    DBに保存されている最も新しい更新日付を取得する

    Parameters
    ----------
    feedUrl : str
      対象サイトのURL
    Returns
    -------
    recentUpdated : str
      DBに保存されている最も新しい更新日付
      保存されている記事がなかった場合、空文字を返す
    """
    self.cursor.execute('SELECT updated FROM entries where site_url = ? order by updated desc limit 1;', (feedUrl,))
    result = self.cursor.fetchone()
    # 検索結果なしのとき
    if result == None:
      return ""

    recentUpdated = dateutil.parser.parse(result[0]).isoformat()
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

if __name__ == '__main__':
  print("hoge")
  RssScraper('production').save_entries()
