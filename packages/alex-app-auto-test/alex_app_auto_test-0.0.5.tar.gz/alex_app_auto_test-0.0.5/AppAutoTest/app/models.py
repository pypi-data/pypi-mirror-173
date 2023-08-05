#!/usr/bin/env python
# coding=utf-8
import datetime

from . import db


class Method(db.Model):
    __tablename__ = 'tb_method'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    method_name = db.Column(db.String(200), nullable=True)
    method_rel_function = db.Column(db.String(200), nullable=True, unique=True)
    method_status = db.Column(db.Boolean, default=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    describe = db.Column(db.Text, nullable=True)


class Case(db.Model):
    __tablename__ = 'tb_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(200), nullable=True)
    case_status = db.Column(db.Boolean, default=True, nullable=True)
    case_sort = db.Column(db.Enum("0", "1", "2"), default="0", nullable=True)
    case_sort_number = db.Column(db.SmallInteger, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    describe = db.Column(db.Text, nullable=True)
    case_step = db.relationship("CaseStep", backref="rel_case_step")


class CaseStep(db.Model):
    __tablename__ = 'tb_case_step'
    id = db.Column(db.Integer, primary_key=True)
    case_step_id = db.Column(db.Integer, db.ForeignKey('tb_case.id'))
    case_step_number = db.Column(db.SmallInteger, nullable=True)
    case_step_name = db.Column(db.String(200), nullable=True)
    case_step_locatior = db.Column(db.String(500), nullable=True)
    case_step_method = db.Column(db.String(200), nullable=True)
    case_step_method_id = db.Column(db.SmallInteger, nullable=True)
    case_step_value = db.Column(db.String(200), nullable=True)
    case_step_assert = db.Column(db.String(200), nullable=True)
    case_step_status = db.Column(db.Boolean, default=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    describe = db.Column(db.Text, nullable=True)


class Report(db.Model):
    __tablename__ = 'tb_report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_name = db.Column(db.String(200), nullable=True)
    report_status = db.Column(db.Boolean, default=True, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    describe = db.Column(db.Text, nullable=True)
    report_step = db.relationship("ReportStep", backref="rel_report_step")


class ReportStep(db.Model):
    __tablename__ = 'tb_report_step'
    id = db.Column(db.Integer, primary_key=True)
    report_step_id = db.Column(db.Integer, db.ForeignKey('tb_report.id'))
    report_step_name = db.Column(db.String(200), nullable=True)
    report_step_locatior = db.Column(db.String(500), nullable=True)
    report_step_method = db.Column(db.String(200), nullable=True)
    report_step_value = db.Column(db.String(200), nullable=True)
    report_step_status = db.Column(db.Boolean, default=True, nullable=True)
    report_step_image = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    describe = db.Column(db.Text, nullable=True)
