from database import db
from sqlalchemy import Integer, String, Text, Date
from sqlalchemy.orm import validates
from sqlalchemy.orm import mapped_column, relationship
from article.models import *

class User(db.Model):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = mapped_column(String(40), default='')
    last_name = mapped_column(String(40), default='')
    phonenumber = mapped_column(String(20), nullable=True)
    profile_image = mapped_column(String(128), nullable=True)
    birth_date = mapped_column(String(20), nullable=True)
    about = mapped_column(Text, nullable=True)
    articles = relationship('Article', backref='users')
    bookmarks = relationship('Bookmark', backref='users')
    votes = relationship('Vote', backref='users')

    def __init__(self, username, password, email):
        super().__init__()
        self.username = username.lower()
        self.password = password
        self.email = email.lower()


