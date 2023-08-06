"""
    pg 方法类
"""
from typing import List
from sqlalchemy.engine import Result
from sqlalchemy.dialects.postgresql import insert
from gtoolkit.db.orm.sqlalchemy.engine import SQLAlchemyEngineBase
from gtoolkit.db.orm.sqlalchemy.methods import SQLAlchemyMethodsBase, BaseModel


class PostgreSQLAlchemyMethods(SQLAlchemyMethodsBase):
    def __init__(self, engine: SQLAlchemyEngineBase):
        super().__init__(engine)

    def upsert_one(
            self,
            instance: BaseModel,
            constraint: str = None,
            index_elements: List[str] = None,
            index_where=None,
            update_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作
        详情见：https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

        index_where=my_table.c.user_email.like('%@gmail.com')

        :param instance: 数据
        :param constraint: 表上唯一或排除约束的名称，或者约束对象本身
        :param index_elements: 由字符串列名、列对象或其他列表达式对象组成的序列
        :param index_where: 可用于推断条件目标索引的附加 WHERE 条件
        :param update_keys: 需要更新的字段（无则全更）
        :return:
        """
        instance_dict = self._get_dict(instance)  # 获取实例的字典
        update_dict = self._get_update_data(instance_dict, update_keys)  # 获取需要更新的字典

        # 构造 sql 语句
        insert_stmt = insert(instance.__table__).values(instance_dict)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint=constraint,
            index_elements=index_elements,
            index_where=index_where,
            set_=update_dict
        )

        return self.execute(do_update_stmt)

    # def upsert_many(
    #         self,
    #         instance: [BaseModel],
    #         constraint: str = None,
    #         index_elements: List[str] = None,
    #         index_where: str = None,
    #         update_keys: List[str] = None
    # ) -> Result:
    #     """
    #     做 更新或插入 操作
    #
    #     :param instance: 数据
    #     :param constraint: 表上唯一或排除约束的名称，或者约束对象本身
    #     :param index_elements: 由字符串列名、列对象或其他列表达式对象组成的序列
    #     :param index_where: 可用于推断条件目标索引的附加 WHERE 条件
    #     :param update_keys: 需要更新的字段（无则全更）
    #     :return:
    #     """
    #     instance_dict = self._get_dict(instance[0])  # 获取实例的字典
    #     update_dict = self._get_update_data(instance_dict, update_keys)  # 获取需要更新的字典
    #
    #     # 构造 sql 语句
    #     insert_stmt = insert(instance.__table__).values(instance_dict)
    #     do_update_stmt = insert_stmt.on_conflict_do_update(
    #         constraint=constraint,
    #         index_elements=index_elements,
    #         index_where=index_where,
    #         set_=update_dict
    #     )
    #
    #     return self.execute(do_update_stmt)
