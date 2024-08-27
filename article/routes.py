from flask import Blueprint, render_template
from .models import UserModel  # Import your model here

user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def list_users():
    users = UserModel.query.all()
    return render_template('users.html', users=users)
