import scraper
import unittest

class TestRssScraper(unittest.TestCase):
  def setUp(self):
    self.test = scraper.RssScraper('test')
    self.test.del_entries()
  def test_init(self):
    assert(self.test.dbManager)
  def tearDown(self):
    self.test.del_entries()

  def test_save_entries(self):
    count = self.test.save_entries()
    assert(count > 0)

  def test_save_only_new_enrty(self):
    # 新しい記事のみ取得する
    # （瞬時に二回実行しても件数が変化しければOKとする）
    self.test.save_entries()
    dbManager = scraper.DbManager('test')
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

class TestDbManager(unittest.TestCase):
  def setUp(self):
    self.test = scraper.DbManager('test')
    self.test.connect_db()
  def test_connect_db(self):
    assert(self.test.conn != None)
    assert(self.test.cursor != None)

if __name__ == "__main__":
    unittest.main()