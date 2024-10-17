import os
import csv


from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, desc
from flask_wtf import FlaskForm
from werkzeug.debug import console
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date, datetime
from forms import ContactForm, CoffeeShopForm, TodoForm
from urllib.parse import urlparse
from urllib.parse import parse_qs

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b') #''
ckEditor = CKEditor(app)
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI",  'sqlite:///python-portfolio.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

class TodoItem(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.Date, default=date.today())
    due_date = db.Column(db.Date, nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)

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
        return redirect(url_for('home'))
    return render_template("pages/contact.html", **context)

@app.route("/projects")
def projects():
    context = {
        'header_img': 'projects.png'
    }
    return render_template("pages/projects.html", **context)

@app.route('/projects/cafes')
def cafes():
    list_of_rows = []
    titles = ["Cafe Name", "Location", "Open", "Close", "Coffee", "Wifi", "Power"]
    context = {
        'header_img': 'projects.png',
        'cafes': list_of_rows,
        'titles': titles
    }
    with open('static/data/cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('pages/cafes.html', **context)

@app.route('/projects/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    form = CoffeeShopForm()
    context = {
        'header_img': 'projects.png',
        "form": form
    }
    if form.cancel.data:
        return redirect(url_for('cafes'))

    if form.validate_on_submit():
        with open("static/data/cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe_name.data},"
                           f"{form.location.data},"
                           f"{form.open_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_outlet_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('pages/add_cafe.html', **context)

@app.route("/complete_todos/<int:todo_id>", methods=['GET', 'POST'])
def complete_todo(todo_id):
    result = db.session.execute(db.select(TodoItem).where(TodoItem.id == todo_id))
    todo_item = result.scalar()
    if todo_item:
        todo_item.complete = True
        db.session.add(todo_item)
        db.session.commit()
    return redirect(url_for('todos'))

@app.route("/projects/todos", methods=['GET', 'POST'])
def todos():
    todo_list = db.session.execute(db.select(TodoItem).order_by('due_date').where(TodoItem.complete == False)).scalars().all()
    context = {
        'header_img': 'projects.png',
        'todos': todo_list
    }
    return render_template("pages/todo.html", **context)

@app.route("/projects/add_todo", methods=['GET', 'POST'])
def add_todo():
    todo_form = TodoForm()
    context = {
        'header_img': 'projects.png',
        'form': todo_form
    }
    print(request.form)
    if todo_form.validate_on_submit():
        todo_data = TodoItem(
            title=request.form.get('title'),
            content=request.form.get('content'),
            due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date(),
        )
        db.session.add(todo_data)
        db.session.commit()
        return redirect(url_for('todos'))
    return render_template("pages/add_todo.html", **context)


if __name__ == "__main__":
    app.run(debug=True, port=5003)