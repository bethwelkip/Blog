from datetime import date
import time, datetime
from .. import db
from ..models import User, Blog, Comment
from werkzeug.security import generate_password_hash, check_password_hash
 
def initialize():

    users = [("Bethwel", "Kip", "bethwelkiplimo@gmail.com", False), ("Brian", "Kos", "kos@kos.com", False), ("Dominic", "Tei", "tei@tei.com", False), ("Elvos", "Ron", "ron@ron.com", False)]
    for user, password, email, log in users:
        user = User(username = user, password = generate_password_hash(password), email =email, logged_in = log)
        db.session.add(user)
        db.session.commit()
    now = datetime.datetime.now()
    print(now)
    blogs = [("Life", "No one knows how it goes", now), ("Biking", "Such a great activity", now), ("Moringa", "Such a great place",datetime.datetime.now()),("Blog", "A nice to have thing", datetime.datetime.now())]
    usees = User.query.all()
    for user in usees:
        for title, blog, date in blogs:
            new_blog = Blog(title = title, blog = blog, date = date, user_id = user.user_id)
            db.session.add(new_blog)
            db.session.commit()

    comments = ["I loved reading your article", "Good work", "Too many typos", "Would love to read more", "I have repeated this comments"]
    blogs = Blog.query.all()
    for blog in blogs:
        for comment in comments:
            new_comment = Comment(comment=comment,blog_id = blog.blog_id)
            db.session.add(new_comment)
            db.session.commit()

