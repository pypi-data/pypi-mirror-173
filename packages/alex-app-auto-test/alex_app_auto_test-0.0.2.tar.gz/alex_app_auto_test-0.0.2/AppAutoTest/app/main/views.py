#!/usr/bin/env python
# coding=utf-8
import multiprocessing
from threading import Thread

from flask import render_template, session, request, flash, jsonify, redirect, url_for

from . import main
from .. import db
from ..models import *
from . import task


@main.route('/case', methods=['POST'])
def case():
    request_data = request.get_json()
    case_id = request_data["case_id"]
    case_name = request_data["case_name"]
    steps = request_data["steps"]
    if int(case_id):
        case_name = request_data["case_name"]
        case_obj = Case.query.get(case_id)
        case_obj.case_name = case_name
        for item_step in steps:
            case_step_id = item_step["case_step_id"]
            if int(case_step_id):
                obj_case_step = CaseStep.query.get(case_step_id)
                obj_case_step.case_step_name = item_step["case_step_name"]
                obj_case_step.case_step_method = item_step["case_step_method"]
                obj_case_step.case_step_method_id = item_step["case_step_method_id"]
                obj_case_step.case_step_locatior = item_step["case_step_locatior"]
                obj_case_step.case_step_value = item_step["case_step_value"]
                obj_case_step.case_step_number = item_step["case_step_number"]
                obj_case_step.case_step_assert = item_step["case_step_assert"]
            else:
                case_step_name = item_step["case_step_name"]
                case_step_method_id = item_step["case_step_method_id"]
                case_step_method = item_step["case_step_method"]
                case_step_locatior = item_step["case_step_locatior"]
                case_step_value = item_step["case_step_value"]
                case_step_number = item_step["case_step_number"]
                case_step_assert = item_step["case_step_assert"]

                case_step_obj = CaseStep(case_step_id=case_obj.id, case_step_name=case_step_name,
                                         case_step_method_id=case_step_method_id, case_step_method=case_step_method,
                                         case_step_locatior=case_step_locatior, case_step_number=case_step_number,
                                         case_step_assert=case_step_assert,
                                         case_step_value=case_step_value)
                db.session.add(case_step_obj)
        db.session.commit()
        # return jsonify({"code": "1", "message": "更新成功"})
    else:
        case_obj = Case(case_name=case_name)
        db.session.add(case_obj)
        db.session.flush()
        for item_step in steps:
            case_step_name = item_step["case_step_name"]
            case_step_method = item_step["case_step_method"]
            case_step_method_id = item_step["case_step_method_id"]
            case_step_locatior = item_step["case_step_locatior"]
            case_step_value = item_step["case_step_value"]
            case_step_number = item_step["case_step_number"]
            case_step_assert = item_step["case_step_assert"]
            case_step_obj = CaseStep(case_step_id=case_obj.id, case_step_name=case_step_name,
                                     case_step_method_id=case_step_method_id,
                                     case_step_method=case_step_method,
                                     case_step_locatior=case_step_locatior, case_step_number=case_step_number,
                                     case_step_assert=case_step_assert,
                                     case_step_value=case_step_value)
            db.session.add(case_step_obj)
        db.session.commit()
        # return jsonify({"code": "1", "message": "添加成功"})
    # return redirect(url_for('main.case_list'))
    return jsonify({"code": "1", "message": "添加成功"})


@main.route('/detail/<string:id>', methods=['GET'])
def detail(id):
    case_detail = Case.query.get(id)
    case_detail_dict = {}
    case_detail_dict["case_id"] = case_detail.id
    case_detail_dict["case_name"] = case_detail.case_name
    case_detail_dict["case_status"] = case_detail.case_status
    case_detail_dict["create_time"] = case_detail.create_time
    case_detail_dict["update_time"] = case_detail.update_time
    steps_dict_list = []
    case_steps_set = CaseStep.query.filter_by(case_step_id=case_detail.id).order_by("case_step_number").all()
    for item in case_steps_set:
        steps_dict = {}
        steps_dict["case_step_id"] = item.id
        steps_dict["case_step_number"] = item.case_step_number
        steps_dict["case_step_name"] = item.case_step_name
        steps_dict["case_step_locatior"] = item.case_step_locatior
        steps_dict["case_step_method"] = item.case_step_method
        steps_dict["case_step_method_id"] = item.case_step_method_id
        steps_dict["case_step_value"] = item.case_step_value
        steps_dict["case_step_assert"] = item.case_step_assert
        steps_dict["case_step_status"] = item.case_step_status
        steps_dict["describe"] = item.describe
        steps_dict_list.append(steps_dict)
    case_detail_dict["steps"] = steps_dict_list
    return jsonify(case_detail_dict)


@main.route('/', methods=['GET'])
def case_list():
    case_set = Case.query.all()
    return render_template('index.html', case_list=case_set)


