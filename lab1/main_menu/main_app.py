from flask import Flask, render_template, session
from bp_query.query_route import query_bp
import json


app = Flask(__name__, template_folder='template', static_folder='../static')
app.config['SECRET_KEY'] = '1234'


# Загружаем конфигурацию БД
with open('../data/db_config.json') as f:
    app.config['db_config'] = json.load(f)


# Регистрируем blueprint и передаем ему конфиг
app.register_blueprint(query_bp)


@app.route('/')
def main_menu():
    return render_template('main_menu.html')


@app.route('/exit')
def exit_system():
    session.clear()
    return "👋 До свидания!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
