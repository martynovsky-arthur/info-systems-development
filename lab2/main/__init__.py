from flask import Flask, render_template, session
from bp_catalog import bp_catalog
import json


app = Flask(__name__, template_folder='template', static_folder='../static')
app.config['SECRET_KEY'] = '1234'


app.register_blueprint(bp_catalog, url_prefix='/')


with open('data/db_config.json') as f:
    app.config['db_config'] = json.load(f)


# @app.route('/exit')
# def exit_system():
#     session.clear()
#     return render_template('error.html', msg='Вы успешно вышли из системы. До свидания!')


if __name__ == '__main__':
    app.run(
        host='localhost',
        port=5001,
        debug=True,
    )
