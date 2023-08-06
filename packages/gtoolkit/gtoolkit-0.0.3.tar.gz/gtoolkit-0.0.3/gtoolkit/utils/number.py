"""
    BinaryConversion：处理进制转换
    to_fixed：保留小数点后 n 位

    示例：
        print(BinaryConversion(0x18, keep_prefix=True).all)
        print(BinaryConversion(0b11000).hex)
        print(BinaryConversion(0o30).hex)
        print(BinaryConversion(24).hex)

        print(to_fixed(3.1415936, 5))
"""
from typing import Union


class BinaryConversion:
    def __init__(self, num, keep_prefix: bool = False):
        """

        :param num:
        :param keep_prefix: 是否保留进制的前缀
        """
        num = str(num)
        self.keep_prefix = keep_prefix

        if num.lower().startswith('0b'):
            self._num = int(num, 2)
        elif num.lower().startswith('0o'):
            self._num = int(num, 8)
        elif num.lower().startswith('0x'):
            self._num = int(num, 16)
        else:
            self._num = int(num)

    @property
    def hex(self) -> Union[int, str]:
        """
        转换为十六进制
        """
        result = hex(self._num)

        if self.keep_prefix:
            return result
        else:
            return int(result.lstrip('0x'))

    @property
    def dec(self) -> int:
        """
        转换为十进制
        """

        return self._num

    @property
    def oct(self) -> Union[int, str]:
        """
        转换为八进制
        """

        result = oct(self._num)

        if self.keep_prefix:
            return result
        else:
            return int(result.lstrip('0o'))

    @property
    def bin(self) -> Union[int, str]:
        """
        转换为二进制
        """

        result = bin(self._num)

        if self.keep_prefix:
            return result
        else:
            return int(result.lstrip('0b'))

    @property
    def all(self) -> dict:
        """
        转换为各种进制进制
        """

        return {
            'hex': self.hex,
            'dec': self.dec,
            'oct': self.oct,
            'bin': self.bin,
        }


def to_fixed(num: float, n: int) -> float:
    """
    保留小数点后 n 位

    :param num: 输入字符
    :param n: 小数点后 n 位
    :return:
    """
    if isinstance(num, str) or isinstance(num, int):
        num = float(num)

    return float(format(num, f'.{n}f'))
