import json
from pathlib import Path
from typing import Union

from PIL import Image


class FileType:
    """
    文件类型
    """
    PICTURE = ("png", "jpg", "gif", "bmp", "jpeg", "webp")
    AUDIO = ("mp3", "wma", "wav", "amr", "aac", "flac", "ape", "ogg", "m4a", "opus", "aac")
    VIDEO = ("mp4", "mkv", "avi", "wmv", "rm", "rmvb", "flv", "mpeg", "mpg", "mpe", "mov", "3gp", "webm", "ts")
    DOCUMENT = ("doc", "ppt", "xls", "docx", "pptx", "xlsx", "txt", "pdf", "epub", "md", "rtf", "mobi")
    CODE = ("py", "java", "c", "cpp", "js", "html", "css", "json", "xml", "sql")
    ARCHIVE = ("zip", "rar", "7z", "img", "iso", "gz", "bz2", "tar")
    NT = ("exe", "bat", "msi")
    LINUX = ("sh", "deb", "rpm")
    GAME = ("esp", "esl", "fomod", "slot")

    @classmethod
    def file_dict(cls):
        """
        获取文件类型字典
        Returns:

        """
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_') and "method" not in str(v)}

    @classmethod
    def file_types(cls, lower=True) -> list[str]:
        """
        获取所有文件类型名称
        Args:
            lower: 以小写形式返回

        Returns:

        """
        types = list(cls.file_dict().keys())
        return types if not lower else [t.lower() for t in types]

    @classmethod
    def file_suffixes(cls, file_type: str, path_use: bool = False) -> list[str]:
        """
        获得指定文件类型的后缀
        Args:
            file_type: 指定文件类型
            path_use: 用于Path类的判断

        Returns: 该文件类型注册的后缀

        """
        suffixes = getattr(cls, file_type.upper())
        return [f".{s}" for s in suffixes] if path_use else suffixes


"""
其它常用工具类
"""


class NumCalc:
    """
    数值计算工具类
    """

    @staticmethod
    def hex_format(num: Union[str, int]):
        """
        十六进制格式化
        :param num:
        :return:
        """
        if isinstance(num, int):
            num = hex(num)
        elif isinstance(num, str):
            num = num.lower()
            if not num.startswith("0x"):
                num = f"0x{num}"
            return num
        else:
            raise Exception("type error")
        return num

    @classmethod
    def hex_add(cls, base, offset):
        """
        16进制加法
        Args:
            base:
            offset:

        Returns:

        """
        return hex(eval(base) + eval(offset))


class UnitConverter:
    """
    单位转换工具类
    """

    @staticmethod
    def time2sec(time_str):
        """
        时间转换为秒
        :param time_str:
        :return:
        """
        return sum(x * int(t) for x, t in zip([3600, 60, 1], time_str.split(":")))


class Media:
    """
    媒体工具箱
    """

    @classmethod
    def is_picture(cls, path):
        """
        判断文件是否是图片
        Args:
            path:

        Returns:

        """
        path = Path(path)
        return path.is_file() and path.name.endswith(FileType.PICTURE)

    @staticmethod
    def get_image_resolution(image_path):
        """
        获得图片分辨率
        Args:
            image_path:

        Returns:

        """
        with Image.open(image_path) as img:
            width, height = img.size
        return width, height

    @classmethod
    def is_vertical_picture(cls, image_path):
        """
        判断图片是否是纵向图片(高大于宽)
        Args:
            image_path:

        Returns:

        """
        width, height = cls.get_image_resolution(image_path)
        return height > width

    @classmethod
    def is_horizontal_picture(cls, image_path):
        """
        判断图片是否是横向图片(宽大于高)
        Args:
            image_path:

        Returns:

        """
        width, height = cls.get_image_resolution(image_path)
        return width > height

    @classmethod
    def get_image_orient(cls, image_path):
        """
        判断图片方向
        Args:
            image_path:

        Returns: -1: horizontal, 1: vertical, 0: square

        """
        width, height = cls.get_image_resolution(image_path)
        diff = width - height
        if diff > 0:
            return -1
        elif diff < 0:
            return 1
        else:
            return 0


class FileParser:
    space = " " * 2

    @staticmethod
    def try_loads(str_like):
        try:
            data = json.loads(str_like)
            assert isinstance(data, dict)
        except:
            return None
        print(f"data: {data}")
        return data

    @classmethod
    def expand_dict(cls, src_dict, level=0):
        """
        json里面v是字典、字典列表、字符串、字典字符串
        Args:
            src_dict:
            level: 展开层级

        Returns:

        """
        for k, v in src_dict.items():
            k_phrase = f"{cls.space * level}{k}:"
            kv_phrase = f"{cls.space * level}{k}: {v}"
            # 递归终止条件之一: 数字
            if isinstance(v, (int, float)):
                print(kv_phrase)
            # 嵌套字典
            elif isinstance(v, dict):
                print(k_phrase)
                cls.expand_dict(v, level + 1)
            # 列表：字符串列表、数字列表、字典列表、列表列表
            elif isinstance(v, list):
                print(k_phrase)
                for ele in v:
                    cls.expand_dict(ele, level + 1)
            # 字符串
            elif isinstance(v, str):
                # 字典字符串、列表字符串等集合类型
                if v.startswith(("[", "{")):
                    pass
                else:
                    # 递归终止条件之二: 字符串、数字字符串
                    print(kv_phrase)
                    continue
                try:
                    # 数字、数字列表、字典、字典列表可以转换，其他比如字符串、字符串列表报错
                    data = json.loads(v)
                    # 数字列表、字典列表、字典
                    if isinstance(data, (dict, list, str)):
                        print(k_phrase)
                        cls.expand_dict(data, level + 1)
                    else:
                        # 数字
                        print(kv_phrase)
                except Exception as e:
                    # 字符串、字符串列表
                    print(f"error: {e}, {k}={v}, {type(v)}")
                    print(kv_phrase)

            else:
                raise Exception(f"Unknown type: {k}->{type(k)}, {v}->{type(v)}")

    @classmethod
    def get_label_from_json(cls, json_file, label):
        with open(json_file, "r") as f:
            data = json.load(f)
        cls.expand_dict(data)


if __name__ == '__main__':
    FileParser.get_label_from_json(r"D:\WorkShop\Python\DesktopUtils\Windows\Placement.json", 1)
