"""
DBとの情報のやりとりを行う
"""
import os
import dateutil.parser
import psycopg2


def parse_date(date):
    parsedDate = dateutil.parser.parse(date).isoformat()
    return parsedDate


class DbManager:
    def __init__(self, mode):
        """
        初期化処理
        """
        self.dbName = os.environ.get('DATABASE_URL')
        self.conn = None
        self.cursor = None

    def connect_db(self):
        """
        DBと接続する
        """
        self.conn = psycopg2.connect(self.dbName)
        self.cursor = self.conn.cursor()

    def close_db(self):
        """
        DBを切断する
        """
        self.conn.close()

    def get_feed_list(self):
        """
        フィードのリストを取得する

        Returns
        -------
        取得したフィードのリスト
        """
        feeds = []
        self.connect_db()

        self.cursor.execute('SELECT * FROM feeds;')
        for result in self.cursor:
            feed = {
                'id':        result[0],
                'user_id':   result[1],
                'siteTitle': result[2],
                'siteUrl':   result[3],
                'feedUrl':   result[4]}
            feeds.append(feed)

        self.close_db()

        return feeds

    def search_recent_updated(self, feedId, userId):
        """
        指定されたフィードIDおよびユーザIDの最新のエントリの更新日付を検索する

        Parameters
        ----------
        feedId : str
            対象のフィードID
        userId : str
            対象のユーザID

        Returns
        -------
        取得した更新日付
        検索結果なしの場合、空文字列を返す。
        """
        self.connect_db()
        self.cursor.execute(
            'SELECT updated FROM entries WHERE feed_id = %s and user_id = %s'
            'ORDER BY updated DESC LIMIT 1;',
            (feedId, userId))
        result = self.cursor.fetchone()
        self.close_db()

        if result is None:
            return ""

        recentUpdated = parse_date(result[0])
        return recentUpdated

    def execute_query(self, statement, *parameters):
        """
        SQLクエリを実行する

        Parameters
        ----------
        statement : str
            SQLクエリ
        parameters : list (省略可)
            SQLクエリに '%s' の形式で埋め込まれた変数に適用する値のリスト
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
