"""
RSSからエントリを収集する
"""
import sys
import feedparser
import dateutil.parser

import dbmanager

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
    self.dbManager = dbmanager.DbManager(mode)

  def save_entries(self):
    """
    RSSのリストからエントリを取得してDBに格納する

    Returns
    -------
    count : int
      保存したエントリの件数
    """
    sites = self.dbManager.get_feed_list()
    count = 0

    for site in sites:
      siteTitle = site['siteTitle']
      feedUrl   = site['feedUrl']
  
      # DB に保存されている最新のエントリの日付
      recentUpdated = self.dbManager.search_recent_updated(feedUrl)

      feed = feedparser.parse(feedUrl)
      for entry in feed.entries:
        update = dbmanager.parse_date(entry.updated)

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
        count = count + 1

    return count

if __name__ == '__main__':
  RssScraper('production').save_entries()
