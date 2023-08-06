"""
    返回带有解析器功能的 Response

    示例：
        resp = Parser(requests.xxx())
        resp.xpath().extract()
        resp.css()
        resp.re()
        resp.re_first()
"""
import re
from parsel import Selector
from requests.models import Response


class ResponseParser(Response):
    def __init__(self, resp: Response):
        """

        :param resp: requests 返回的响应
        """
        super().__init__()
        self._resp = resp
        self._resp.encoding = resp.apparent_encoding
        self._selector = Selector(self._resp.text)

        self.__dict__.update(self._resp.__dict__)  # 把 request Response 对象的数据转移过来

    def xpath(self, query: str, namespaces: str = None, **kwargs):
        """
        实现 xpath 选择器功能

        :param query: 匹配规则
        :param namespaces: 命名空间
        :param kwargs:
        :return:
        """
        return self._selector.xpath(query=query, namespaces=namespaces, **kwargs)

    def css(self, query: str):
        """
        实现 css 选择器功能

        :param query: 匹配规则
        :return:
        """
        return self._selector.css(query=query)

    def re(self, pattern: str, flags=0) -> list:
        """
        常用 flags：
            re.I：忽略字母大小写
            re.A：匹配相应的 ASCII 字符类别

        :param pattern: 匹配规则
        :param flags: 修饰符
        :return:
        """
        return re.findall(pattern, self.text, flags=flags)

    def re_first(self, pattern: str, flags=0) -> str:
        """
        常用 flags：
            re.I：忽略字母大小写
            re.A：匹配相应的 ASCII 字符类别

        :param pattern: 匹配规则
        :param flags: 修饰符
        :return:
        """
        result = self.re(pattern=pattern, flags=flags)
        if result:
            return result[0]