@main.route('/change_status/<string:id>', methods=['PUT'])
def case_chanage_status(id):
    case_obj = Case.query.get(id)
    if case_obj.case_status:
        case_obj.case_status = False
    else:
        case_obj.case_status = True
    db.session.commit()
    return jsonify({"code": "1", "message": "用例状态更新成功"})


@main.route('/change_sort/<string:id>/<string:status>', methods=['PUT'])
def case_case_sort(id, status):
    case_obj = Case.query.get(id)
    if status == "0":
        case_obj.case_sort = "0"
    elif status == "1":
        case_obj.case_sort = "1"
    else:
        case_obj.case_sort = "2"
    db.session.commit()
    return jsonify({"code": "1", "message": "用例状态更新成功"})


@main.route('/method', methods=['GET'])
def method_list():
    method_set = Method.query.all()
    method_list = []
    for item in method_set:
        item_dict = {}
        item_dict["id"] = item.id
        item_dict["method_name"] = item.method_name
        method_list.append(item_dict)
    return jsonify(method_list)


@main.route('/method_list', methods=['GET'])
def method():
    method_set = Method.query.all()
    return render_template("method.html", method_set=method_set)


@main.route('/add_method', methods=['POST'])
def add_method():
    request_json = request.get_json()
    method_name = request_json["method_name"]
    method_rel_function = request_json["method_rel_function"]
    method_obj = Method(method_name=method_name, method_rel_function=method_rel_function)
    db.session.add(method_obj)
    db.session.commit()
    return jsonify({"code": "1", "message": "添加方法成功"})


@main.route('/case/<string:id>', methods=['DELETE'])
def delete_case(id):
    case_obj = Case.query.get(id)
    if case_obj is None:
        return jsonify({"code": "1", "message": "该用例已经删除"})
    case_step_set = case_obj.case_step
    for item_case_step in case_step_set:
        db.session.delete(item_case_step)
    db.session.delete(case_obj)
    db.session.commit()

    return jsonify({"code": "1", "message": "删除成功"})


@main.route('/case_step/<string:id>', methods=['DELETE'])
def delete_case_step(id):
    case_step_obj = CaseStep.query.get(id)
    if case_step_obj is None:
        return jsonify({"code": "1", "message": "该用例步骤已经删除"})

    db.session.delete(case_step_obj)
    db.session.commit()

    return jsonify({"code": "1", "message": "删除成功"})


@main.route('/debug', methods=['POST'])
def debug():
    from flask import current_app
    request_data = request.get_json()
    # p1 = multiprocessing.Process(target=task.debug, args=(request_data,))
    p1 = Thread(target=task.debug, args=(current_app._get_current_object(), request_data,))
    p1.start()
    return jsonify({"code": "1", "message": "调试任务处理中"})


@main.route('/batch', methods=['POST'])
def batch():
    from flask import current_app
    p1 = Thread(target=task.batch, args=(current_app._get_current_object(),))
    p1.start()
    return jsonify({"code": "1", "message": "批量任务处理中"})


@main.route('/batch_list', methods=['GET'])
def batch_list():
    case_set = Case.query.filter_by(case_status=1).all()
    return render_template("batch.html", case_list=case_set)


@main.route('/remove/<string:id>', methods=['DELETE'])
def remove(id):
    case_obj = Case.query.get(id)
    case_obj.case_status = False
    db.session.commit()
    return jsonify({"code": "1", "message": "移除成功"})


@main.route('/report', methods=['GET'])
def report():
    report_set = Report.query.all()
    return render_template("report.html", report_set=report_set)


@main.route('/report_detail/<string:id>', methods=['GET'])
def report_detail(id):
    report_obj = Report.query.get(id)
    report_step_set = report_obj.report_step
    report_dict = {"case_name": report_obj.report_name, "steps": []}
    for item_report_step in report_step_set:
        report_step_dict = {}
        report_step_dict["case_step_name"] = item_report_step.report_step_name
        report_step_dict["describe"] = item_report_step.describe
        report_step_dict[
            "case_step_locatior"] = item_report_step.report_step_locatior if item_report_step.report_step_locatior else "无"
        report_step_dict["case_step_method"] = item_report_step.report_step_method
        report_step_dict[
            "case_step_value"] = item_report_step.report_step_value if item_report_step.report_step_value else "无"
        report_step_dict[
            "case_step_image"] = item_report_step.report_step_image
        report_dict["steps"].append(report_step_dict)
    return jsonify(report_dict)


@main.route('/report/<string:id>', methods=['DELETE'])
def delete_report(id):
    report_obj = Report.query.get(id)
    if report_obj is None:
        return jsonify({"code": "1", "message": "该用例报告已经删除"})
    report_step_set = report_obj.report_step
    for item_report_step in report_step_set:
        db.session.delete(item_report_step)
    db.session.delete(report_obj)
    db.session.commit()

    return jsonify({"code": "1", "message": "报告删除成功"})


@main.before_app_first_request
######stackoverflow真是个牛逼的网站。。这个地方注意了！
def init_database():
    db.create_all()
