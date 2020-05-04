# -*- coding: utf-8 -*-

import hashlib
import os
from getpass import getpass

salt = 'c1ee631b06d1c29b5608a5fd3bd88276aa2e06d5ce5a4ac58949ca1ff4c82015'

dk = hashlib.pbkdf2_hmac('sha256', b'komine!', bytes.fromhex(salt), 100000)

digest_success = 'f91455ff9e1a2adee4d01c0b0825c4d8c2e618c1fc5683704777c945eb7ebc2e'
assert(digest_success == dk.hex())
print('digest: ' + dk.hex())
print('digest: ' + digest_success)
