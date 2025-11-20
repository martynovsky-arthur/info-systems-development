from dataclasses import dataclass
from database.select import execute_dict
from database.transaction import Transaction
from database.sql_provider import SQLProvider


@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str


class Model:
    def __init__(self, db_config: dict, provider: SQLProvider):
        self.db_config = db_config
        self.provider = provider

    def execute(self, sql_file: str, params: dict) -> ResultInfo:
        _sql = self.provider.get(sql_file)
        result = execute_dict(self.db_config, _sql, params)

        return ResultInfo(
            result=result,
            status=bool(result),
            err_message=(
                'Ок' if result else 'Данные не получены'
            ),
        )

    def transaction():
        pass
