import json
import os

from flask import Flask, Blueprint, request, jsonify, current_app, render_template

from model_route import model_route

from database.DBcm import DBContextManager
from database.select import select_list
from database.sql_provider import SQLProvider

app = Flask(__name__)
api_bp = Blueprint('api', __name__)


with open('db_config.json', 'r') as f:
    app.config['db_config'] = json.load(f)

Provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

print(f'{os.path = }')
print(f'{os.path.dirname(__file__) = }')


@app.route('/', methods=['GET'])
def product_form_handler():
    return render_template('input_category.html')


@app.route('/', methods=['POST'])
def product_result_handler():
    result_info = model_route(Provider, request.form)

    if not result_info.status:
        return 'Нет ответа от БД'

    return result_info.result  # render_template('dynamic.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=1488,
        debug=True,
    )
