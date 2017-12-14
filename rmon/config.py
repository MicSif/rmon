'''
rmon config file
'''
import os

class DevConfig:
    '''
    develop envirnment config
    '''
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True

class ProductConfig(DevConfig):
    '''
    product envirnment config
    '''
    DEBUG = False
    #sqlite database file path
    path = os.path.john(os.getcwd(),'rmon.db').replace('\\','/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path
