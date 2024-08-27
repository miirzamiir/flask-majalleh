from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from database import db
from secrets import token_hex
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from article.models import Article, Category, Bookmark, Vote, Comment
from authentication.routes import auth_bp
from article.routes import article_bp
from user.routes import user_bp


load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.secret_key = token_hex(16)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(article_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp, url_prefix='/user')

@app.get('/')
@app.get('/index')
def home():
    articles =  Article.query.order_by(Article.date.desc()).limit(10).all()
    categories =  Category.query.order_by(Category.label).all()
    tag_box =  Article.tag_box_selector(session=db.session)
    slider =  Article.slider(session=db.session)
    return render_template('pages/index.html', articles=articles, categories=categories, tag_box=tag_box, slider=slider)

@app.get('/about')
def about():
    categories =  Category.query.order_by(Category.label).all()
    return render_template('pages/about.html', categories=categories)

@app.get('/search')
def search():
    return 'search'

@app.errorhandler(404)
def page_not_found(e):
    categories =  Category.query.order_by(Category.label).all()
    return render_template('errors/notfound.html', categories=categories), 404



if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    