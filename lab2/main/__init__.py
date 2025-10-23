import json

from bp_query import bp_query

from flask import Flask, render_template, session



app = Flask(__name__, template_folder='templates', static_folder='../static')
app.config['SECRET_KEY'] = '1234'


app.register_blueprint(bp_query, url_prefix='/')


with open('lab2/data/db_config.json') as f:
    app.config['db_config'] = json.load(f)


@app.route('/')
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
