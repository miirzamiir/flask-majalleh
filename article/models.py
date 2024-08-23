from database import db
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship


class Category(db.Model):
    __tablename__ = 'category'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    label = mapped_column(String(50), unique=True, nullable=False)
    articles = relationship('Article', backref='category')

    def __init__(self, label):
        super().__init__()
        self.label = label
    
    def __str__(self):
        return self.label


class Article(db.Model):
    __tablename__ = 'articles'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(100))
    image = mapped_column(String, nullable=True)
    summary = mapped_column(String(400))
    text = mapped_column(Text)
    tags = mapped_column(String(200), nullable=True)
    category_id = mapped_column(Integer, ForeignKey('category.id'), nullable=True)
    author_id = mapped_column(Integer, ForeignKey('users.id'))
    bookmarks = relationship('Bookmark', backref='articles')

    @classmethod
    def tag_split(cls, session):
        splitted_tags = []
        articles = session.query(cls).order_by(cls.date.desc()).limit(10).all()
        for article in articles:
            if len(splitted_tags) > 12:
                break
            else:
                splitted_tags = list(set(splitted_tags.extend(article.tags.split()))) 
        return splitted_tags
    
    def __str__(self):
        return self.title


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    article_id = mapped_column(Integer, ForeignKey('articles.id'), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
