# -*- coding: utf8 -*-
import os
import os.path

import flask

import zeeguu
import zeeguu.gym.views
import zeeguu.api.views


# Mircea: we must define this before we use it ...
class CrossdomainErrorFlask(flask.Flask):
    """Allows cross-domain requests for all error pages"""
    def handle_user_exception(self, e):
        rv = super(CrossdomainErrorFlask, self).handle_user_exception(e)
        rv = self.make_response(rv)
        rv.headers['Access-Control-Allow-Origin'] = "*"
        return rv


app = CrossdomainErrorFlask(__name__, instance_relative_config=True)
app.config.from_object("zeeguu.config")
app.config.from_pyfile("config.cfg", silent=True)
app.config.from_envvar("ZEEGUU_CONFIG", silent=True)

instance_path = os.path.join(app.instance_path, "gen")
instance = flask.Blueprint("instance", __name__, static_folder=instance_path)
app.register_blueprint(instance)

app.register_blueprint(zeeguu.gym.views.gym)
app.register_blueprint(zeeguu.api.views.api)

try:
    os.makedirs(instance_path)
except:
    if not os.path.isdir(instance_path):
        raise
