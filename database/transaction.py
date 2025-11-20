from database.DBcm import DBContextManager
from database.sql_provider import SQLProvider
from flask import current_app


class Transaction():
    def __init__(self, provider: SQLProvider):
        self._dbcm = DBContextManager(current_app.config['db_config'])
        self._provider = provider
        self._cur = None

    def __enter__(self):
        self._cur = self._dbcm.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._dbcm.__exit__(exc_type, exc, tb)

    def begin():
        pass

    def commit():
        pass

    def rollback():
        pass

    def execute(self, sql_file: str, params: dict) -> int | None:
        sql = self._provider.get(sql_file)
        self._cur.execute(sql, params or {})
        return getattr(self._cur, 'lastrowid', None)
