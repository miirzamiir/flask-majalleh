from flask import Flask
from database import db
from config import DATABASE_URI, HOST, PORT
from secrets import token_hex

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.secret_key = token_hex(16)

db.init_app(app)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
