from flask import Flask, render_template, flash, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from werkzeug.debug import console
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckEditor = CKEditor(app)
Bootstrap5(app)

# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["5 per minute"],
#     storage_uri="memory://"
# )

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///python-portfolio.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route("/about")
def about():
    context = {
        'header_img': 'about.png'
    }
    return render_template("pages/about.html", **context)

@app.route("/contact", methods=['GET', 'POST'])
# @limiter.limit("5 per minute")
def contact():
    contact_form = ContactForm()
    context = {
        'header_img': 'contact.png',
        'form': contact_form
    }
    if contact_form.validate_on_submit():
        contact_data = Contact(name=contact_form.name.data, email=contact_form.email.data, message=contact_form.message.data)
        db.session.add(contact_data)
        db.session.commit()

        contact_form.name.data = ''
        contact_form.email.data = ''
        contact_form.message.data = ''
        flash("Your message was successfully sent.")
        return redirect(url_for('contact'))
    return render_template("pages/contact.html", **context)

@app.route("/projects")
def projects():
    context = {
        'header_img': 'projects.png'
    }
    return render_template("pages/projects.html", **context)

if __name__ == "__main__":
    app.run(debug=True, port=5003)