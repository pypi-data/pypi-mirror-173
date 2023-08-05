# This sample code uses the Appium python client v2
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait






def wait_element(driver, time, element_by, element, msg):
    """
    等待元素出现
    :param driver: driver
    :param time: 等待时间
    :param element_by: 元素类型
    :param element: 元素关键字
    :param msg: 输出信息
    :return:
    """
    WebDriverWait(driver, time).until(expected_conditions.presence_of_element_located((element_by, element)), msg)




caps = {}
caps["platformName"] = "Android"
caps["appium:platformVersion"] = "10"
caps["appium:deviceName"] = "CLB0218806002550"
caps["appium:appPackage"] = "com.aax.exchange.beta"
caps["appium:appActivity"] = "com.aax.exchange.activity.MainActivity"
caps["appium:app"] = "/Users/Alex/Documents/apk/Exchange.apk"
caps["appium:noReset"] = True
caps["appium:newCommandTimeout"] = "6000"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
# AndoridDriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

# driver.add_cookie({'name': 'authorization', 'value': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBVE9NSU5UTCIsInVpZCI6Njc3MTQwLCJpYXQiOjE2NjUzNzA5MDUsImV4cCI6MTY2NTQ1NzMwNX0.YYR0gWQsrJclOtT7ShKQPZ9SHrUOdcQfgSvkJG2lw77Ln2hYodxDfBqGZ3r7u1zDVOjp4b6urW-fcO4_zOxxvBXJ7IbmOWHRJPtGuwmsu8MwXbFupLPsSOKwCINt-j1tT5rtIK-pD1lx8d04gLdqc6C0-bzz-1OTjZVzTPZJ8YK3HsKvM2ErqNK_3hC_HQFP2HFEjXuORN0vD3fmzApjEdmdhebbOHPJGHVD_aJiMLvw2l6vICPX9fLhRuuqvpDnb7oCSC18AESEObLgh-mmIxKMg_frerAanbkxQbGET1QCItE-sB67lQKXYJ5vzz4mIFjutoMHdC_ZpmxAbU44Lg'})

# aaa = driver.find_element(AppiumBy.ID,"com.aax.exchange.beta:id/ll_search")
# aaa.click()
# time.sleep(5)
# bbb = driver.find_element(AppiumBy.ID,"com.aax.exchange.beta:id/et_search_key")
# print(bbb.text)
#
# time.sleep(3)
#
# bbb.send_keys("ddd")

# ##立即登陆
# ele_login_up = driver.find_elements(AppiumBy.ID,"com.aax.exchange.beta:id/ll_login")
# ele_login = ele_login_up[0].find_elements(AppiumBy.CLASS_NAME,"android.widget.TextView")
# ele_login[1].click()

##头像登陆
ele_iv_avatar = driver.find_element(AppiumBy.ID, "com.aax.exchange.beta:id/iv_avatar")
ele_iv_avatar.click()
##登陆/注册
wait_element(driver, 10, AppiumBy.ID, "com.aax.exchange.beta:id/tv_login", "登陆/注册页面，没出现")
ele_tv_login = driver.find_element(AppiumBy.ID, "com.aax.exchange.beta:id/tv_login")
ele_tv_login.click()
##请登陆账户
wait_element(driver, 10, AppiumBy.ID, "com.aax.exchange.beta:id/et_email", "请登陆页账户页面，邮箱控件没有显示完全")
ele_et_email = driver.find_element(AppiumBy.ID, "com.aax.exchange.beta:id/et_email")
ele_et_pwd = driver.find_element(AppiumBy.ID, "com.aax.exchange.beta:id/et_pwd")
tv_next = driver.find_element(AppiumBy.ID, "com.aax.exchange.beta:id/tv_next")
ele_et_email.send_keys("alex_uat_042301@test.com")
ele_et_pwd.send_keys("q1111111")
tv_next.click()
##验证码
wait_element(driver, 10, AppiumBy.ID, "com.aax.exchange.beta:id/et_code", "验证码界面")
ele_et_code = driver.find_element(AppiumBy.ID,"com.aax.exchange.beta:id/et_code")
ele_et_code.click()
ele_et_code.send_keys("987654")
time.sleep(2)
wait_element(driver, 10, AppiumBy.ID, "com.aax.exchange.beta:id/tv_uid", "显示uid")
ele_tv_uid = driver.find_element(AppiumBy.ID,"com.aax.exchange.beta:id/tv_uid")
time.sleep(2)
# driver.quit()
