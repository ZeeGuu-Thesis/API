#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import os.path

import flask.ext.assets
import flask.ext.sqlalchemy

db = flask.ext.sqlalchemy.SQLAlchemy()

from zeeguu import app

app = app.app
if os.environ.get("ZEEGUU_TESTING"):
    # in case of testing, we don't want to use the real database
    app.config.pop("SQLALCHEMY_DATABASE_URI", None)

env = flask.ext.assets.Environment(app)
env.cache = app.instance_path
env.directory = os.path.join(app.instance_path, "gen")
env.url = "/gen"
env.append_path(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static"
), "/static")

db.init_app(app)
db.create_all(app=app)
