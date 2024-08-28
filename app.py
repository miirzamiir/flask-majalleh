from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
from database import db
from secrets import token_hex
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from article.models import Article, Category, Bookmark, Vote, Comment
from authentication.routes import auth_bp
from article.routes import article_bp
from user.routes import user_bp
from hashlib import sha256


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
    return 'search'

@app.errorhandler(401)
def unauthorized(e):
    categories =  Category.query.order_by(Category.label).all()
    return render_template('errors/unauthorized.html', categories=categories), 401

@app.errorhandler(404)
def page_not_found(e):
    categories =  Category.query.order_by(Category.label).all()
    return render_template('errors/notfound.html', categories=categories), 404

@app.post('/upload')
def upload_file():
    resp = redirect(request.url)
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    file = None
    if 'file' in request.files:
        file = request.files['file']
    ftype = None
    if file is not None:
        fbytes = file.read()
        filename = sha256(fbytes).hexdigest() 
        _, ext = os.path.splitext(file.filename.lower())
        if ext in image_extensions:
            ftype = 'images'
        elif ext in video_extensions:
            ftype = 'videos'

    if ftype is not None:
        path = os.path.join(app.config['UPLOAD_FOLDER'], ftype, filename+ext)
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(fbytes)
        resp = url_for('static', filename=f'contents/{ftype}/{filename+ext}')
    return resp



if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    