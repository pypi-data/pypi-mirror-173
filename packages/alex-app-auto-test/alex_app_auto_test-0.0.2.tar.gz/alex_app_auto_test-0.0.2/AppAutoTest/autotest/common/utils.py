import os

import yaml


class Utils():
    def parse_yaml(self, type=0):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if type == 0:  ##配置文件
            file_path = path + "/config/config.yaml"
        elif type == 1:  ##安卓定位数据
            file_path = path + "/data/android_locatior.yaml"
        elif type == 2:  ##IOS定位数据
            file_path = path + "/data/ios_locatior.yaml"
        else:
            raise Exception("目前只有配置文件，安卓定位数据文件，IOS定位数据文件")

        with open(file_path, encoding='utf8') as a_yaml_file:
            parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
            return parsed_yaml_file


if __name__ == "__main__":
    uls = Utils()
    print(uls.parse_yaml(0))
