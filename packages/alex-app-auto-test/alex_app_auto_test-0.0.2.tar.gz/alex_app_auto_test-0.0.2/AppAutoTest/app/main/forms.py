#!/usr/bin/env python
#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,HiddenField,IntegerField,SelectField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,NumberRange,Email

class InfoForm(FlaskForm):
    id = HiddenField(u'id')
    name = StringField(u'姓名',validators=[DataRequired()])
    age = IntegerField(u'年龄',validators=[DataRequired(),NumberRange(min=0,max=99,message=u'年龄必须在%(min)s和%(max)s之间')])
    gender = SelectField(u'性别',choices=[('0',u'男'),('1',u'女')],validators=[DataRequired()])
    mailAdd = StringField(u'邮箱地址',validators=[Email(message=u'邮箱格式不对哦')])
    note = TextAreaField(u'备注')
    submit = SubmitField(u'提交')
