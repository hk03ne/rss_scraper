import os
import unittest

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        ret = self.app.get('/logout', follow_redirects=True)

    def test_get_user(self):
        # TODO
        pass

    def test_login(self):
        # ユーザ名またはパスワードが入力されていない場合
        ret = self.app.post('/login', data=dict(name="", password=""), follow_redirects=True)
        assert(b'Input name and password' in ret.data)

        ret = self.app.post('/login', data=dict(name="test", password=""), follow_redirects=True)
        assert(b'Input name and password' in ret.data)

        ret = self.app.post('/login', data=dict(name="", password="TEST"), follow_redirects=True)
        assert(b'Input name and password' in ret.data)

        # ユーザ名が間違っている場合
        ret = self.app.post('/login', data=dict(name="tset", password="TEST"), follow_redirects=True)
        assert(b'Incorrect name or password.' in ret.data)

        # パスワードが間違っている場合
        ret = self.app.post('/login', data=dict(name="test", password="tEST"), follow_redirects=True)
        assert(b'Incorrect name or password.' in ret.data)

        # ユーザ名とパスワードが正しい場合
        ret = self.app.post('/login', data=dict(name="test", password="TEST"), follow_redirects=True)
        assert(b'Update' in ret.data)

    def test_logout(self):
        ret = self.app.post('/login', data=dict(name="test", password="TEST"), follow_redirects=True)
        ret = self.app.get('/logout', follow_redirects=True)
        assert(b'Your name' in ret.data)

    def test_unauthorized_handler(self):
        # ログインしていない状態で認証の必要なページにアクセスしようとした場合、ログイン画面にリダイレクトする
        ret = self.app.get('/', follow_redirects=True)
        assert(b'Your name' in ret.data)

    # TODO: Add more tests

if __name__ == '__main__':
    unittest.main()
