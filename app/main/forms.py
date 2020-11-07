from flask_wtf import FlaskForm
from ..models import User
from .. import db
from wtforms import StringField, DateField, SubmitField, TextAreaField, PasswordField,ValidationError, validators
from wtforms.validators import Required, Optional, Email, EqualTo
from wtforms import RadioField
class BlogForm(FlaskForm):
    title = StringField('Title', validators = [Required()])
    blog = TextAreaField('Content', validators = [Required()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [Required()])
    password = PasswordField("Password", validators = [Required()])         
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [Required()])
    email_address =StringField("Email Address", validators = [Required(), Email()])
    password = PasswordField("Password", validators = [Required(),EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField("Confirm Password")

    def validate_username(self, username):
        if User.query.filter_by(username = username.data).first():
            raise ValidationError(f'That username is no longer available, try {username.data}xy2')
    def validate_email(self, email_field):
        if User.query.filter_by(email = email_field.data).first():
            raise ValidationError("That email is already registered here. If it's your email, please log in")
    submit = SubmitField('Register')
class CommentForm(FlaskForm):
    comment =StringField("Comment",  validators = [Required()])
    submit =SubmitField("Submit Comment")
class DeleteForm(FlaskForm):
    delete = SubmitField("Delete")
class UpdateForm(FlaskForm):
    update = SubmitField("Update")
class SubscribeForm(FlaskForm):
    name = StringField("Name", validators = [Required()])
    email =StringField("Email", validators = [Required(), Email()])
    submit = SubmitField("Subscribe")
