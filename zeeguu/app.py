# -*- coding: utf8 -*-
import os
import os.path
import functools

import flask
import sqlalchemy.exc

import zeeguu
from zeeguu import model


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

try:
    os.makedirs(instance_path)
except:
    if not os.path.isdir(instance_path):
        raise


def with_user(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        try:
            session_id = int(flask.request.args['session'])
        except:
            flask.abort(401)
        session = model.Session.query.get(session_id)
        if session is None:
            flask.abort(401)
        flask.g.user = session.user
        session.update_use_date()
        return view(*args, **kwargs)
    return wrapped_view


def crossdomain(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response
    return wrapped_view


@app.before_request
def setup():
    if "user" in flask.session:
        flask.g.user = model.User.query.get(flask.session["user"])
    else:
        flask.g.user = None


# Web interface

@app.route("/")
def home():
    return flask.render_template("index.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    form = flask.request.form
    if flask.request.method == "POST" and form.get("login", False):
        password = form.get("password", None)
        email = form.get("email", None)
        if password is None or email is None:
            flask.flash("Please enter your email address and password")
        else:
            user = model.User.authorize(email, password)
            if user is None:
                flask.flash("Invalid email and password combination")
            else:
                flask.session["user"] = user.id
                return flask.redirect(flask.url_for("learning_center"))
    return flask.render_template("login.html")


@app.route("/logout")
def logout():
    flask.session.pop("user", None)
    return flask.redirect(flask.url_for("home"))


@app.route("/learningcenter")
def learning_center():
    if not flask.g.user:
        return flask.redirect(flask.url_for("login"))
    searches = model.Search.query.filter_by(user=flask.g.user).limit(100).all()
    return flask.render_template("learningcenter.html", searches=searches)


# API

@app.route("/adduser/<email>", methods=["POST"])
def adduser(email):
    password = flask.request.form.get("password", None)
    if password is None:
        flask.abort(400)
    try:
        zeeguu.db.session.add(model.User(email, password))
        zeeguu.db.session.commit()
    except ValueError:
        flask.abort(400)
    except sqlalchemy.exc.IntegrityError:
        flask.abort(400)
    return get_session(email)


@app.route("/session/<email>", methods=["POST"])
def get_session(email):
    password = flask.request.form.get("password", None)
    if password is None:
        flask.abort(400)
    user = model.User.authorize(email, password)
    if user is None:
        flask.abort(401)
    session = model.Session.for_user(user)
    zeeguu.db.session.add(session)
    zeeguu.db.session.commit()
    return str(session.id)


@app.route("/contribute/<from_lang_code>/<term>/<to_lang_code>/<translation>",
           methods=["POST"])
@crossdomain
@with_user
def contribute(from_lang_code, term, to_lang_code, translation):
    from_lang = model.Language.find(from_lang_code)
    to_lang = model.Language.find(to_lang_code)

    word = model.Word.find(term, from_lang)
    translation = model.Word.find(translation, to_lang)

    if translation not in word.translations:
        word.translations.append(translation)
        zeeguu.db.session.add(word)
        zeeguu.db.session.commit()

    return "OK"


@app.route("/lookup/<from_lang>/<term>/<to_lang>", methods=("POST",))
@crossdomain
@with_user
def translate(from_lang, term, to_lang):
    from_lang = model.Language.find(from_lang)
    if not isinstance(to_lang, model.Language):
        to_lang = model.Language.find(to_lang)
    user = flask.g.user
    content = flask.request.form.get("text")
    if content is not None:
        text = model.Text.find(content, from_lang)
        user.read(text)
    else:
        text = None
    user.searches.append(
        model.Search(user, model.Word.find(term, from_lang), to_lang, text)
    )
    zeeguu.db.session.commit()
    return "OK"


@app.route("/lookup/<from_lang>/<term>", methods=("POST",))
@crossdomain
@with_user
def translate_to_preferred(from_lang, term):
    return translate(from_lang, term, flask.g.user.preferred_language)
