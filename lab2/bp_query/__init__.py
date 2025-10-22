# Реализация сценария "меню запросов"

import os

from access import group_required, login_required
from database.sql_provider import SQLProvider
from flask import Blueprint, render_template, request
from model import model_route


bp_query = Blueprint('bp_query', __name__, template_folder='templates')

_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@login_required
@group_required
@bp_query.route('/', methods=['GET'])
def query_menu():
    return render_template('query_menu.html')


@login_required
@group_required
@bp_query.route('/', methods=['POST'])
def execute_query():
    user_input = request.form
    # print('request.form', user_input)

    if not user_input.get('prod_category'):
        return render_template('error.html', msg='Не указана категория товаров')

    _sql = _provider.get('product.sql')
    result_info = model_route(_sql, user_input)
    if result_info.status:
        product = result_info.result
        prod_title = 'Результат поиска'
        return render_template('query_result.html', prod_title=prod_title, products=product)
    else:
        return render_template('error.html', msg=result_info.err_message)
