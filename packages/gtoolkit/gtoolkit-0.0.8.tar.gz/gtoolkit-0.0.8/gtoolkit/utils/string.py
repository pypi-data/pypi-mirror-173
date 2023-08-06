"""
    字符串工具包
"""
from six import unichr


# 全半角转换
class StrConversion:
    def __init__(self, s: str):
        self.s = s

    def to_half(self):
        """
        全角转半角

        :return:
        """
        s = ""

        for uchar in self.s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            s += unichr(inside_code)

        return s

    def to_full(self):
        """
        半角转全角

        :return:
        """
        s = ""

        for uchar in self.s:
            inside_code = ord(uchar)
            if inside_code == 32:  # 半角空格直接转化
                inside_code = 12288
            elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
                inside_code += 65248

            s += unichr(inside_code)

        return s
