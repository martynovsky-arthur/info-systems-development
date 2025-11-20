import os

from access import login_required
from database.sql_provider import SQLProvider
from flask import Blueprint, redirect, render_template, session, url_for
from model import Model


bp_basket = Blueprint('bp_basket', __name__, template_folder='templates', url_prefix='/basket')

basket_model: Model

@bp_basket.record
def on_register(setup_state):
    global basket_model
    app = setup_state.app
    basket_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
    basket_model = Model(app.config['db_config'], basket_provider)


queries = {
    'get_all_products': 'get_all_products.sql',
}


@bp_basket.route('/')
@login_required
def basket_menu():
    products = basket_model.select(queries['get_all_products'], {})
    basket_count = session.get('basket', {})  # словарь {prod_id(str): amount(int)}

    tmp = {str(product.get('prod_id')): product for product in products}

    basket_info = {}
    for prod_id, amount in basket_count.items():
        prod_data = tmp.get(prod_id, {})
        prod_data.update({'amount': amount})
        basket_info.update({prod_id: prod_data})

    total_price = sum(
        float(item.get('prod_price', '0')) * item['amount']
        for item in basket_info.values()
    )

    return render_template(
        'basket_order_list.html',
        items=products,
        basket=basket_info,
        total_price=total_price,
    )


@bp_basket.route('/add/<string:prod_id>', methods=['POST'])
@login_required
def add_to_basket(prod_id: str):
    basket = session.get('basket', {})
    basket[prod_id] = basket.get(prod_id, 0) + 1
    session['basket'] = basket
    return redirect(url_for('bp_basket.basket_menu'))

@bp_basket.route('/clear')
@login_required
def clear_basket():
    session['basket'] = {}
    return redirect(url_for('bp_basket.basket_menu'))


@bp_basket.route('/save', methods=['GET'])
@login_required
def save_order():
    basket = session.get('basket', {})

    with basket_model.transaction() as tr:
        order_id: int = tr.execute('create_order.sql', {'u_id': session['user_id']})
        for k, v in basket.items():
            tr.execute('create_order_line.sql', {'prod_id': k, 'l_amount': v, 'or_id': order_id})

    return redirect(url_for('bp_basket.clear_basket'))
