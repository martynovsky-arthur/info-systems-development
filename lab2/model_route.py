from dataclasses import dataclass
from database.select import *

@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str

def model_route(provider, user_input: dict):
    err_message = ''
    _sql = provider.get('product.sql')
    result = select_dict(_sql, user_input)
    if result:
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        err_message = 'Данные не получены'
        return ResultInfo(result=result, status=False, err_message=err_message)