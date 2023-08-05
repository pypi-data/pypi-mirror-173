#!/usr/bin/env python
#coding=utf-8

from flask import render_template
from . import main

@main.errorhandler(404)
def page_not_found(error):
    return render_template('errors_page/404.html'),404

@main.errorhandler(500)
def interval_server_error(error):
    return render_template('errors_page/500.html'),500