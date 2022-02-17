from email.utils import unquote
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session, abort
from flask_login import current_user, login_required
from flask_mail import Message
from . import csrf
import jwt
from itertools import cycle

user = Blueprint('user', __name__)

            
@user.route("/settimezone", methods=['POST'])
@csrf.exempt
def timezone():
    timezone = request.get_json(force=True).get('timezone', 0)
    session['timezone'] = timezone
    return "ok"


@user.route("/")
def index():
    return render_template("index.html")


@user.route("/profile")
@login_required
def profile():
    return render_template("profile.html")