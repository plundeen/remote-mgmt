#!/usr/bin/env python3
"""Demo webserver leveraging Flask-Bootstrap"""

from time import sleep
from datetime import datetime
import os
import sys

from flask import Flask, Response, render_template, request, stream_with_context
from flask_bootstrap import Bootstrap
import flask_bootstrap.nav
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


# dummy package names for now
PACKAGE_LIST = ["canary", "demo", "foo", "bar"]
VERSION_LIST = ["1.0.0.0", "1.1.0.0", "1.2.3.4", "2.0.1.0"]


class FeedRegistrationForm(FlaskForm):
    """Flask WTForm object for selecting feed to register"""

    feed = SelectField(
        label="Package", validators=[DataRequired()]
    )
    submit = SubmitField(label="Install")


class InstallForm(FlaskForm):
    """Flask WTForm object for selecting package to install"""

    package = SelectField(
        label="Package", validators=[DataRequired()]
    )
    version = SelectField(
        label="Version", validators=[DataRequired()]
    )
    submit = SubmitField(label="Install")


# Instantiate the Nav object, to render the navbar
nav = Nav()


@nav.navigation()
def mynavbar():
    """Sets up the common nav bar"""
    return Navbar(
        "Company Name",
        View("Home", "home"),
        View("Register Feed", "register_feed"),
        View("Install Package", "install_package"),
        View("Job History", "job_history"),
        View("Stream test", "stream_test"),
        View("Log Files", "log_file", file_path=""),
    )


# Set up the flask app
if getattr(sys, 'frozen', False):
    print('getattr returned frozen')
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    print('default getattr case')
    app = Flask(__name__)

# Enable this to serve local bootstrap resources (i.e. if behind firewall)
# app.config['BOOTSTRAP_SERVE_LOCAL'] = True

nav.init_app(app)
Bootstrap(app)

# TODO come up with a better secret key!
app.secret_key = "waffleswaffleswaffleswaffles"


@app.route("/")
def home():
    """Default index"""
    return render_template("index.html")


@app.route("/register_feed", methods=["GET", "POST"])
def register_feed():
    """Route to demonstrate registering a new feed"""
    feed_form = FeedRegistrationForm()
    feed_form.feed.choices = PACKAGE_LIST
    if feed_form.validate_on_submit():
        feed_obj = {"package": feed_form.feed.data}
        print(feed_obj)
    return render_template("register_feed.html", form=feed_form)


@app.route("/install_package", methods=["GET", "POST"])
def install_package():
    """Route to demonstrate installing a package"""
    install_form = InstallForm()
    install_form.package.choices = PACKAGE_LIST
    install_form.version.choices = VERSION_LIST
    if install_form.validate_on_submit():
        package_obj = {
            "package": install_form.package.data,
            "version": install_form.version.data,
        }
        print(package_obj)
    return render_template("install_package.html", form=install_form)


@app.route("/job_history", methods=["GET"])
def job_history():
    """Route for opening the job_history template, to demo showing previous jobs' logs"""
    return render_template("job_history.html")


def stream_template(template_name, **context):
    """Function to stream data to a template"""
    app.update_template_context(context)
    # pylint: disable=E1101
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


def generate():
    """Demo function to simulate streaming data (such as package installation stdout)"""
    for i in range(10):
        yield f"{datetime.now().time()} Line {i}"
        sleep(0.5)


@app.route("/stream_test", methods=["GET"])
def stream_test():
    """Demo of streaming text content into a templated page"""
    # https://flask.palletsprojects.com/en/2.0.x/patterns/streaming/
    # https://gist.github.com/huiliu/46be335427605960fa84
    lines = generate()
    return Response(
        stream_with_context(stream_template("stream_test.html", lines=lines))
    )


@app.route("/logs/", defaults={"file_path": ""})
@app.route("/logs/<path:file_path>", methods=["GET"])
def log_file(file_path):
    """Demo of hosting static files and rendering contents in browser"""
    content = ""
    links = [{"name": "<root>", "href": "/logs"}]
    file_path = f"static/logs/{file_path}"

    if os.path.isfile(file_path):
        with open(file_path) as f:
            content = f.read()
    else:
        with os.scandir(os.path.abspath(file_path)) as list_of_entries:
            for entry in list_of_entries:
                relpath = os.path.relpath(entry.path, "logs")
                linkname = relpath.replace("\\", "/")
                if os.path.isdir(entry.path):
                    linkname += "/"
                links.append({"name": linkname, "href": relpath})
    return render_template("log_file.html", file_contents=content, links=links)


def shutdown_server():
    """Function to shut down the simple flask server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/shutdown")
def shutdown():
    """Shuts down the server"""
    # Intent here is to support killing this app in preparation for updating it.
    # We might be able to call a scheduled task to update and restart in 1 min.
    # Or, perhaps we could have this run as a service, and it could auto recover...
    # TODO: consider making a page with a button and doing this as a POST operation
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(debug=True)
