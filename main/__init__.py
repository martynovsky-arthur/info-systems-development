import json

from access import login_required

from bp_auth import bp_auth
from bp_basket import bp_basket
from bp_query import bp_query
from bp_report import bp_report

from flask import Flask, render_template, session



app = Flask(__name__, template_folder='templates', static_folder='../static')
app.config['SECRET_KEY'] = '1234'


app.register_blueprint(bp_auth)
app.register_blueprint(bp_basket)
app.register_blueprint(bp_query)
app.register_blueprint(bp_report)


with open('data/db_config.json', encoding='utf-8') as f:
    app.config['db_config'] = json.load(f)


with open('data/access_config.json', encoding='utf-8') as f:
    app.config['access'] = json.load(f)


with open('data/reports_config.json', 'r', encoding='utf-8') as f:
    app.config['reports'] = json.load(f)


with open('data/cache_config.json', 'r', encoding='utf-8') as f:
    app.config['cache'] = json.load(f)


@app.route('/')
@login_required
def main_menu():
    return render_template('main_menu.html')


@app.route('/exit')
def exit_system():
    session.clear()
    return render_template('error.html', msg='Вы успешно вышли из системы. До свидания!')


if __name__ == '__main__':

    app.run(
        host='localhost',
        port=5001,
        debug=True,
    )
