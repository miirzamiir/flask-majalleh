from flask import Blueprint, render_template, abort, session, request, redirect, flash, url_for
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


@article_bp.get('/article/new-article')
def new_article():
    categories = Category.query.order_by(Category.label).all()
    resp = render_template('/articles/new_article.html', categories=categories)
    if 'username' not in session:
        flash('اول باید وارد حساب کاربری خود شوید', 'warning')
        resp = redirect('/users/login')
    return resp

@article_bp.post('/article/save-article')
def save_article():
    if 'username' not in session:
        route = 'auth.login'
        flash('برای ثبت مقاله ابتدا باید وازد حساب کاربری خود شوید', category='warning')
    else:
        route = 'new-article'
        user = User.query.filter(User.username == session['username']).first()
        title = request.form.get('title')
        image = request.form.get('image')
        summary = request.form.get('summary')
        tags = request.form.get('tags')
        category_label = request.form.get('category')
        content = request.form.get('html-content')

        existed_article = Article.query.filter(Article.author_id == user.id, Article.title == title).first()

        if not existed_article:
            if image == '':
                # set default image for it
                pass
            
            try:
                category = Category.query.filter(Category.label == category_label).first()
                db.session.add(Article(title, image, summary, content, tags, category.id, user.id))
                db.session.commit()
                # set dashboard route of user
                route = ''
            except:
                flash('خطا در برقراری با سرور', category='danger')
        else:
            flash('شما مقاله با این عنوان را قبلا ثبت کرده‌اید', category='danger')

    return url_for(route)