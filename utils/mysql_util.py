from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
Base = declarative_base()



class MysqlDB(object):
    def __init__(self, cfg, charset='utf8') -> None:
        self.url = f'mysql+pymysql://{cfg.user}:{cfg.password}@{cfg.ip}:{cfg.port}/{cfg.database}?charset={charset}'
        self._engine = create_engine(self.url, pool_pre_ping=True, pool_recycle=3600, pool_size=10)
        self._cur_session = None
        self._Session = scoped_session(sessionmaker(bind=self._engine))

    def create_tables(self, tables, drop_on_exists=False):
        for table in tables:
            assert hasattr(table, '__tablename__')

            table_exists = inspect(self._engine).has_table(table.__tablename__)
            if not table_exists:
                print(
                    f'create table {table.__tablename__} in {self.url}')

            table = table.__table__
            if drop_on_exists and table_exists:
                table.drop(self._engine)
            table.create(self._engine, checkfirst=True)

    def get_session(self):
        return self._Session()

    def get_table_names(self):
        insp = inspect(self._engine)
        return insp.get_table_names()

    def get_engine(self):
        return self._engine