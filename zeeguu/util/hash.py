# -*- coding: utf8 -*-
from hashlib import sha1


def text_hash(text):
    if isinstance(text, unicode):
        text = text.encode("utf8")
    return sha1(text).digest()


def password_hash(password, salt):
    password = password.encode("utf8")
    for i in range(1000):
        password = text_hash(password + salt)
    return password
