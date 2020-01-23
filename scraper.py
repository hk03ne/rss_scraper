import html
import datetime

import feedparser
from bs4 import BeautifulSoup

import dbmanager


class RssScraper:
    def __init__(self, mode):
        self.dbManager = dbmanager.DbManager(mode)

    def save_entries(self):
        sites = self.dbManager.get_feed_list()
        count = 0

        for site in sites:
            feedId = site['id']
            userId = site['user_id']
            feedUrl = site['feedUrl']

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

    def delete_old_entries(self):
        minDatetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)

        self.dbManager.execute_query('DELETE FROM entries WHERE updated < %s', minDatetime.isoformat(timespec='seconds'))

if __name__ == '__main__':
    RssScraper('production').save_entries()
    RssScraper('production').delete_old_entries()
