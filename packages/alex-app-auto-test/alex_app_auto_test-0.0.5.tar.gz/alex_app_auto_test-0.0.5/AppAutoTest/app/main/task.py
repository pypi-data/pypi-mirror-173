from autotest.function.android_driver_fun import AndroidDriverFun
from autotest.initialize.initialize import LoadCfg
from ..models import *


def debug(app, case_dict):
    with app.app_context():
        GV = LoadCfg()
        GV.new_driver()
        case_name = case_dict["case_name"]
        steps = case_dict["steps"]
        report_obj = Report(report_name=case_name)
        db.session.add(report_obj)
        db.session.flush()
        try:
            for item_step in steps:
                GV.IMAGE_URL = None
                GV.STEP_START_TIME = GV.new_time()
                case_step_number = item_step["case_step_number"]
                case_step_locatior = item_step["case_step_locatior"]
                case_step_name = item_step["case_step_name"]
                case_step_method_id = item_step["case_step_method_id"]
                case_step_method = item_step["case_step_method"]
                method_obj = Method.query.get(case_step_method_id)
                method_rel_function = method_obj.method_rel_function
                case_step_value = item_step["case_step_value"]
                describe = "步骤执行成功"
                try:
                    job(GV, method_rel_function, case_step_locatior, case_step_value)
                except Exception as e:
                    print("%s执行失败,原因：%s" % (case_step_name, str(e)))
                    describe = str(e)
                    report_obj.report_status = False
                    break

                finally:
                    if GV.IMAGE_URL is not None:
                        report_step_image = "static"+GV.IMAGE_URL.split("static")[1]
                    else:
                        report_step_image = None
                    report_step_obj = ReportStep(report_step_id=report_obj.id,
                                                 report_step_name="【步骤%s】%s" % (case_step_number, case_step_name),
                                                 report_step_locatior=case_step_locatior,
                                                 report_step_method=case_step_method,
                                                 report_step_value=case_step_value,
                                                 report_step_image=report_step_image,
                                                 describe=describe
                                                 )
                    db.session.add(report_step_obj)
        finally:
            db.session.commit()
            GV.DRIVER.quit()
            print("%s调试任务执行完成" % case_name)


def batch(app):
    with app.app_context():
        GV = LoadCfg()
        case_set = []
        case_set_1 = Case.query.filter_by(case_status=True, case_sort="1").first()
        case_set_0 = Case.query.filter_by(case_status=True, case_sort="0").all()
        case_set_2 = Case.query.filter_by(case_status=True, case_sort="2").first()
        case_set.append(case_set_1)
        case_set.extend(case_set_0)
        case_set.append(case_set_2)


        for item_case in case_set:
            GV.new_driver()
            steps = item_case.case_step
            report_obj = Report(report_name=item_case.case_name)
            db.session.add(report_obj)
            db.session.flush()
            try:
                for item_step in steps:
                    GV.IMAGE_URL = None
                    GV.STEP_START_TIME = GV.new_time()

                    case_step_number = item_step.case_step_number
                    case_step_locatior = item_step.case_step_locatior
                    case_step_name = item_step.case_step_name
                    case_step_method_id = item_step.case_step_method_id
                    case_step_method = item_step.case_step_method
                    method_obj = Method.query.get(case_step_method_id)
                    method_rel_function = method_obj.method_rel_function
                    case_step_value = item_step.case_step_value
                    describe = "步骤执行成功"
                    try:
                        job(GV, method_rel_function, case_step_locatior, case_step_value)
                        print("*******%s执行成功" % case_step_name)
                    except Exception as e:
                        print("*******%s执行失败,原因：%s" % (case_step_name, str(e)))
                        describe = str(e)

                        report_obj.report_status = False
                        break
                    finally:
                        if GV.IMAGE_URL is not None:
                            report_step_image = "static"+GV.IMAGE_URL.split("static")[1]
                        else:
                            report_step_image = None
                        report_step_obj = ReportStep(report_step_id=report_obj.id,
                                                     report_step_name="【步骤%s】%s" % (case_step_number, case_step_name),
                                                     report_step_locatior=case_step_locatior,
                                                     report_step_method=case_step_method,
                                                     report_step_value=case_step_value,
                                                     report_step_image=report_step_image,
                                                     describe=describe
                                                     )
                        db.session.add(report_step_obj)
            finally:
                db.session.commit()
                GV.DRIVER.quit()
            print("##%s执行完成" % item_case.case_name)
        print("批量执行完成")


def job(GV, case_step_method, case_step_locatior, case_step_value):
    adf = AndroidDriverFun(GV)
    if hasattr(adf, case_step_method):
        fun = getattr(adf, case_step_method)
        fun(case_step_locatior, case_step_value)
