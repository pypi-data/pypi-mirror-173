import time

from appium import webdriver
from autotest.common.utils import Utils
from root_dir import root_dir

uls = Utils()


class LoadCfg():
    def __init__(self):
        basedir = root_dir + "/app"
        config_data = uls.parse_yaml(0)
        self.PLATFORM = config_data["platform"]
        self.WAIT_ELEMENT_TIME = config_data["wait_element_time"]
        self.SCREENSHOTS_DIR = basedir + config_data["screenshot_dir"]
        self.DRIVER_FOR_EVER = config_data["driver_for_ever"]

        if self.PLATFORM == 1:  ##安卓
            self.CONFIG_DATA = config_data["Android"]
            self.YAML_DATA = uls.parse_yaml(1)
        elif self.PLATFORM == 2:  ##IOS
            self.CONFIG_DATA = config_data["IOS"]
            self.YAML_DATA = uls.parse_yaml(2)

        if self.DRIVER_FOR_EVER:
            self.new_driver()
        else:
            self.DRIVER = None

        self.STEP_START_TIME = self.new_time()
        self.IMAGE_URL = None

    def new_time(self):
        return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))

    def new_driver(self):
        caps = {}
        if self.PLATFORM == 1:  ##安卓
            caps["platformName"] = self.CONFIG_DATA["platformName"]
            caps["appium:platformVersion"] = self.CONFIG_DATA["platformVersion"]
            caps["appium:deviceName"] = self.CONFIG_DATA["deviceName"]
            caps["appium:appPackage"] = self.CONFIG_DATA["appPackage"]
            caps["appium:appActivity"] = self.CONFIG_DATA["appActivity"]
            caps["appium:app"] = self.CONFIG_DATA["app"]
            caps["appium:noReset"] = self.CONFIG_DATA["noReset"]
            caps["appium:newCommandTimeout"] = self.CONFIG_DATA["newCommandTimeout"]
            caps["appium:ensureWebviewsHavePages"] = self.CONFIG_DATA["ensureWebviewsHavePages"]
            caps["appium:nativeWebScreenshot"] = self.CONFIG_DATA["nativeWebScreenshot"]
            caps["appium:connectHardwareKeyboard"] = self.CONFIG_DATA["connectHardwareKeyboard"]
        elif self.PLATFORM == 2:  ##IOS
            caps["platformName"] = self.CONFIG_DATA["platformName"]
            caps["appium:platformVersion"] = self.CONFIG_DATA["platformVersion"]
            caps["appium:deviceName"] = self.CONFIG_DATA["deviceName"]
            caps["appium:app"] = self.CONFIG_DATA["app"]
            caps["appium:udid"] = self.CONFIG_DATA["udid"]
            caps["appium:noReset"] = self.CONFIG_DATA["noReset"]
            caps["appium:newCommandTimeout"] = self.CONFIG_DATA["newCommandTimeout"]
        self.DRIVER = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
