# -*- coding: utf-8 -*-
"""
フィードからエントリを収集する
"""
import html
import feedparser
from bs4 import BeautifulSoup

import dbmanager


class RssScraper:
    def __init__(self):
        """
        初期化処理

        DBと接続する
        """
        self.dbManager = dbmanager.DbManager()

    def save_entries(self):
        """
        エントリを収集する

        Returns
        -------
        count : int
            収集したエントリ数
        """
        feeds = self.dbManager.get_feed_list()
        count = 0

        for feed in feeds:
            feedId = feed['id']
            userId = feed['user_id']
            feedUrl = feed['feedUrl']

            recentUpdated = self.dbManager.search_recent_updated(feedId, userId)

            feed = feedparser.parse(feedUrl)
            for entry in feed.entries:
                update = dbmanager.parse_date(entry.updated)

                if update <= recentUpdated:
                    continue

                soup = BeautifulSoup(entry.summary, "html.parser")
                text = html.escape(soup.get_text())

                query = 'INSERT INTO entries '\
                        '(feed_id, user_id, entry_title, entry_url, summary, updated) '\
                        'VALUES (%s, %s, %s, %s, %s, %s)'

                self.dbManager.execute_query(
                    query,
                    feedId,
                    userId,
                    entry.title,
                    entry.link,
                    text[:200] + "...",
                    update
                )
                count = count + 1

        return count


if __name__ == '__main__':
    RssScraper('production').save_entries()
