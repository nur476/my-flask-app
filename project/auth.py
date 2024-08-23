from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        if not email:
            flash('E-posta adresi boş olamaz.')
            return redirect(url_for('auth.login'))
        if not password:
            flash('Şifre boş olamaz.')
        elif len(password) < 8:
            flash('Şifre en az 8 karakter uzunluğunda olmalıdır.')

            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Lütfen giriş bilgilerinizi kontrol edin ve tekrar deneyin.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    flash('Geçersiz istek', 'ERROR!')
    return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if not email:
            flash('E-posta adresi boş olamaz.')
            return redirect(url_for('auth.login'))
    if not password:
            flash('Şifre boş olamaz.')
    elif len(password) < 8:
            flash('Şifre en az 8 karakter uzunluğunda olmalıdır.')

    
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email adresi zaten mevcut.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yaptınız.', 'Başarılı')
    return redirect(url_for('main.index'))
