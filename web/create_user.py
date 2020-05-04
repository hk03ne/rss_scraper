# -*- coding: utf-8 -*-
"""
ユーザを追加するツール

Example
-------
python3 create_user.py
"""

import os
import hashlib
from getpass import getpass

import dbmanager

dbman = dbmanager.DbManager()

username = input('username: ')
password = getpass('password: ')

salt = os.urandom(32)
digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

query = 'INSERT INTO users '\
        '(name, password_digest, salt) '\
        'VALUES (%s, %s, %s)'

dbman.execute_query(query, username, digest, salt.hex())
