from flask import Flask, session
from flask_moment import Moment
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_static_digest import FlaskStaticDigest
from config import config
from uuid import uuid4
from datetime import datetime


moment = Moment()
digest = FlaskStaticDigest()
csrf = CSRFProtect()
mail = Mail()


def create_app(config_name):
    import urllib.parse as urlparse
    from urllib.parse import urlencode, unquote
    from flask import request
    from .utils import paginate, order_column
    from .models import ChatViews, Chat
    from flask_login import current_user
    import logging

    app = Flask(__name__)
    moment.init_app(app)
    digest.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    config_name = config_name if type(config_name) is str else 'default'
    config_object = config.get(config_name)
    app.config.from_object(config_object)
    config_object.init_app(app)

    app.paginate = paginate
    app.order_column = order_column
    last_cache_id = uuid4()

    @app.before_request
    def permanent_session():
        session.permanent = True

    @app.template_filter('cache_bust')
    def cache_bust(url):
        nonlocal last_cache_id
        if config_name != 'production':
            last_cache_id = uuid4()
        return f'{url}/?v={last_cache_id}'

    @app.context_processor
    def page():
        def page_link(p):
            print("page", p)
            url_parts = list(urlparse.urlparse(request.url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update({'page': p})
            url_parts[4] = urlencode(query)
            return urlparse.urlunparse(url_parts)
        return {'page_link': page_link, 'unquote': unquote}

    @app.template_filter('countdown')
    def countdown(time):
        diff = time - datetime.utcnow()
        seconds = diff.total_seconds()
        if seconds <= 0:
            return "0d:0h:0m:0s"
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(round(rem), 3600)
        minutes, rem = divmod(round(rem), 60)
        return f"{int(days)}d:{int(hours)}h:{int(minutes)}m:{round(rem)}s"

    @app.template_filter('date')
    def date(obj):
        return obj.strftime('%d/%m/%Y %H:%M:%S')

    def money(num):
        if not num:
            return "0"
        num = f"{num:.30f}".rstrip('0')
        parts = num.split('.')
        result = f'{int(parts[0]):,d}'
        parts = [p for p in parts if p]
        if len(parts) > 1 and 'e' in parts[1]:
            n = str(float(parts[1]))
            parts[1] = n.split('.')[1]

        if len(parts) > 1 and int(parts[1]) > 0:
            s = parts[1]
            s = float(f'0.{s}')
            s = float(f"{s:.3}")
            parts[1] = f"{s:.9f}".rstrip('0').split('.')[-1]
            result = f"{result}.{parts[1]}"
        return result.rstrip('.')

    def naira(num):
        num = num or 0
        num = str(num / 100)
        arr = num.split('.')
        first = f'{int(arr[0]):,d}'
        if len(arr) > 1:
            second = arr[1]
            return first
        return first

    app.money = money
    app.naira = naira

    app.template_filter('money')(money)
    app.template_filter('naira')(naira)
    
    def is_new_chat(chat):
        view = ChatViews.query.filter_by(user_id=current_user.id).order_by(ChatViews.date_created.desc()).first()
        return view and view.date_created <= chat.date_modified

    def new_chat():
        if current_user.is_authenticated:
            chats=Chat.query.filter((Chat.user_1_id == current_user.id) | (Chat.user_2_id == current_user.id)) 
            return any(is_new_chat(chat) for chat in chats)

    @app.context_processor
    def money():
        def filter_actions(arr):
            return list(filter(lambda i: i[-1], arr))
        return {'filter_actions': filter_actions, 'len': len, 'list': list, 'int': int, 'vars': vars, 'new_chat': new_chat}

    from . import models
    from . import forms
    from . import views

    models.init_app(app)
    forms.init_app(app)
    views.init_app(app)

    return app
