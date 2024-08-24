from flask import Flask
from database import db
from secrets import token_hex
from dotenv import load_dotenv
import os
from user.model import *
from article.models import *


load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.secret_key = token_hex(16)

db.init_app(app)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)