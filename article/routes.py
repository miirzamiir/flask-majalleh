from flask import Blueprint, render_template, abort, session, request, redirect, flash, url_for, jsonify
from .models import *
from user.models import User
from persiantools.jdatetime import JalaliDate

article_bp = Blueprint('article', __name__)

def validate_article(author_id, title, summary, category_label, content, curr_article_title=''):
    errors = []
    if title == '':
        errors.append('عنوان مقاله نمیتواند خالی باشد')
    elif Article.query.filter(Article.author_id == author_id, Article.title == title).first() is not None \
          and curr_article_title != title:
        errors.append('مقاله با این عنوان قبلا ثبت شده')
    if summary == '':
        errors.append('خلاصه مقاله نمیتواند خالی باشد')
    if category_label == '' or not Category.query.filter(Category.label == category_label).first():
        errors.append('دسته بندی باید انتخاب شود')
    if content == '':
        errors.append('محتوای مقاله نمیتواند خالی باشد')

    return errors

@article_bp.get('/<username>/<title>')
def article(username, title, template='single_article'):
    user = User.query.filter(User.username == username).first()
    if user == None:
        abort(404)
    article = Article.query.filter(Article.author_id == user.id, Article.title == title).first()
    categories = Category.query.order_by(Category.label).all()
    tags = article.tags.split(' ')
    persian_date = JalaliDate(article.date)
    if article == None:
        abort(404)
    
    return render_template(f'articles/{template}.html', article=article, user=article.author, tags=tags, date=persian_date, categories=categories)


@article_bp.get('/article/new-article')
def new_article():
    categories = Category.query.order_by(Category.label).all()
    resp = render_template('/articles/new_article.html', categories=categories, article=None)
    if 'username' not in session:
        flash('اول باید وارد حساب کاربری خود شوید', 'warning')
        resp = redirect('/login')
    return resp

@article_bp.get('/<username>/<title>/edit-article')
def edit_article(username, title):
    if 'username' not in session:
        abort(401)
 
    if session['username'] != username:
        abort(401)
    user = User.query.filter(User.username == username).first()
    article = Article.query.filter(Article.author_id == user.id, Article.title == title).first()
    if article is None:
        abort(404)
    categories = Category.query.order_by(Category.label).all()
    resp = render_template('/articles/new_article.html', categories=categories, article=article)  

    return resp
    

@article_bp.post('/article/save-article')
def save_article():
    if 'username' not in session:
        route = 'auth.login'
        flash('برای ثبت مقاله ابتدا باید وازد حساب کاربری خود شوید', category='warning')
    else:
        route = 'article.new_article'
        user = User.query.filter(User.username == session['username']).first()
        title = request.form.get('title').strip()
        image = request.form.get('image').strip()
        summary = request.form.get('summary').strip()
        tags = request.form.get('tags').strip()
        category_label = request.form.get('category').strip()
        content = request.form.get('html-content').strip()

        errors = validate_article(user.id, title, summary, category_label, content)

        if not errors:
            try:
                if image in ('', 'http://127.0.0.1:5000/article/new-article'):
                    image = url_for('static', filename='images/article-default.png')
                category = Category.query.filter(Category.label == category_label).first()
                db.session.add(Article(title, image, summary, content, tags, category.id, user.id))
                db.session.commit()
                route = 'user.dashboard'
            except:
                flash('خطا در برقراری با سرور', category='danger')
        else:
            for error in errors:
                flash(error, category='danger')

    return url_for(route)


@article_bp.post('/<username>/<title>/save-edit-article')
def save_edit_article(username, title):
    if 'username' not in session:
        return jsonify({'status': 401, 'error': 'unauthorized'}), 401

    if session['username'] != username:
        return jsonify({'status': 401, 'error': 'unauthorized'}), 401

    user = User.query.filter(User.username == username).first()
    article = Article.query.filter(Article.author_id == user.id, Article.title == title).first()
    if article is None:
        return jsonify({'status': 404, 'error': 'not found'}), 404
    user = User.query.filter(User.username == session['username']).first()
    title = request.form.get('title').strip()
    image = request.form.get('image').strip()
    summary = request.form.get('summary').strip()
    tags = request.form.get('tags').strip()
    category_label = request.form.get('category').strip()
    content = request.form.get('html-content').strip()
    errors = validate_article(user.id, title, summary, category_label, content, article.title)
    if not errors:
        try:
            category = Category.query.filter(Category.label == category_label).first()

            article.title = title
            article.image = image
            article.summary = summary
            article.tags = tags
            article.category_id = category.id
            article.content = content
            db.session.commit()
            return url_for('user.dashboard')
        except:
            flash('خطا در برقراری با سرور', category='danger')
    else:
        for error in errors:
            flash(error, category='danger')

    return url_for('article.edit_article', username=user.username, title=article.title)

@article_bp.get('/<username>/<title>/delete-article')
def delete_article(username, title):
    if 'username' not in session:
        abort(401)
    
    if session['username'] != username:
        abort(401)

    user = User.query.filter(User.username == username).first()
    article = Article.query.filter(Article.author_id == user.id, Article.title == title).first()

    if article is None:
        abort(404)
    try:
        db.session.delete(article)
        db.session.commit()
        flash('مقاله با موفقیت حذف شد', category='success')
    except:
        flash('خطا در برقراری با سرور', category='danger')

    return redirect(url_for('user.dashboard'))


@article_bp.post('/add-comment')
def add_comment():
    url = url_for('auth.login')
    if 'username' in session:
        data = request.json

        user = User.query.filter(User.username == session['username']).first()

        author = User.query.filter(User.username == data['username']).first()

        article = Article.query.filter(Article.author_id == author.id, Article.title == data['title']).first()

        parent = None
        if data.get('parent_id'):
            parent = int(data['parent_id'])

        db.session.add(Comment(user.id, article.id, data['text'], parent))
        db.session.commit()

        url = url_for('article.article', username=data['username'], title=data['title'])

    return url

        

        
    
