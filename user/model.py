from database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship

class User(db.Model):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)
    profile = relationship('Profile', backref='usres', uselist=False)
    articles = relationship('Article', backref='users')
    bookmarks = relationship('Bookmark', backref='users')

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password