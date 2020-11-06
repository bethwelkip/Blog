from flask import render_template,request,redirect,url_for, abort
from ..models import User, Blog, Comment
from .forms import BlogForm, LoginForm, RegistrationForm, CommentForm, DeleteForm
from . import main
from .fill_db import initialize
from .. import db
from flask_login import login_required, login_user, logout_user
from ..email import mail_message
from werkzeug.security import generate_password_hash,check_password_hash



@main.route('/')
def index():
    # initialize() #initializes db
    form = CommentForm()
    blog_array = set(Blog.query.all())
    blogs = set(sorted(blog_array, key= lambda x: x.date, reverse = True))
    print(blogs)
    return render_template('index.html',form = form, blogs = blogs)

@main.route('/profile')
@login_required
def profile():
    current_user = User.query.filter_by(logged_in = True).first()
    blogs = Blog.query.filter_by(user_id = current_user.user_id).all()
    return render_template('profile.html', blogs = blogs)
    
@main.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    title = "Please Login into your account"
    if form.validate_on_submit():
        former_user = User.query.filter_by(logged_in = True).first()
        if former_user:
            former_user.logged_in = False
        db.session.commit()
        current_user = User.query.filter_by(username = form.username.data).first()
        if not current_user:
            return redirect(url_for('main.login'))
        name = form.username.data
        current_user.logged_in = True
        db.session.commit()
        if current_user and current_user.verify_password(form.password.data):
            login_user(current_user)
            return redirect(url_for('main.index'))
        else:
            redirect(url_for('main.login'))
    
    return render_template('auth/login.html', form= form)

@main.route('/logout')
def logout():
    former_user = User.query.filter_by(logged_in = True).first()
    logout_user()
    return redirect(url_for('main.index'))

    
@main.route('/registration', methods = ['GET', 'POST'])
def registration():
    form = RegistrationForm()
    title = "Let's get you started!!"
    if form.validate_on_submit():
        username = form.username.data
        email = form.email_address.data
        user = User(username = form.username.data,email = form.email_address.data, password = generate_password_hash(form.password.data), logged_in = False)
        db.session.add(user)
        db.session.commit()
        # mail_message("Welcome to BlogMe", "welcome/welcome_user",email,user=user)
        return redirect(url_for('main.login'))
    return render_template('auth/register.html', form = form, title = title)

    return render_template('auth/register.html', form = form)

@main.route('/<blog>/comment/', methods = ['GET', 'POST'])
def comment(blog):

    return render_template('comment.html')




