from flask import Blueprint, request, render_template, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from user.models import User
from database import db
from user.utils import validate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.get('/login')
def login():
    backurl = request.args.get('backurl', None)
    return render_template('account/login.html', backurl=backurl)

@auth_bp.post('/loginpost')
def login_post():
    backurl = request.args.get('backurl', None)
    username = request.form.get('username')
    password = request.form.get('password')

    redirect_path = url_for('auth.login', backurl=backurl)

    user = User.query.filter(User.username==username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = user.username
        if backurl:
            redirect_path = backurl
        else:
            redirect_path = '/'
    else:
        flash('ورود ناموفق. اطلاعات ورودی را بازبینی کنید.', 'danger')
    
    return redirect(redirect_path)

@auth_bp.get('/register')
def register():
    return render_template('account/register.html')

@auth_bp.post('/registerpost')
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    re_password = request.form.get('repassword')

    
    errors, _ = validate_user(username=username, email=email, password=password)
    redirect_path = '/register'

    if not errors:
        if password!=re_password:
            flash('رمز عبور با تکرارش مطابقت ندارد.', 'danger')
        else:
            hashed_password = generate_password_hash(password=password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('ثبت نام با موفقیت انجام شد.', 'success')
            redirect_path = '/login'
    else:
        for error in errors:
            flash(error, category='danger')

    return redirect(redirect_path)

@auth_bp.post('/logout')
def logout():
    if session.get('username'):
        session.pop('username', None)  
        
    return redirect('/')