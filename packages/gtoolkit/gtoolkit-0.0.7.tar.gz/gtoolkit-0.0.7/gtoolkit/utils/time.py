"""
    一个时间转换工具：
        将 date、datetime、timestamp 转换为任意类型
        获取当前日期的之前一段、后一段日期

    示例：
        print(TimeConverter(date='2022-10-25').to_datetime())
        print(TimeConverter(date_time='2022-10-25 15:49:41.240015').to_date())
        print(TimeConverter(timestamp=1666684181.0).to_day_after(1).to_day_before(1))
"""
import re
import datetime


class TimeConverter:
    def __init__(self, date: str = None, date_time: str = None, timestamp: float = None):
        if date:
            self.time = datetime.datetime.strptime(self.parse_date(date), '%Y-%m-%d')
        elif date_time:
            self.time = datetime.datetime.strptime(self.parse_datetime(date_time), '%Y-%m-%d %H:%M:%S')
        elif timestamp:
            self.time = datetime.datetime.fromtimestamp(self.parse_timestamp(timestamp))
        else:
            raise Exception('未输入待转换数据')

    def to_date(self, pattern: str = None) -> str:
        """
        转换成 date

        :param pattern: 格式化规则
        :return:
        """
        return self.time.strftime(pattern or '%Y-%m-%d')

    def to_datetime(self, pattern: str = None) -> str:
        """
        转换成 date

        :param pattern: 格式化规则
        :return:
        """
        return self.time.strftime(pattern or '%Y-%m-%d  %H:%M:%S')

    def to_timestamp(self) -> float:
        """
        转换为时间戳

        :return:
        """
        return self.time.timestamp()

    def to_day(
            self,
            add: bool = False,
            reduce: bool = False,
            days: int = 0,
            seconds: int = 0,
            microseconds: int = 0,
            milliseconds: int = 0,
            minutes: int = 0,
            hours: int = 0,
            weeks: int = 0
    ):
        """
        获取指定 时间 之前或之后的时间

        :param add: + 操作符
        :param reduce: - 操作符
        :param days:
        :param seconds:
        :param microseconds:
        :param milliseconds:
        :param minutes:
        :param hours:
        :param weeks:
        :return:
        """
        if add:
            self.time += datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
        elif reduce:
            self.time -= datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

        return self

    def to_day_after(self, days: int):
        """
        获取指定天数之后的日期

        :param days: 天数
        :return:
        """
        return self.to_day(add=True, days=days)

    def to_day_before(self, days: int):
        """
        获取指定天数之前的日期

        :param days: 天数
        :return:
        """
        return self.to_day(reduce=True, days=days)

    def get_between(self, date: datetime.datetime) -> datetime.timedelta:
        """
        获取两个日期相差的天数

        :param date:
        :return:
        """

        return self.time - date

    @staticmethod
    def parse_datetime(time: str) -> str:
        """
        解析出时间

        :param time:
        :return:
        """
        result = re.findall(r'\d+', time)

        if len(result) >= 6:
            return f'{result[0]}-{result[1]}-{result[2]} {result[3]}:{result[4]}:{result[5]}'

    @staticmethod
    def parse_date(time: str) -> str:
        """
        解析出时间

        :param time:
        :return:
        """
        result = re.findall(r'\d+', time)

        if len(result) >= 3:
            return f'{result[0]}-{result[1]}-{result[2]}'

    @staticmethod
    def parse_timestamp(time: float) -> float:
        """
        解析出时间

        :param time:
        :return:
        """
        timestamp_str = str(time)

        if '.' in timestamp_str:
            if len(timestamp_str.split('.')[0]) > 10:
                time = time / 1000
        elif len(timestamp_str) > 10:
            time = time / pow(10, (len(timestamp_str) - 10))

        return float(time)

    def __str__(self):
        return self.to_datetime()
