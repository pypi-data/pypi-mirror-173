import os
import time

import allure
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from autotest.function.common import FuncUtils


class AndroidDriverFun():
    def __init__(self, GV):

        self.GV = GV
        self.uls = FuncUtils(GV)
        self.driver = GV.DRIVER
        self.wait_time = 10

    def wait_element(func):
        def wrapper(self, *args, **kwargs):
            self.STEP_START_TIME = time.strftime('%Y%m%d%H%M%s', time.localtime(time.time()))
            try:
                by, locatior = self.uls.get_locatior(args[0])
                WebDriverWait(self.driver, self.wait_time).until(
                    expected_conditions.presence_of_element_located((by, locatior)))
            except TimeoutException as e:  ##未找到元素时截图
                ##检查是否有弹窗

                ##截图
                self.screenshot("", "")
                raise Exception("未找到定位元素")

                # ##把截图添加到allure中
                # self.allure_add_image(locatior, "")
            func(self, *args, **kwargs)

        return wrapper

    ##点击元素
    @wait_element
    def click(self, by_element, str_value):
        by, locatior = self.uls.get_locatior(by_element)
        by_element.split()
        ele = self.driver.find_element(by, locatior)
        ##判断元素是否可以点击
        WebDriverWait(self.driver, self.wait_time).until(expected_conditions.element_to_be_clickable((by, locatior)))
        ele.click()

    ##点击元素
    @wait_element
    def click_index(self, by_element, index):
        by, locatior = self.uls.get_locatior(by_element)
        by_element.split()
        ele = self.driver.find_elements(by, locatior)
        ele_index = ele[int(index)]
        ##判断元素是否可以点击
        WebDriverWait(self.driver, self.wait_time).until(expected_conditions.element_to_be_clickable((by, locatior)))
        ele_index.click()

    ##输入框输入数据
    @wait_element
    def send_keys(self, by_element, str_value):
        by, locatior = self.uls.get_locatior(by_element)
        ele = self.driver.find_element(by, locatior)
        ele.send_keys(str_value)

    ##点击输入框然后输入数据
    @wait_element
    def click_send_keys(self, by_element, str_value):
        by, locatior = self.uls.get_locatior(by_element)
        ele = self.driver.find_element(by, locatior)
        ele.click()
        ele.send_keys(str_value)

    ##判断元素是否存在，用于断言
    @wait_element
    def assert_exist(self, by_element, str_value):
        pass

    ##判断元素不存在
    def assert_not_exist(self, by_element, str_value):
        by, locatior = self.uls.get_locatior(by_element)
        try:
            WebDriverWait(self.driver, self.wait_time).until(
                expected_conditions.presence_of_element_located((by, locatior)),
                "未定位到%s元素" % locatior)
            assert False, "%s元素存在" % locatior
        except:
            pass

    ##点击输入框然后输入数据
    @wait_element
    def assert_text(self, by_element, str_value):
        by, locatior = self.uls.get_locatior(by_element)
        ele = self.driver.find_element(by, locatior)
        actual_result = ele.text
        if actual_result == str_value:
            pass
        else:
            self.screenshot("", "")
            # self.allure_add_image(locatior, "", "")
            assert False, "定位%s的内容预期是%s，实际是%s" % (locatior, str_value, actual_result)

    ##截图
    def screenshot(self, by_element, str_value):
        img_folder = self.GV.SCREENSHOTS_DIR
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        screen_save_path = img_folder + self.GV.STEP_START_TIME + '.png'
        self.driver.get_screenshot_as_file(screen_save_path)
        self.GV.IMAGE_URL = screen_save_path

    ##截图添加到allure中
    def allure_add_image(self, locatior, str_value):
        image_path = self.GV.SCREENSHOTS_DIR + self.GV.STEP_START_TIME + ".png"
        with open(image_path, mode='rb') as f:
            image_file = f.read()
        allure.attach(image_file, '未定位到【%s】元素' % locatior, allure.attachment_type.PNG)

    ##关闭手机键盘
    def hide_keyboard(self, locatior, str_value):
        self.driver.hide_keyboard()

    def get_size(self, locatior, str_value):
        # 获取屏幕尺寸
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y  # 向左滑动

    ##向上滑动
    def swipe_up(self, locatior, str_value):
        l = self.get_size(locatior, str_value)
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.7)
        y2 = int(l[1] * 0.4)
        self.driver.swipe(x1, y1, x1, y2, 1000)

    ##向下滑动
    def swipe_down(self, locatior, str_value):
        l = self.get_size(locatior, str_value)
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.35)
        y2 = int(l[1] * 0.85)
        self.driver.swipe(x1, y1, x1, y2, 1000)

    ##向左滑动
    def swipe_left(self, locatior, str_value):
        l = self.get_size(locatior, str_value)
        x1 = int(l[0] * 0.95)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.25)
        self.driver.swipe(x1, y1, x2, y1, 1000)

    ##向右滑动
    def swipe_right(self, locatior, str_value):
        l = self.get_size(locatior, str_value)
        y1 = int(l[1] * 0.5)
        x1 = int(l[0] * 0.25)
        x2 = int(l[0] * 0.95)
        self.driver.swipe(x1, y1, x2, y1, 1000)
