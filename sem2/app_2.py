import json
from flask import Flask, Blueprint, request, jsonify, current_app
from database.DBcm import DBContextManager
from database.select import select_list


app = Flask(__name__)
api_bp = Blueprint('api', __name__)


with open('db_config.json', 'r') as f:
    app.config['db_config'] = json.load(f)


@api_bp.route('/api/get-table-data', methods=['POST'])
def get_table_data():
    try:
        data = request.get_json()
        table_name = data.get('table')
        
        if not table_name:
            return jsonify({'error': 'Table name is required'}), 400
        
        # Безопасное формирование SQL запроса
        sql = f"SELECT * FROM {table_name}"
        
        # Используем вашу функцию select_list
        from your_module import select_list  # Импортируйте функцию из вашего модуля
        
        results = select_list(sql, [])
        
        # Преобразуем результаты в список словарей
        columns = [desc[0] for desc in current_app.config['db_config'].cursor().description]
        data_list = []
        
        for row in results:
            data_list.append(dict(zip(columns, row)))
        
        return jsonify(data_list)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def connect_index():
    _sql = '''select prod_name, prod_measure, prod_price from product
where prod_category = (%s)'''

    prod_params = [1]
    
    print(select_list(_sql, prod_params))
    return 'Все получилось'


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=1488,
        debug=True,
    )