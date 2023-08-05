from appium.webdriver.common.appiumby import AppiumBy


class FuncUtils():
    def __init__(self, GV):
        self.GV = GV

    def get_locatior(self, locatior_str):
        """

        :param locatior_str: home_page#iv_avatar#id
        :return:
        """

        try:
            locator_li = locatior_str.split("#")
            page = locator_li[0]
            ele_name = locator_li[1]
            by = locator_li[2]
        except:
            raise Exception("定位数据需要用#号分割")
        try:
            ele_locatior = self.GV.YAML_DATA[page][ele_name][by]
        except:
            raise Exception("未找到%s的定位数据" % locatior_str)

        by = str.upper(by)
        if by == "ID":
            str_by = AppiumBy.ID
        elif by == "XPATH":
            str_by = AppiumBy.XPATH
        elif by == "CLASS_NAME":
            str_by = AppiumBy.CLASS_NAME
        elif by == "LINK_TEXT":
            str_by = AppiumBy.LINK_TEXT
        elif by == "PARTIAL_LINK_TEXT":
            str_by = AppiumBy.PARTIAL_LINK_TEXT
        elif by == "NAME":
            str_by = AppiumBy.NAME
        elif by == "TAG_NAME":
            str_by = AppiumBy.TAG_NAME
        elif by == "CSS_SELECTOR":
            str_by = AppiumBy.CSS_SELECTOR
        else:
            raise Exception("输入的 %s 未在程序中被定义" % by)
        return str_by, ele_locatior
