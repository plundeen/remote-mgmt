from flask import Flask, render_template, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from time import sleep
from datetime import datetime

# dummy package names for now
package_list = ["canary", "demo", "foo", "bar"]
version_list = ["1.0.0.0", "1.1.0.0", "1.2.3.4", "2.0.1.0"]


class FeedRegistrationForm(FlaskForm):
    """Flask WTForm object for selecting feed to register"""

    feed = SelectField(
        label="Package", choices=package_list, validators=[DataRequired()]
    )
    submit = SubmitField(label="Install")


class InstallForm(FlaskForm):
    """Flask WTForm object for selecting package to install"""

    package = SelectField(
        label="Package", choices=package_list, validators=[DataRequired()]
    )
    version = SelectField(
        label="Version", choices=version_list, validators=[DataRequired()]
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
    )


# Set up the flask app
app = Flask(__name__)
nav.init_app(app)
Bootstrap(app)

# TODO come up with a better secret key!
app.secret_key = "waffleswaffleswaffleswaffles"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register_feed", methods=["GET", "POST"])
def register_feed():
    feed_form = FeedRegistrationForm()
    if feed_form.validate_on_submit():
        feed_obj = {"package": feed_form.feed.data}
        print(feed_obj)
    return render_template("register_feed.html", form=feed_form)


@app.route("/install_package", methods=["GET", "POST"])
def install_package():
    install_form = InstallForm()
    if install_form.validate_on_submit():
        package_obj = {
            "package": install_form.package.data,
            "version": install_form.version.data,
        }
        print(package_obj)
    return render_template("install_package.html", form=install_form)


@app.route("/job_history", methods=["GET"])
def job_history():
    return render_template("job_history.html")


def stream_template(template_name, **context):
    """Function to stream data to a template"""
    app.update_template_context(context)
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
    # https://flask.palletsprojects.com/en/2.0.x/patterns/streaming/
    # https://gist.github.com/huiliu/46be335427605960fa84
    lines = generate()
    return Response(stream_with_context(stream_template("stream_test.html", lines=lines)))


if __name__ == "__main__":
    app.run(debug=True)
