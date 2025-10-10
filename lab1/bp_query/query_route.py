from flask import Blueprint, render_template, request
from model_route import model_route
from database.sql_provider import SQLProvider
import os

query_bp = Blueprint('query_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_bp.route('/query', methods=['GET'])
def query_menu():
    return render_template('query_menu.html')


@query_bp.route('/query', methods=['POST'])
def execute_query():
    user_input = request.form
    print('request.form', user_input)

    if not user_input.get('prod_category'):
        return render_template('error.html', msg='Не указана категория товаров')

    result_info = model_route(provider, user_input)
    if result_info.status:
        product = result_info.result
        prod_title = 'Результат поиска'
        return render_template('query_result.html', prod_title=prod_title, products=product)
    else:
        return render_template('error.html', msg=result_info.err_message)
