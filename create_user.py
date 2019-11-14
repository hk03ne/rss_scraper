from hashlib import sha256

import dbmanager

dbman = dbmanager.DbManager('production')

username = input('username: ')
password = input('password: ')

sha256 = sha256()
sha256.update(password.encode())

digest = sha256.hexdigest()

query = 'INSERT INTO users '\
        '(id, password_digest) '\
        'VALUES (%s, %s)'

dbman.execute_query(query, username, digest)
