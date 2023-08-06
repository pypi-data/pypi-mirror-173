"""
    SQL 方法类

    示例：
        engine = MysqlSQLAlchemyEngine(host='localhost', port=3306, user='root', pwd='1234', db='test')

        method = MysqlSQLAlchemyMethods(engine=engine)

        method.reverse_table_model(path='./modules.py', tables=[])
        res = method.execute(sql='select * from user', fetchone=True, back_dict=True)

    注意：
        这里使用了事务
            with Session(self.engine.db_engine) as session, session.begin():
                session 会自动关闭
                session.begin 可以自动捕获错误，自动回滚，自动提交
"""
import os
from typing import List
from pathlib import Path
from sqlalchemy.orm import declarative_base
from gtoolkit.db.orm.sqlalchemy.exception import SuffixError
from gtoolkit.db.orm.sqlalchemy.engine import SQLAlchemyEngineBase

Base = declarative_base()


# 方法执行类
class SQLAlchemyMethodsBase:
    def __init__(self, engine: SQLAlchemyEngineBase):
        self.engine = engine

    def reverse_table_model(self, path: str, tables: List[str] = None):
        """
        逆向表模型

        注意：pip install sqlacodegen

        :param path: 最终生成的 models.py 文件路径
        :param tables: 需要逆向的表，默认是所有表
        :return:
        """
        if Path(path).suffix != '.py':
            raise SuffixError(f'请输入文件路径，而非文件夹路径，输入：{path}')

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        conn_url = self.engine.conn_url.render_as_string(hide_password=False)  # 将 url 类转换为 url 字符串

        if tables:
            os.system(f"sqlacodegen {conn_url} > {path} --tables {','.join(tables)}")
        else:
            os.system(f"sqlacodegen {conn_url} > {path}")

    def insert_one(self, instance: Base):
        """
        插入一条信息

        :param instance: 模型类
        :return:
        """
        with self.engine.session as session, session.begin():
            session.add(instance)

    def insert_many(self, instance_list: List[Base]):
        """
        插入多条

        :param instance_list: 模型类列表
        :return:
        """
        with self.engine.session as session, session.begin():
            session.add_all(instance_list)

    def merge(self, instance, load: bool = True, options=None):
        """
        根据主键 upsert

        :param instance: 模型类
        :param load:
        :param options:
        :return:
        """
        with self.engine.session as session, session.begin():
            session.merge(instance, load, options)

    def execute(self, sql: str, fetchone: bool = False, fetchmany: int = None, fetchall: bool = False,
                back_dict: bool = False):
        """

        :param sql: sql
        :param fetchone: 返回一条
        :param fetchmany: 返回指定数量
        :param fetchall: 返回多条
        :param back_dict: 以字典形式返回
        :return:
        """
        with self.engine.session as session, session.begin():
            result = session.execute(sql)

        if fetchone:
            back = result.fetchone()
        elif fetchmany:
            back = result.fetchmany(size=fetchmany)
        elif fetchall:
            back = result.fetchall()
        else:
            return

        # 判断是否需要生成字典
        if back_dict and back:
            if isinstance(back, list):
                back = [dict(zip(result.keys(), i)) for i in back]
            else:
                back = dict(zip(result.keys(), back))

        return back

    def delete(self, instance: Base):
        """
        删除数据

        :param instance:
        :return:
        """
        with self.engine.session as session, session.begin():
            session.delete(instance)
