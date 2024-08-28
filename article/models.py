from database import db
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship, backref
from datetime import datetime
from user.models import User


class Category(db.Model):
    __tablename__ = 'categories'
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
    title = mapped_column(String(100), nullable=False)
    image = mapped_column(String, nullable=True)
    summary = mapped_column(String(400), nullable=False)
    text = mapped_column(Text, nullable=False)
    tags = mapped_column(String(200), nullable=True)
    category_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)
    author_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    date = mapped_column(DateTime, default=datetime.now()) 
    bookmarks = relationship('Bookmark', backref='articles') 
    votes = relationship('Vote', backref='articles')

    def __init__(self, title, image, summary, text, tags, category_id, author_id) -> None:
        super().__init__()
        self.title = title
        self.image = image
        self.summary = summary
        self.text = text
        self.tags = tags
        self.category_id = category_id
        self.author_id = author_id

    @classmethod
    def tag_box_selector(cls, session):
        selected_tags = []
        articles = session.query(cls).order_by(cls.date.desc()).limit(10).all()
        for article in articles:
            if len(selected_tags) > 12:
                break
            selected_tags.extend(article.tags.split())
        return list(set(selected_tags))
    
    @classmethod
    def slider(cls, session):
        slider = []
        for article in session.query(cls).order_by(cls.date.desc()).limit(10).all():
            slider.append(article.image)
        return slider
    
    @property
    def author(self):
        return User.query.get(self.author_id)
    
    @property
    def category(self):
        return Category.query.get(self.category_id)

    def calculate_votes(self):
        return sum(vote.vote for vote in self.votes)
    
    def __str__(self):
        return self.title


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    article_id = mapped_column(Integer, ForeignKey('articles.id'), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)

    def __init__(self, article_id, user_id) -> None:
        super().__init__()
        self.article_id = article_id
        self.user_id = user_id


class Vote(db.Model):
    __tablename__ = 'votes'
    article_id = mapped_column(Integer, ForeignKey('articles.id'), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    vote = mapped_column(Integer, nullable=False)

    def __init__(self, article_id, user_id, vote) -> None:
        super().__init__()
        self.article_id = article_id
        self.user_id = user_id
        self.vote = 1 if vote > 0 else -1 

    def __str__(self):
        return f'<Vote user_id={self.user_id}, article_id={self.article_id}, vote={self.vote}>'
    

class Comment(db.Model):
    __tablename__ = 'comments'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    article_id = mapped_column(Integer, ForeignKey('articles.id'), nullable=False)
    text = mapped_column(String(128))
    parent_id = mapped_column(Integer, ForeignKey('comments.id'), nullable=True)
    replies = relationship('Comment', backref=backref('parent', remote_side=[id]), lazy=True)


    def __init__(self, user_id, article_id, text, parent_id=None):
        super().__init__()
        self.user_id = user_id
        self.article_id = article_id
        self.text = text
        self.parent_id = parent_id
