from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, abort, make_response
from database import db
from secrets import token_hex
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from sqlalchemy import and_
from article.models import Article, Category, Bookmark, Vote, Comment
from authentication.routes import auth_bp
from article.routes import article_bp
from user.routes import user_bp
from hashlib import sha256
from werkzeug.middleware.proxy_fix import ProxyFix
import logging


load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['UPLOAD_FOLDER'] = 'static/contents/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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
    title_summary_query = request.args.get('q', '')
    tags_query = request.args.get('tags', '')
    category_query = request.args.get('category', '')

    query = Article.query

    if title_summary_query:
        query = query.filter(
            (Article.title.ilike(f'%{title_summary_query}%')) |
            (Article.summary.ilike(f'%{title_summary_query}%'))
        )

    if tags_query:
        filter_tag = []        
        [filter_tag.append(Article.tags.ilike(f'%{tag}%')) for tag in tags_query.split()]

        query = query.filter(and_(*filter_tag))

    if category_query:
        try:
            category_id = Category.query.filter(Category.label==category_query).first().id
            query = query.filter(Article.category_id == category_id)
        except:
           flash('چنین دسته بندی ای وجود ندارد.', 'warning')
            

    categories =  Category.query.order_by(Category.label).all()
    articles = query.all()
    tag_box =  Article.tag_box_selector(session=db.session)
    slider =  Article.slider(session=db.session)
    

    return render_template('search/search.html', categories=categories, articles=articles, tag_box=tag_box, slider=slider, q=title_summary_query, t=tags_query, c=category_query)

@app.get('/category')
def category():
    label = request.args.get('label', '')
    articles = None
    if label:
        try:
            category_id = Category.query.filter(Category.label==label).first().id
            articles = Article.query.filter(Article.category_id == category_id)
        except:
           flash('چنین دسته بندی ای وجود ندارد.', 'warning')
        
    
    categories =  Category.query.order_by(Category.label).all()
    tag_box =  Article.tag_box_selector(session=db.session)
    slider =  Article.slider(session=db.session)

    return render_template('search/category.html', articles=articles, categories=categories, tag_box=tag_box, slider=slider, q=label)

@app.get('/tag')
def tag():
    query = Article.query
    tags = request.args.get('tags', '')
    if tags:
        filter_tag = []        
        [filter_tag.append(Article.tags.ilike(f'%{tag}%')) for tag in tags.split()]

        query = query.filter(and_(*filter_tag))
        
    
    categories =  Category.query.order_by(Category.label).all()
    articles = query.all()
    tag_box =  Article.tag_box_selector(session=db.session)
    slider =  Article.slider(session=db.session)

    return render_template('search/category.html', articles=articles, categories=categories, tag_box=tag_box, slider=slider, q=tags)


@app.errorhandler(401)
def unauthorized(e):
    categories =  Category.query.order_by(Category.label).all()
    return render_template('errors/unauthorized.html', categories=categories), 401

@app.errorhandler(404)
def page_not_found(e):
    categories =  Category.query.order_by(Category.label).all()
    return render_template('errors/notfound.html', categories=categories), 404

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'status': 413, 'error': 'too large file', 'message': 'حجم فایل باید کمتر از ۱۶مگابایت باشد'}), 413

@app.post('/upload-video')
def upload_video():
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    return upload(video_extensions, 'videos')

@app.post('/upload-image')
def upload_image():
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    return upload(image_extensions, 'images')

def upload(extensions, ftype):
    file = None
    if 'file' in request.files:
        file = request.files['file']
    ext = ''
    if file is not None:
        _, ext = os.path.splitext(file.filename.lower())
    valid_types = ','.join(extensions)
    resp = jsonify({'status': 415, 'error': 'media not supported', 'message': f'فایل ورودی باید یکی از این موارد باشد ({valid_types})'}), 415
    if ext in extensions:
        resp = save_file(file, ext, ftype)
    return resp
    

def save_file(file, ext, ftype):
    fbytes = file.read()
    filename = sha256(fbytes).hexdigest() 
    path = os.path.join(app.config['UPLOAD_FOLDER'], ftype, filename+ext)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(fbytes)
    resp = jsonify({'status': 200, 'url': url_for('static', filename=f'contents/{ftype}/{filename+ext}')})
    return resp


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    