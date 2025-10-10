from dataclasses import dataclass

from database.select import select_dict
from database.sql_provider import SQLProvider

@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str


def model_route(provider: SQLProvider, user_input: dict):
    _sql = provider.get('product.sql')
    result = select_dict(_sql, user_input)

    if not result:
        ResultInfo(result=result, status=False, err_message='Данные не получены')

    return ResultInfo(result=result, status=True, err_message='')
