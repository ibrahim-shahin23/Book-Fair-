import os

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///project1.db')
    DEBUG = False  

class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project1.db'
    DEBUG = True  

class ProductionConfig(BaseConfig):
    DEBUG = False  

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}