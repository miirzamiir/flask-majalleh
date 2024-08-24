from database import db
from sqlalchemy import Integer, String, ForeignKey, Text
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


    class Profile(db.Model):
        __tablename__ = 'profiles'
        id = mapped_column(Integer, primary_key=True, autoincrement=True)
        email = mapped_column(String(50), nullable=True)
        phonenumber = mapped_column(String(20), nullable=True)
        profile_image = mapped_column(String(128), nullable=True)
        about = mapped_column(Text, nullable=True)
        user_id = mapped_column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

        def __init__(self, email, phonenumber, profile_image, about, user_id):
            super().__init__()
            self.email = email
            self.phonenumber = phonenumber
            self.profile_image = profile_image
            self.about = about
            self.user_id = user_id