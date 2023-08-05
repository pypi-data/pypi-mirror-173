#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lixiaoyang
# Mail: 541121316@163.com
# Created Time:  2022-10-24 10:24:34
#############################################

from setuptools import setup, find_packages

setup(
    name = "alex_app_auto_test",      #这里是pip项目发布的名称
    version = "0.0.5",  #版本号，数值大的会优先被pip
    keywords = ("pip", "alex_app_auto_test"),
    description = "An app auto test",
    long_description = "An app auto test",
    license = "MIT Licence",

    url = "",     #项目相关文件地址，一般是github
    author = "lixiaoyang",
    author_email = "541121316@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["flask","Appium-Python-Client","flask_sqlalchemy","flask_migrate","pyyaml"]          #这个项目需要的第三方库
)