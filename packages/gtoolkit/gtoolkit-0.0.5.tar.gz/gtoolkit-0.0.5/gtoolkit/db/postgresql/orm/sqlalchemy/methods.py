"""
    pg 方法类
"""
from gtoolkit.db.orm.sqlalchemy.engine import SQLAlchemyEngineBase
from gtoolkit.db.orm.sqlalchemy.methods import SQLAlchemyMethodsBase


class PostgreSQLAlchemyMethods(SQLAlchemyMethodsBase):
    def __init__(self, engine: SQLAlchemyEngineBase):
        super().__init__(engine)
