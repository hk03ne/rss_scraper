import unittest

import dbmanager


class TestDbManager(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect_db(self):
        db = dbmanager.DbManager()
        db.connect_db()
        assert(db.conn.closed == 0)
        db.close_db()

    def test_close_db(self):
        db = dbmanager.DbManager()
        db.connect_db()
        db.close_db()
        assert(db.conn.closed != 0)

    def test_get_feed_list(self):
        db = dbmanager.DbManager()
        db.execute_query('DELETE FROM feeds;')
        db.execute_query('INSERT INTO feeds (id, user_id, site_title, site_url, feed_url) VALUES (1, 2, \'site_title\', \'site_url\', \'feed_url\');')
        feeds = db.get_feed_list()
        assert(feeds[0]['id'] == 1)
        assert(feeds[0]['user_id'] == 2)
        assert(feeds[0]['siteTitle'] == 'site_title')
        assert(feeds[0]['siteUrl'] == 'site_url')
        assert(feeds[0]['feedUrl'] == 'feed_url')
        db.execute_query('DELETE FROM feeds;')

    def test_search_recent_updated(self):
        db = dbmanager.DbManager()
        db.execute_query('DELETE FROM entries;')
        db.execute_query('INSERT INTO entries (user_id, feed_id, entry_title, entry_url, summary, updated) VALUES (3, 3, \'entry_title\', \'entry_url\', \'summary\', \'2020-01-01 09:00:00\');')
        db.execute_query('INSERT INTO entries (user_id, feed_id, entry_title, entry_url, summary, updated) VALUES (3, 3, \'entry_title\', \'entry_url\', \'summary\', \'2020-01-02 03:01:01\');')
        db.execute_query('INSERT INTO entries (user_id, feed_id, entry_title, entry_url, summary, updated) VALUES (3, 3, \'entry_title\', \'entry_url\', \'summary\', \'2019-12-01 23:59:59\');')
        date = db.search_recent_updated(3,3)
        assert(date == '2020-01-02T03:01:01')
        db.execute_query('DELETE FROM entries;')


if __name__ == "__main__":
    unittest.main()

