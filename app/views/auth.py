from flask import Blueprint, render_template, redirect, url_for, request,  flash, current_app
from flask_login import current_user, login_user, login_required, logout_user
from ..forms.auth import LoginForm, SignUpForm
from ..models import User


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('user.index'))
    return render_template('login.html', form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(phone_no=form.phone_no.data,
                    email=form.email.data,
                    password=form.password.data,
                    username=form.username.data,
                    )
        user.add_role('normal')
        user.save()
        flash("Account created successfully, you can now login")
        return redirect(url_for('auth.login'))
    if form.errors:
        flash(str(form.errors).replace('[', '').replace(
            '{', '').replace('}', '').replace(']', ''), category='error')
    return render_template('signup.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
