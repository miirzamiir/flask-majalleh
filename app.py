from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from database import db
from secrets import token_hex
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash
from article.models import Article, Category, Bookmark, Vote, Comment
from user.models import User, Profile


load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.secret_key = token_hex(16)

db.init_app(app)
migrate = Migrate(app, db)

# app.register_blueprint(user_bp, url_prefix='/user')
# app.register_blueprint(article_bp, url_prefix='/article')

@app.get('/')
def home():

    context = {
        'articles': Article.query.order_by(Article.date.desc()).limit(10).all(),
        'categories': Category.query.order_by(Category.label).all(),
        'tag_box': Article.tag_box_selector(session=db.session),
        'slider': Article.slider(session=db.session)
    }
    return render_template('pages/index.html', context=context)

@app.get('/about')
def about():
    context = {
        'categories': Category.query.order_by(Category.label).all()
    }
    return render_template('pages/about.html', context=context)

@app.get('/login')
def login():
    return render_template('account/login.html')

@app.post('/loginpost')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    redirect_path = '/login'

    user = User.query.filter(User.username==username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = user.username
        redirect_path = '/'
    else:
        flash('ورود ناموفق. اطلاعات ورودی را بازبینی کنید.', 'danger')
    
    return redirect(redirect_path)

@app.get('/register')
def register():
    return render_template('account/register.html')

@app.post('/registerpost')
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    re_password = request.form.get('repassword')

    redirect_path = url_for('register')
    existing_user = User.query.filter((User.username==username) | (User.email==email)).first()
    
    if existing_user:
        flash('نام کاربری یا ایمیل تکراری است.', 'danger')

    elif password!=re_password:
        flash('رمز عبور با تکرارش مطابقت ندارد.', 'danger')


    elif password==re_password:
        hashed_password = generate_password_hash(password=password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('ثبت نام با موفقیت انجام شد.', 'success')
        redirect_path = '/login'

    return redirect(redirect_path)

@app.get('/search')
def search():
    return 'search'

@app.get('/logout')
def logout():
    session.pop('user_id', None)  
    flash('You have been logged out.', 'success')
    return redirect('/')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
    