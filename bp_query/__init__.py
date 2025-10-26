# Реализация сценария "меню запросов"

import os

from access import login_required, group_required
from database.sql_provider import SQLProvider
from flask import Blueprint, render_template, request
from model import model_route


bp_query = Blueprint('bp_query', __name__, template_folder='templates', url_prefix='/query')

query_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_query.route('/', methods=['GET'])
@login_required
def query_menu():
    return render_template('query_menu.html')


@bp_query.route('/category', methods=['GET', 'POST'])
@group_required
def get_category():

    if request.method == 'GET':
        return render_template('category_form.html')

    user_input = request.form

    if not user_input.get('prod_category'):
        return render_template('error.html', msg='Не указана категория товаров')

    result_info = model_route(query_provider, 'category.sql', user_input)

    if not result_info.status:
        return render_template('error.html', msg=result_info.err_message)

    return render_template('category_result.html', items=result_info.result)
