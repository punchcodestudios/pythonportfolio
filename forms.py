from datetime import datetime
from tkinter.ttk import Button

from flask_wtf import FlaskForm
from sqlalchemy import DateTime, Nullable
from wtforms import StringField, SubmitField, DateField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField, FileField
from wtforms.validators import DataRequired, URL, Email, Length, Optional
from wtforms.validators import DataRequired, ValidationError
from flask_ckeditor import CKEditorField


def validate_url(form, field):
    valid = field.data.split('://')[0] == 'https'
    if not valid:
        raise ValidationError('value is missing required "https"')
    return valid

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit')

class CoffeeShopForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    URL = StringField('URL', validators=[DataRequired(), validate_url])
    open_time = StringField('Open', validators=[DataRequired()])
    closing_time = StringField('Close', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_outlet_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class UploadFileForm(FlaskForm):
    image = FileField('Source', validators=[DataRequired()])
    submit = SubmitField('Submit')
