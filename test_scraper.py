import scraper

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

class TestDbManager(TestCase):
  def setUp(self):
    self.test = scraper.DbManager('test')
    self.test.connect_db()
  def test_connect_db(self):
    assert(self.test.conn != None)
    assert(self.test.cursor != None)

TestDbManager("test_connect_db").run()
TestRssScraper("test_init").run()
TestRssScraper("test_save_entries").run()
TestRssScraper("test_save_only_new_enrty").run()

