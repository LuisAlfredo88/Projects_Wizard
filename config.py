from os import path

class Config(object):
    SERVER_NAME = 'localhost:8080'
    DEBUG = False
    TESTING = False
    BASE_DIR = path.abspath(path.dirname(__file__))

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DB_CONFIG = {
        'PROTOCOL': 'mysql+pymysql',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASS': '',
        'DB': 'acl_gestor'
    }
    DATABASE_URI = "{PROTOCOL}://{USER}:{PASS}@{HOST}/{DB}?charset=utf8".format(**DB_CONFIG)
    DEBUG = True

class TestingConfig(Config):
    TESTING = True