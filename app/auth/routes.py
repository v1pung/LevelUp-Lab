from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import LoginForm, RegForm, AvatarForm
from .model import Users
from ..extensions import db
from ..utils import save_picture

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and check_password_hash(user.psw, form.psw.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for('ranks.stats'))
        else:
            flash("Неверная пара логин/пароль", "danger")

    return render_template("auth/login.html", title="Авторизация", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()

    if form.validate_on_submit():
        hashed_psw = generate_password_hash(form.psw.data)
        user = Users(login=form.login.data, psw=hashed_psw)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'{form.login.data} registered successfully!', "success")
            login_user(user)
            return redirect(url_for('ranks.stats'))
        except Exception as e:
            print('bd error ' + str(e))
            flash("Registration error", "error")

    return render_template('auth/register.html', title="Регистрация", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = AvatarForm()
    if request.method == 'POST':
        file = form.avatar.data
        if file.filename != '':
            filename = save_picture(file)
            current_user.avatar = url_for('static', filename='upload/' + filename)
            db.session.commit()
            return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form)