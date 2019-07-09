import os, sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# WIN = sys.platform.startswith('win')
# if WIN:  # 如果是 Windows 系统，使用三个斜线
#     prefix = 'sqlite:///'
# else:  # 否则使用四个斜线
#     prefix = 'sqlite:////'

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'f2e232sfewD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:q1889233@localhost/assignor?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass
    # TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    # WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}