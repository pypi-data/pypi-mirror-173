"""
    SQL 连接类

    官网及文档：https://www.sqlalchemy.org/
    连接池文档：https://www.osgeo.cn/sqlalchemy/core/pooling.html

    示例：
        engine = SQLAlchemyEngineBase(drivername='mysql+pymysql', host='localhost', port=3306, user='root', pwd='1234', db='test')

    注意：
        默认就是 QueuePool
"""
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session


class SQLAlchemyEngineBase:
    def __init__(self, drivername: str, host: str, port: int, user: str, pwd: str, db: str, **kwargs):
        """

        :param drivername: 连接方式如：mysql 的 mysql+pymysql
        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """

        # 创建连接 url
        self.conn_url = URL.create(
            drivername=drivername,
            username=user,
            password=pwd,
            host=host,
            port=port,
            database=db
        )

        # 更新默认配置
        config_default = {
            'pool_size': 5,  # 连接池大小
            'pool_pre_ping': True,  # 检查连接状态
            'pool_recycle': 3600,  # 连接回收时间 s，-1 为不启用
            'max_overflow': 10,  # 允许连接池溢出的最大数量
        }
        config_default.update(kwargs)

        # 创建 engine
        self.engine = create_engine(self.conn_url, **config_default)  # 创建连接

    @property
    def session(self) -> Session:
        """
        获取执行的 session

        :return:
        """
        return Session(self.engine)
