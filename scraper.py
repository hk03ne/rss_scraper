"""
RSSからエントリを収集する
"""
import html
import feedparser
from bs4 import BeautifulSoup

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
            "test"             : テスト用のDB
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
            id = site['id']
            feedUrl = site['feedUrl']

            # DB に保存されている最新のエントリの日付
            recentUpdated = self.dbManager.search_recent_updated(id)

            feed = feedparser.parse(feedUrl)
            for entry in feed.entries:
                update = dbmanager.parse_date(entry.updated)

                # 古いエントリはスキップ
                if update <= recentUpdated:
                    continue

                soup = BeautifulSoup(entry.summary, "html.parser")
                text = html.escape(soup.get_text())

                query = 'INSERT INTO entries '\
                        '(feed_id, entry_title, entry_url, summary, updated) '\
                        'VALUES (%s, %s, %s, %s, %s)'

                self.dbManager.execute_query(
                    query,
                    (
                        id,
                        entry.title,
                        entry.link,
                        text[:200] + "...",
                        update
                    )
                )
                count = count + 1

        return count


if __name__ == '__main__':
    RssScraper('production').save_entries()
