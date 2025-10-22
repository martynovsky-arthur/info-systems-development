# Реализация сценария "каталог"

import os

from access import group_required, login_required
from database.sql_provider import SQLProvider
from flask import Blueprint, render_template, request
from model import model_route


bp_catalog = Blueprint('bp_catalog', __name__, template_folder='templates')

_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_catalog.route('/', methods=['GET', 'POST'])
def catalog_page():

    result = model_route(_provider.get('category.sql'))

    if result.status == False:
        return render_template('error.html', msg=result.err_message)

    categories = result.result

    # Определяем активную категорию
    active_category_id = None
    products = []

    if request.method == 'POST':
        # Получаем категорию из POST запроса
        category_id = request.form.get('category_id')
        if category_id:
            active_category_id = int(category_id)
    else:
        # Для GET запроса выбираем первую категорию по умолчанию
        if categories:
            active_category_id = categories[0][0]  # первый столбец - category_id

    # Получаем товары для активной категории
    if active_category_id:
        result = model_route(
            _provider.get('product.sql'),
            {'category_id': active_category_id},
        )

        if result.status == False:
            return render_template('error.html', msg=result.err_message)

        products = result.result

    return render_template(
        'catalog.html',
        categories=categories,
        products=products,
        active_category_id=active_category_id
    )
