# -*- coding: utf8 -*-
import re

import zeeguu
from zeeguu import model


WORD_PATTERN = re.compile("\[?([^{\[]+)\]?( {[^}]+})?( \[[^\]]\])?")


class WordCache(object):
    def __init__(self):
        self.cache = {}

    def __getitem__(self, args):
        word = self.cache.get(args, None)
        if word is None:
            word = model.Word(*args)
            zeeguu.db.session.add(word)
            self.cache[args] = word
        return word


def populate(from_, to, dict_file):
    cache = WordCache()
    with open(dict_file, "r") as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                return
            orig = cache[clean_word(parts[0]), from_]
            trans = cache[clean_word(parts[1]), to]
            if trans not in orig.translations:
                orig.translations.append(trans)


def clean_word(word):
    match = re.match(WORD_PATTERN, word)
    if match is None:
        print word
        return word.decode("utf8")
    return match.group(1).decode("utf8")


if __name__ == "__main__":
    zeeguu.app.test_request_context().push()

    zeeguu.db.drop_all()
    zeeguu.db.create_all()
    de = model.Language("de", "German")
    en = model.Language("en", "English")
    user = model.User("user@localhost.com", "password", de)
    zeeguu.db.session.add(user)
    zeeguu.db.session.add(en)

    zeeguu.db.session.commit()
