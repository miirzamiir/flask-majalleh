from flask import Blueprint, render_template, abort, session, redirect, flash
from .models import *  # Import your model here
from user.models import User

article_bp = Blueprint('article', __name__)

@article_bp.get('/<username>/<title>/single-article')
@article_bp.get('/<username>/<title>')
def single_article(username, title):
    user = User.query.filter(User.username == username).first()
    if user == None:
        abort(404)
    artile = Article.query.filter(Article.author_id == user.id, Article.title == title)
    if artile == None:
        abort(404)
    return render_template('articles/single_article.html', artile=artile)



@article_bp.get('/<username>/<title>/full-width')
def full_width(username, title):
    user = User.query.filter(User.username == username).first()
    if user == None:
        abort(404)
    artile = Article.query.filter(Article.author_id == user.id, Article.title == title)
    if artile == None:
        abort(404)
    return render_template('articles/full-width.html', artile=artile)

@article_bp.get('/article/new-article')
def new_article():
    categories = Category.query.order_by(Category.label).all()
    resp = render_template('/articles/new_article.html', categories)
    if 'username' not in session:
        flash('اول باید وارد حساب کاربری خود شوید', 'warning')
        resp = redirect('/users/login')
    return resp