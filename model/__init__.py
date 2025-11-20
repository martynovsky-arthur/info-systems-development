from dataclasses import dataclass
from database.transaction import Transaction
from database.sql_provider import SQLProvider
from database.DBcm import DBContextManager


@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str


class Model:
    def __init__(self, db_config: dict, provider: SQLProvider):
        self.db_config = db_config
        self.provider = provider

    def select(self, sql_file: str, params: dict) -> ResultInfo:
        print(f'{__name__ = }: {sql_file = }, {params = }')

        _sql = self.provider.get(sql_file)

        with DBContextManager(self.db_config) as cursor:
            cursor.execute(_sql, params)
            result = cursor.fetchall()

        print(f'{__name__ = }: {result = }')

        return ResultInfo(
            result=result,
            status=bool(result),
            err_message=(
                'Ок' if result else 'Данные не получены'
            ),
        )

    def transaction() -> Transaction:
        pass
