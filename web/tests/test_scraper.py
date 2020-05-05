import unittest

import scraper
import dbmanager


class TestRssScraper(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_entries(self):
        sc = scraper.RssScraper()
        db = sc.dbManager

        db.execute_query('DELETE FROM entries;')
        db.execute_query('DELETE FROM feeds;')
        db.execute_query('INSERT INTO feeds (id, user_id, site_title, site_url, feed_url) VALUES (9, 99, \'Wikipedia featured articles\', \'https://en.wikipedia.org/w/api.php\', \'http://en.wikipedia.org/w/api.php?action=featuredfeed&feed=featured&feedformat=atom\');')

        sc.save_entries()

        latest = db.search_recent_updated(9, 99)

        db.connect_db()
        db.cursor.execute("SELECT COUNT(*) FROM entries WHERE user_id = 99 AND feed_id = 9;")
        result = db.cursor.fetchone()
        db.close_db()
        count = result[0]

        assert(count > 1)

        sc.save_entries()

        latest2 = db.search_recent_updated(9, 99)

        db.connect_db()
        db.cursor.execute("SELECT COUNT(*) FROM entries WHERE user_id = 99 AND feed_id = 9;")
        result = db.cursor.fetchone()
        db.close_db()
        count2 = result[0]

        # The number of articles should not change
        # unless the latest update date is chaged.
        assert(count == count2 or (count < count2 and latest < latest2))

        db.execute_query('DELETE FROM entries;')
        db.execute_query('DELETE FROM feeds;')


if __name__ == "__main__":
    unittest.main()
