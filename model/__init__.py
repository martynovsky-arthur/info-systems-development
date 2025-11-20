from database.DBcm import DBContextManager
from database.sql_provider import SQLProvider


class _Transaction:
    def __init__(self, dbcm: DBContextManager, provider: SQLProvider):
        self._dbcm = dbcm
        self._provider = provider
        self._cur = None

    def __enter__(self):
        self._cur = self._dbcm.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._dbcm.__exit__(exc_type, exc, tb)

    def execute(self, sql_file: str, params: dict) -> int | None:
        sql = self._provider.get(sql_file)
        self._cur.execute(sql, params or {})
        return getattr(self._cur, 'lastrowid', None)


class Model:
    def __init__(self, db_config: dict, provider: SQLProvider):
        self.db_config = db_config
        self.provider = provider

    def select(self, sql_file: str, params: dict) -> dict:

        print(f'{__name__ = }: {sql_file = }, {params = }')

        _sql = self.provider.get(sql_file)

        with DBContextManager(self.db_config) as cursor:
            cursor.execute(_sql, params)
            result = cursor.fetchall()

        print(f'{__name__ = }: {result[0].keys() if result else 'Empty set'}')

        return result

    def transaction(self) -> _Transaction:
        return _Transaction(DBContextManager(self.db_config), self.provider)
