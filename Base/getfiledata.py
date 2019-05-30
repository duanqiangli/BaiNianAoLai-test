import yaml, os


class GetFileData:

    def __init__(self):
        pass

    def get_yaml_data(self, name):
        """
        返回yaml文件数据
        :param name: 读取yaml文件数据
        :return:
        """
        # 拼接文件路径
        file_path = os.getcwd() + os.sep + "Data" + os.sep + name
        # 读取文件数据
        with open(file_path, "r",encoding="utf-8") as f:
            return yaml.safe_load(f)
