from user.models import *
from article.models import *
from database import db
import os

if not os.path.exists('static/contents/images'):
    os.makedirs('static/contents/images')

if not os.path.exists('static/contents/videos'):
    os.makedirs('static/contents/videos')

with app.app_context():
    db.create_all()