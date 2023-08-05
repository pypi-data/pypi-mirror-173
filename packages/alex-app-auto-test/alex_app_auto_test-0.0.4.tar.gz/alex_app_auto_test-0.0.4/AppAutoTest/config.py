#!/usr/bin/env python
#coding=utf-8
import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'franknihao'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):

    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/instance/app_auto_test.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app_auto_test.db'

config = {
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}
