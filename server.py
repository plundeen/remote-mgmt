from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

# dummy package names for now
package_list = ["canary", "demo", "foo", "bar"]
version_list = ["1.0.0.0", "1.1.0.0", "1.2.3.4", "2.0.1.0"]


class InstallForm(FlaskForm):
    package = SelectField(
        label="Package", choices=package_list, validators=[DataRequired()]
    )
    version = SelectField(
        label="Version", choices=version_list, validators=[DataRequired()]
    )
    submit = SubmitField(label="Install")


app = Flask(__name__)
Bootstrap(app)

# TODO come up with a better secret key!
app.secret_key = "waffleswaffleswaffleswaffles"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/install_package", methods=["GET", "POST"])
def install_package():
    install_form = InstallForm()
    if install_form.validate_on_submit():
        package_obj = {
            "package": install_form.package.data,
            "version": install_form.version.data,
        }
        print(package_obj)
    #     if install_form.email.data == "admin@email.com" and install_form.password.data == "123456789":
    #         return render_template('success.html')
    #     else:
    #         return render_template('denied.html')
    return render_template("install_package.html", form=install_form)


if __name__ == "__main__":
    app.run(debug=True)
