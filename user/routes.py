from flask import Blueprint, render_template
from .models import ArticleModel  # Import your model here

article_bp = Blueprint('article', __name__)

@article_bp.route('/articles')
def list_articles():
    articles = ArticleModel.query.all()
    return render_template('articles.html', articles=articles)
