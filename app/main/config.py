import os

from app.main.config_variable import ConfigVariables

root_folder = os.path.split(os.environ['VIRTUAL_ENV'])[0]
env = os.getenv('BOILERPLATE_ENV')
config_variables = ConfigVariables(env, config_file_folder=root_folder)


class Config:
    SECRET_KEY = config_variables.get('secret_key')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(config_variables.get('db_username'),
                                                                   config_variables.get('db_password'),
                                                                   config_variables.get('db_host'),
                                                                   config_variables.get('db_schema'))


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
