import json

from bp_catalog import bp_catalog
from bp_query import bp_query

from flask import Flask, render_template, session



def create_app():
    app = Flask(__name__, template_folder='template', static_folder='../static')
    app.config['SECRET_KEY'] = '1234'


    app.register_blueprint(bp_catalog, url_prefix='/')
    app.register_blueprint(bp_query, url_prefix='/')


    with open('data/db_config.json') as f:
        app.config['db_config'] = json.load(f)

    return app


# @app.route('/exit')
# def exit_system():
#     session.clear()
#     return render_template('error.html', msg='Вы успешно вышли из системы. До свидания!')


if __name__ == '__main__':

    create_app().run(
        host='localhost',
        port=5001,
        debug=True,
    )
