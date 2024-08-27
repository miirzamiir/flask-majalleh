from flask import Blueprint, render_template, abort, session, redirect, flash, url_for
from .models import *  # Import your model here
from user.models import User

article_bp = Blueprint('article', __name__)

@article_bp.get('/<username>/<title>')
def article(username, title, template='single_article'):
    user = User.query.filter(User.username == username).first()
    if user == None:
        abort(404)
    article = Article.query.filter(Article.author_id == user.id, Article.title == title)
    if article == None:
        abort(404)
    
    return render_template(f'articles/{template}.html', article=article)

@article_bp.get('/article/new-article')
def new_article():
    categories = Category.query.order_by(Category.label).all()
    resp = render_template('/articles/new_article.html', categories=categories)
    if 'username' not in session:
        flash('برای نوشتن مطلب جدید ابتدا باید وارد حساب کاربری خود شوید.', 'danger')
        resp = redirect(url_for('auth.login'))
    return resp