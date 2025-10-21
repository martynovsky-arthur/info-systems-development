from dataclasses import dataclass
from database.select import select_dict

@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str

def model_route(_sql: str, user_input: dict):
    err_message = ''
    result = select_dict(_sql, user_input)
    if result:
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        err_message = 'Данные не получены'
        return ResultInfo(result=result, status=False, err_message=err_message)
