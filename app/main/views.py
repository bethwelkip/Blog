from flask import render_template,request,redirect,url_for, abort
from ..models import User, Blog, Comment, Subscriber
from .forms import BlogForm,UpdateForm, LoginForm, RegistrationForm, CommentForm, DeleteForm, SubscribeForm
from . import main
from .fill_db import initialize
from .. import db
from flask_login import login_required, login_user, logout_user
from ..email import mail_message
from werkzeug.security import generate_password_hash,check_password_hash



@main.route('/')
def index():
    user = User.query.all()
    if not user:
        initialize() #initializes db
    form = SubscribeForm()
    if form.validate_on_submit:
        name = form.name.data
        email = form.email.data
        print(email)
        # subscriber = Subscriber(name = name, email = email)
        # db.session.add(subscriber)
        # db.session.commit()
        # return redirect(url_for('main.index'))
    blog_array = Blog.query.all()
    blogs = sorted(blog_array, key= lambda x: x.date, reverse = True)
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
    
    return render_template('auth/login.html', form = form)

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
    comment = CommentForm()
    update = UpdateForm()
    delete = DeleteForm()
    if delete.validate_on_submit:
        #user = User.query.filter_by(logged_in = True).first()
        #blogs = user.blogs
        #titles = [blog.title for blog in blogs]
        #if blog in titles:
            #current.blog = Blog.query.filter_by(title = blog).first()
            #comments = current_blog.comments
            #
        #   
        pass
    blog = Blog.query.filter_by(title = blog).first()
    return render_template('comment.html', blog = blog, delete = delete, update = update, comment = comment)

@main.route('/blog/new', methods = ['GET', 'POST'])
def add():
    form = BlogForm()
    comment = CommentForm()
    update = CommentForm()
    delete = CommentForm()
    blog = Blog.query.filter_by(title = blog).first()
    return render_template('comment.html', form = form)

@main.route('/<blog>/update', methods = ['GET', 'POST'])
def update(blog):
    blog = Blog.query.filter_by(title = blog).first()
    form = CommentForm()
    update = UpdateForm()
    delete = CommentForm()
    return render_template('comment.html', blog = blog)




@main.route('/', methods = ['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit:
        name = form.name.data
        email = form.email.data
        print(name)
        subscriber = Subscriber(name = name, email = email)
        db.session.add(subscriber)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('footer.html', form)




