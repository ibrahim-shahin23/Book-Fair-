from wtforms import DateField, FloatField, SelectField, StringField, SubmitField
from datetime import date
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

# class BookDeleteForm(FlaskForm):
#     submit = SubmitField("Delete Book")    

class AuthorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    birth_date = DateField("Birth Date", validators=[DataRequired()], default=date.today)
    image = StringField("Author Image", validators=[DataRequired()])
    submit = SubmitField("Save Author")

class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    image = StringField("Book Image", validators=[DataRequired()])
    publish_date = DateField("Publish Date", validators=[DataRequired()], default=date.today)
    price = FloatField("Price", validators=[DataRequired()])
    appropriate_for = SelectField("Appropriate For", choices=[
        ('under_8', 'Under 8'),
        ('8_15', '8-15'),
        ('adults', 'Adults')
    ], validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save Book")
