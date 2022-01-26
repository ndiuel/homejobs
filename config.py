import os
from itertools import cycle
from random import shuffle

basedir = os.path.abspath(os.path.dirname(__file__))

arr = [31, 12, 2]

class Config:
    APP_NAME = "DAILYBREAD"
    BENEFACTORS = cycle(arr)
    UPLOAD_PATH = os.path.join(basedir, 'app', 'static', 'uploads')
    URL = os.environ.get("URL") or 'localhost:5000'
    SECRET_KEY = 'svav690-behd-4e6d-b117-7b7d92ba3a00'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'mail.daily-bread.com.ng'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ('', '')
    FLASK_STATIC_DIGEST_BLACKLIST_FILTER = []
    FLASK_STATIC_DIGEST_GZIP_FILES = True
    FLASK_STATIC_DIGEST_HOST_URL = None
    ITEMS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost:3306/homejobs?charset=utf8mb4"
    
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):   
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_POOL_RECYCLE = 299 
    SQLALCHEMY_POOL_TIMEOUT = 20
    


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
