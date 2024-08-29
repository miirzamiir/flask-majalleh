from flask import Blueprint, render_template, session, flash, redirect, url_for, request, send_from_directory, abort
from .models import User  
from article.models import Article, Category
import os
from database import db
from .utils import validate_user

user_bp = Blueprint('user', __name__)

@user_bp.get('/')
def dashboard():
    if session.get('username'):
        user = User.query.filter(User.username==session.get('username')).first()
        categories = Category.query.order_by(Category.label).all()
        articles = Article.query.filter(Article.author_id==user.id).order_by(Article.date.desc()).all()
        
        return render_template('account/dashboard.html', user=user, categories=categories, articles=articles)
    else:
        flash('برای دسترسی به پنل کاربری ابتدا باید وارد حساب کاربری خود شوید.', 'danger')
        return redirect(url_for('auth.login'))

@user_bp.get('/edit')
def update_profile():
    if session.get('username'):
        user = User.query.filter(User.username==session.get('username')).first()
        categories = Category.query.order_by(Category.label).all()

        return render_template('account/edit_profile.html', user=user, categories=categories)
    else:
        flash('برای دسترسی به پنل کاربری ابتدا باید وارد حساب کاربری خود شوید.', 'danger')
        return redirect(url_for('auth.login'))

@user_bp.post('/editpost')
def update_profile_post():
    url = url_for('auth.login')
    if session.get('username'):
        user = User.query.filter(User.username==session.get('username')).first()

        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        phonenumber = request.form.get('phone').strip()
        birth_date = request.form.get('birth_date').strip()
        profile_image = request.form.get('profile_image').strip()
        about = request.form.get('bio').strip()


        errors, date = validate_user(username, email, fname=first_name, lname=last_name, phone=phonenumber, 
                                     bdate=birth_date, curr_email=user.email, curr_phone=user.phonenumber, curr_username=user.username)

        if not errors:
            try:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.phonenumber = phonenumber
                user.birth_date = date
                user.profile_image = profile_image
                user.about = about
                db.session.commit()
                flash('تغییرات با موفقیت اعمال شد', category='success')
            except:
                flash('خطا در برقراری با سرور', category='danger')
        else:
            for error in errors:
                flash(error, category='danger')

        url = '/user/edit'
    
    return url

@user_bp.get('/<username>')
def profile(username):
    user = User.query.filter(User.username==username).first()
    if user is None:
        abort(404)
    articles = Article.query.filter(Article.author_id==user.id).all()
    tag_box = Article.tag_box_selector(session=db.session)
    slider = Article.slider(session=db.session)
    return render_template('account/author.html', user=user, articles=articles, tag_box=tag_box, slider=slider)

@user_bp.get('/media/<path:path>')
def show_user_media(path):
    return send_from_directory(directory=os.getenv('PROFILE_IMG_DIR'), path=path)