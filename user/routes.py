from flask import Blueprint, render_template, redirect, session, request, flash, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_bp = Blueprint('user', __name__)


@user_bp.get('/login')
def login():
    resp = redirect('pages/index')
    if 'username' not in session:
        resp = render_template('account/login.html')
    return resp

@user_bp.post('/loginpost')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    redirect_path = '/users/login'

    user = User.query.filter(User.username==username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = user.username
        redirect_path = '/'
    else:
        flash('ورود ناموفق. اطلاعات ورودی را بازبینی کنید.', 'danger')
    
    return redirect(redirect_path)

@user_bp.get('/register')
def register():
    return render_template('account/register.html')

@user_bp.post('/registerpost')
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    re_password = request.form.get('repassword')

    redirect_path = url_for('user.register')
    existing_user = User.query.filter((User.username==username) | (User.email==email)).first()
    
    if existing_user:
        flash('نام کاربری یا ایمیل تکراری است.', 'danger')

    elif password!=re_password:
        flash('رمز عبور با تکرارش مطابقت ندارد.', 'danger')


    elif password==re_password:
        hashed_password = generate_password_hash(password=password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('ثبت نام با موفقیت انجام شد.', 'success')
        redirect_path = '/users/login'

    return redirect(redirect_path)