import os
import dateutil.parser
import psycopg2

def parse_date(date):
    parsedDate = dateutil.parser.parse(date).isoformat()
    return parsedDate

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
      self.dbName = os.environ.get('DATABASE_URL2')
    elif mode == 'production':
      self.dbName = os.environ.get('DATABASE_URL')
    else:
      # TODO
      pass
    self.conn = None
    self.cursor = None

  def connect_db(self):
    """
    DBに接続する
    """
    self.conn = psycopg2.connect(self.dbName)
    self.cursor = self.conn.cursor()

  def close_db(self):
    """
    DBを切断する
    """
    self.conn.close()

  def del_entries(self):
    """
    DBに保存されているエントリを全削除する（テスト用）
    """
    self.execute_query('DELETE FROM entries', '')

  def get_feed_list(self):
    """
    DBからフィードのリストを取得する

    Returns
    -------
    feeds : list
      サイトのタイトル、URL、フィードのURLの辞書の配列
    """
    feeds = []
    self.connect_db()

    self.cursor.execute('SELECT * FROM feeds;')
    for result in self.cursor:
      feed = {'siteTitle':result[1], 'siteUrl':result[2], 'feedUrl':result[3]}
      feeds.append(feed)
  
    self.close_db()

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
    self.connect_db()
    self.cursor.execute('SELECT updated FROM entries where site_url = %s order by updated desc limit 1;', (feedUrl,))
    result = self.cursor.fetchone()
    self.close_db()

    # 検索結果なしのとき
    if result == None:
      return ""

    recentUpdated = parse_date(result[0])
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
    self.connect_db()
    self.cursor.execute(statement, parameters)
    self.commit_db()
    self.close_db()
  
  def commit_db(self):
    """
    DBに変更をコミットする
    """
    self.conn.commit()