from flask import Blueprint, render_template, session, flash, redirect, url_for, request, send_from_directory
from .models import User  
from article.models import Article, Category
import re
import os
import datetime
from database import db
from werkzeug.utils import secure_filename


user_bp = Blueprint('user', __name__)

@user_bp.get('/')
def dashboard():
    if session.get('username'):
        user = User.query.filter(User.username==session.get('username')).first()

        context = {
            'user': user,
            'categories': Category.query.order_by(Category.label).all(),
            'articles': Article.query.filter(Article.author_id==user.id).order_by(Article.date.desc()).all()
        }
        return render_template('account/dashboard.html', context=context)
    else:
        flash('برای دسترسی به پنل کاربری ابتدا باید وارد حساب کاربری خود شوید.', 'danger')
        return redirect(url_for('login'))

@user_bp.get('/edit')
def update_profile():
    if session.get('username'):
        user = User.query.filter(User.username==session.get('username')).first()

        context = {
            'user': user,
            'categories': Category.query.order_by(Category.label).all(),
        }
        return render_template('account/edit_profile.html', context=context)
    else:
        flash('برای دسترسی به پنل کاربری ابتدا باید وارد حساب کاربری خود شوید.', 'danger')
        return redirect(url_for('login'))

@user_bp.post('/editpost')
def update_profile_post():
    if session.get('username'):
        user = User.query.filter(User.username==session.get('username')).first()

        first_name = request.form.get('first_name') 
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')        
        phonenumber = request.form.get('phone')
        birth_date = request.form.get('birth_date')
        about = request.form.get('bio')

        update_is_valid = True

        if username!=user.username:
            if re.match(r'^(?=.{4,})[a-z][a-z0-9_]*\d*$', username):
                if not User.query.filter(User.username==username).first():
                    user.username = username
                    session['username'] = user.username 
                else:
                    update_is_valid = False
                    flash(' نام کاربری تکراری است.', 'danger')
            else:
                update_is_valid = False
                flash('فرمت نام کاربری اشتباه است.', 'danger')

        if email!=user.email and User.query.filter(User.email==email).first():
            update_is_valid = False
            flash('ایمیل تکراری است.', 'danger')
        user.email = email

        if first_name!=user.first_name and first_name.strip():
            user.first_name = first_name
        
        if last_name!=user.last_name and last_name.strip():
            user.last_name = last_name
        
        if not re.match(r'^09\d{9}$', phonenumber):
            update_is_valid = False
            flash('شماره موبایل درست نیست.', 'danger')
        elif phonenumber!=user.phonenumber:
            user.phonenumber = phonenumber

        if about!=user.about:
            user.about = about

        if birth_date!=user.birth_date:
            if len(birth_date.split('-'))==3:
                bd = birth_date.split('-')
                year, month, day = int(bd[0]), int(bd[1]), int(bd[2])
                user.birth_date = datetime.date(year=year, month=month, day=day)
            else:
                update_is_valid = False
                flash('فرمت تاریخ تولد صحیح نیست.', 'danger')

        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        project_root = os.path.abspath(os.path.join(current_dir, '..'))

        pic = request.files.get('pic')
        if pic and pic.filename.split('.')[-1] in ALLOWED_EXTENSIONS:
            filename = session.get('username')+'_prof.'+pic.filename.split('.')[-1]
            file_path = os.path.join(project_root, os.getenv('PROFILE_IMG_DIR'))
            os.makedirs(file_path, exist_ok=True)
            file_path = os.path.join(file_path, filename)
            pic.save(file_path)
            user.profile_image = filename
        else:
            update_is_valid = False
            flash('عکس باید از یکی از فرمت های png, jpg و یا jpeg باشد.', 'danger')


        if update_is_valid:
            db.session.commit()

        context = {
            'user': user,
            'categories': Category.query.order_by(Category.label).all(),
        }
        return render_template('account/edit_profile.html', context=context)
    else:
        flash('برای دسترسی به پنل کاربری ابتدا باید وارد حساب کاربری خود شوید.', 'danger')
        return redirect(url_for('login'))

@user_bp.get('/<username>')
def profile(username):
    user = User.query.filter(User.username==username).first()
    if user:
        context = {
            'user': user,
            'articles': Article.query.filter(Article.author_id==user.id).all(),
            'tag_box': Article.tag_box_selector(session=db.session),
            'slider': Article.slider(session=db.session)
        }

        return render_template('account/author.html', context=context)

    # TODO -> Return 404

@user_bp.get('/media/<path:path>')
def show_user_media(path):
    return send_from_directory(directory=os.getenv('PROFILE_IMG_DIR'), path=path)