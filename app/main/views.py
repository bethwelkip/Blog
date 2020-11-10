from flask import render_template,request,redirect,url_for, abort
from ..models import User, Blog, Comment, Subscriber
from .forms import BlogForm,UpdateForm, LoginForm, RegistrationForm, CommentForm, DeleteForm, SubscribeForm
from . import main
from .fill_db import initialize
from .. import db
from ..request import get_quote
import datetime
from flask_login import login_required, login_user, logout_user,current_user
from ..email import mail_message, mail_subscribe
from werkzeug.security import generate_password_hash,check_password_hash


@main.route('/')
def index():
    quote = get_quote()
    user = User.query.all()
    if not user:
        initialize() #initializes db
    form = SubscribeForm()
    # if form.validate_on_submit:
    #     name = form.name.data
    #     email = form.email.data
        # subscriber = Subscriber(name = name, email = email)
        # db.session.add(subscriber)
        # db.session.commit()
        # return redirect(url_for('main.index'))
    blog_array = Blog.query.all()
    blogs = sorted(blog_array, key= lambda x: x.date, reverse = True)
    return render_template('index.html',quote = quote, form = form, blogs = blogs)

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
        mail_message("Welcome to BlogMe", "welcome/welcome_user",email,user=user)
        return redirect(url_for('main.login'))
    return render_template('auth/register.html', form = form, title = title)

    return render_template('auth/register.html', form = form)

@main.route('/<blog>/comment/', methods = ['GET', 'POST'])
def comment(blog):
    blogg = Blog.query.filter_by(title = blog).first()
    comment = CommentForm()
    update = UpdateForm()
    delete = DeleteForm()
    comments = blogg.comments
    form = BlogForm()
    form.title.data = blogg.title
    form.blog.data =" blogg.blog"
    if update.update.data:
        if request.method == 'POST':
            form.title.data = blogg.title
            form.blog.data = blogg.blog
        form.populate_obj(blogg)
        print("here")
        return redirect(url_for('main.add', form =  BlogForm(blog = blogg.blog)))
        
    return render_template('comment.html', blog = blogg, delete = delete, update = update, comment = comment)

@main.route('/blog/new', methods = ['GET', 'POST'])
@login_required
def add():
    blogs = current_user.blogs
    for blog in blogs:
        if blog.blog is None:
            db.session.delete(blog)
            db.session.commit()
    form = BlogForm()
    comment = CommentForm()
    update = CommentForm()
    delete = CommentForm()
    user = User.query.filter_by(logged_in = True).first()
    if form.validate_on_submit():
        blog = Blog(date = datetime.datetime.now(), blog = form.blog.data, title = form.title.data, user_id = user.user_id)
        db.session.add(blog)
        db.session.commit()
        subscribers = Subscriber.query.all()
        for subscriber in subscribers:
            mail_subscribe("New Post Is UP!!!","new_post/post.txt",subscriber.email,user = subscriber)
    return render_template('add.html', form = form)

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
        subscriber = Subscriber(name = name, email = email)
        db.session.add(subscriber)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('footer.html', form)




