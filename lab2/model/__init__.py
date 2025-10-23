from dataclasses import dataclass
from database.select import select_dict
from database.sql_provider import SQLProvider


@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str


def model_route(provider: SQLProvider, sql_file_name: str, user_input: dict) -> ResultInfo:
    err_message = ''
    _sql = provider.get(sql_file_name)
    result = select_dict(_sql, user_input)
    if result:
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        err_message = 'Данные не получены'
        return ResultInfo(result=result, status=False, err_message=err_message)
