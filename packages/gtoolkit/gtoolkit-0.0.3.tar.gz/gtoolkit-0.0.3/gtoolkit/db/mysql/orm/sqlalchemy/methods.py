"""
    MYSQL 方法类

    示例：
        method = MysqlSQLAlchemyMethods(engine=MysqlSQLAlchemyEngine())

        method.reverse_table_model(path='./modules.py', tables=[])
        res = method.execute(sql='select * from user', fetchone=True, back_dict=True)
"""
from gtoolkit.db.orm.sqlalchemy.engine import SQLAlchemyEngineBase
from gtoolkit.db.orm.sqlalchemy.methods import SQLAlchemyMethodsBase


class MysqlSQLAlchemyMethods(SQLAlchemyMethodsBase):
    def __init__(self, engine: SQLAlchemyEngineBase):
        super().__init__(engine)
