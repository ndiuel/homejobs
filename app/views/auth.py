from flask import Blueprint, render_template, redirect, url_for, request,  flash, current_app
from flask_login import current_user, login_user, login_required, logout_user
from ..forms.auth import LoginForm, SignUpForm
from ..models import User, Provider


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('user.index'))
    return render_template('login.html', form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
                    email=form.email.data,
                    password=form.password.data,
                    )
        user.add_role('normal')
        user.save()
        if form.is_provider.data:
            provider = Provider()
            provider.user_id = user.id 
            provider.save()
            user.add_role('provider')
        flash("Account created successfully")
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
