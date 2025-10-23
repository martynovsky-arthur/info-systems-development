# Реализация сценария "меню запросов"

import os

from access import group_required
from database.sql_provider import SQLProvider
from flask import Blueprint, render_template, request
from model import model_route


bp_query = Blueprint('bp_query', __name__, template_folder='templates', url_prefix='/query')

query_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_query.route('/', methods=['GET'])
@group_required
def query_menu():
    return render_template('query_menu.html')


@bp_query.route('/', methods=['POST'])
@group_required
def execute_query():
    user_input = request.form

    if not user_input.get('prod_category'):
        return render_template('error.html', msg='Не указана категория товаров')

    result_info = model_route(query_provider, 'product.sql', user_input)

    if not result_info.status:
        return render_template('error.html', msg=result_info.err_message)

    product = result_info.result
    prod_title = 'Результат поиска'
    return render_template('query_result.html', prod_title=prod_title, products=product)
